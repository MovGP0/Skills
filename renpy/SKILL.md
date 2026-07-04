---
name: renpy
description: Inspect, unpack, edit, sign, and repack Ren'Py save files. Use when working with Ren'Py .save archives, save metadata JSON, screenshot/extra_info/log/signatures entries, machine save-token keys, or when a user asks to modify or repair a Ren'Py savegame.
---

# Ren'Py Save Files

## Core Format

Treat a Ren'Py `*.save` file as a ZIP archive, usually written with Python `zipfile.ZIP_DEFLATED`.

Expected entries:

- `screenshot.png` or older `screenshot.tga`
- `extra_info`: UTF-8 save-name text
- `json`: JSON metadata bytes
- `renpy_version`: UTF-8 version string
- `log`: pickled game state bytes
- `signatures`: UTF-8 save-token signature lines

Do not unpickle `log` unless the user explicitly asks and the file is trusted. Pickle loading can execute code.

Ren'Py signs the `log` entry, not the `json` entry. JSON-only edits do not require a new signature as long as `log` bytes are preserved exactly. If `log` changes, replace `signatures` with a fresh signature over the new `log` bytes.

Many game variables are not in `json`; they are inside the pickled `log` as store variables such as `store.variable_name`. Expect stats, inventory, flags, and relationship values to require `log` edits.

## Unpack Safely

Use Python `zipfile`; do not rely on archive tools that may normalize timestamps, paths, or compression unexpectedly.

```python
import json
import zipfile
from pathlib import Path

save_path = Path(r"C:\path\to\slot.save")
out_dir = Path(r"C:\path\to\unpacked-slot")

with zipfile.ZipFile(save_path, "r") as zf:
    zf.extractall(out_dir)
    names = zf.namelist()
    metadata = json.loads(zf.read("json"))
    signatures = zf.read("signatures").decode("utf-8", "replace") if "signatures" in names else ""
```

When reporting contents, include entry names and sizes. Avoid printing or decoding `log`.

## Edit JSON

Load `json` as UTF-8 JSON, modify only requested keys, then write compact JSON bytes. Preserve value types; Ren'Py metadata commonly includes:

- `_save_name`: string
- `_renpy_version`: list of integers
- `_version`: game version string or null
- `_game_runtime`: number
- `_ctime`: Unix timestamp number

```python
import json
from pathlib import Path

json_path = Path(r"C:\path\to\unpacked-slot\json")
data = json.loads(json_path.read_bytes())
data["_save_name"] = "New Save Name"
json_path.write_bytes(json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
```

If editing only `json` or `extra_info`, preserve the original `log` and `signatures`.

## Inspect Log Without Loading It

Use `pickletools` to inspect the pickle opcode stream without executing game code. Search for variable names as bytes first, then disassemble a narrow window around relevant offsets.

```python
import pickletools
import re
import zipfile

with zipfile.ZipFile(r"C:\path\to\slot.save", "r") as zf:
    log = zf.read("log")

for name in [b"store.mc_stats", b"mc_stats", b"hp", b"maxhp"]:
    print(name, [m.start() for m in re.finditer(re.escape(name), log)][:20])

for op, arg, pos in pickletools.genops(log):
    if 62000 <= pos <= 63000:
        print(pos, op.name, repr(arg))
```

Interpret the pickle stream before editing. For example, a Ren'Py store variable often appears as:

```text
BINUNICODE 'store.some_variable'
GLOBAL 'store SomeClass'
...
SHORT_BINSTRING 'field_name'
BININT1 16
```

If values are small integers encoded as `BININT1`, the opcode byte is `0x4B` and the next byte is the integer value. Values `0..255` can be patched in place by changing only that argument byte. This keeps the pickle length and memo table unchanged.

Do not do byte-level patches unless all of these are true:

1. The target value is identified in the disassembly, not only by a raw string match.
2. The byte before the edited offset is the expected pickle opcode, such as `0x4B` for `BININT1`.
3. The replacement value fits the same opcode encoding.
4. The edit is verified by disassembling the modified `log`.

For larger structural changes, prefer using the game's Ren'Py/Python runtime to load and reserialize, but only with trusted saves.

## Read Persistent File

Treat the per-game `persistent` file as compressed pickle bytes followed by signature text. It is not a ZIP archive.

Format:

```text
zlib.compress(pickle_bytes, 3) + signatures_utf8
```

Ren'Py reads it with `zlib.decompressobj()`: decompressed data is the pickle payload, and `decompressobj.unused_data` is the appended UTF-8 save-token signature text.

Inspect without unpickling:

```python
import pickletools
import zlib
from pathlib import Path

path = Path(r"C:\path\to\saves\persistent")
raw = path.read_bytes()

do = zlib.decompressobj()
pickle_bytes = do.decompress(raw)
signatures = do.unused_data.decode("utf-8", "replace")

print("pickle bytes:", len(pickle_bytes))
print("signature text:")
print(signatures)
pickletools.dis(pickle_bytes)
```

Only unpickle trusted persistent files:

```python
import pickle
import zlib
from pathlib import Path

raw = Path(r"C:\path\to\saves\persistent").read_bytes()
do = zlib.decompressobj()
pickle_bytes = do.decompress(raw)
persistent = pickle.loads(pickle_bytes)
print(persistent.__dict__)
```

When modifying `persistent`, sign the uncompressed `pickle_bytes`, not the compressed file bytes. Repack with:

```python
new_raw = zlib.compress(new_pickle_bytes, 3) + new_signature_text.encode("utf-8")
```

The signature text uses the same `signature <public-key-base64> <signature-base64>` line format as `.save` archives.

## Locate Machine Keys

Ren'Py save-token keys are stored in a `security_keys.txt` file in the local Ren'Py tokens directory. On Windows this is commonly under:

```text
%APPDATA%\RenPy\tokens\security_keys.txt
```

Search if needed:

```text
rg --files "%APPDATA%\RenPy" -g security_keys.txt
```

Key lines use base64 fields:

```text
signing-key <private-key-der-base64> <public-key-der-base64>
verifying-key <public-key-der-base64>
```

The `signatures` save entry uses:

```text
signature <public-key-der-base64> <signature-base64>
```

Only sign with keys from the user's own machine or keys explicitly supplied by the user.

## Sign The Log

Prefer the exact Ren'Py implementation bundled with the game or engine version. Depending on Ren'Py version, `savetoken.py` signs with either `renpy.ecsign` or the Python `ecdsa` package, then writes `signature` lines containing the public key and signature.

Use the bundled game/runtime Python when possible, because it has the same dependencies and bytecode compatibility as the target game. On Windows, common bundled interpreters include:

```text
lib\py2-windows-x86_64\python.exe
lib\py3-windows-x86_64\python.exe
```

If `renpy.savetoken` exposes a direct loader for token files, use it:

```python
import renpy.savetoken

renpy.savetoken.load_tokens(r"C:\Users\YOU\AppData\Roaming\RenPy\tokens\security_keys.txt")
signature_text = renpy.savetoken.sign_data(log_bytes)
```

If the game's `savetoken.py` uses `ecdsa`, a standalone signing script can mirror it:

```python
import base64
import ecdsa

def decode_line(line):
    parts = line.strip().split(None, 2)
    if len(parts) == 2:
        return parts[0], base64.b64decode(parts[1]), None
    return parts[0], base64.b64decode(parts[1]), base64.b64decode(parts[2])

def encode_line(kind, a, b):
    return kind + " " + base64.b64encode(a).decode("ascii") + " " + base64.b64encode(b).decode("ascii") + "\n"

signing_keys = []
with open(r"C:\Users\YOU\AppData\Roaming\RenPy\tokens\security_keys.txt", "r") as f:
    for line in f:
        kind, key, _ = decode_line(line)
        if kind == "signing-key":
            signing_keys.append(ecdsa.SigningKey.from_der(key).to_der())

signature_text = ""
for key in signing_keys:
    sk = ecdsa.SigningKey.from_der(key)
    signature_text += encode_line("signature", sk.verifying_key.to_der(), sk.sign(log_bytes))
```

If the local Ren'Py runtime cannot import its signing dependencies, do not guess the signature algorithm for a modified `log`. Either run the script with the game's bundled Python/runtime or leave `log` unchanged and preserve the existing `signatures` entry.

For JSON-only edits, do not regenerate signatures unless the user specifically asks; copying the original `signatures` entry is correct because verification covers `log`.

## Choose Save Filename

Match the existing save naming convention in the target save directory before writing output. Do not assume an arbitrary suffix.

Manual Ren'Py saves commonly use:

```text
<page>-<slot>-LT<version>.save
```

Examples:

```text
1-1-LT1.save
1-2-LT1.save
1-3-LT1.save
```

Autosaves commonly use:

```text
auto-1-LT1.save
auto-2-LT1.save
```

Before creating a new save, list the directory and choose a filename consistent with neighboring files. If duplicating a manual save into the next slot, increment the slot component (`1-1-LT1.save` -> `1-2-LT1.save`) rather than changing `LT1` to `LT2`. Treat `LT*` as part of Ren'Py's filename format, not a version number to increment for edited copies unless existing files show that pattern.

## Repack

Repack with the same canonical entry names. Use deflated ZIP entries and write bytes exactly as prepared.

```python
import zipfile
from pathlib import Path

src = Path(r"C:\path\to\unpacked-slot")
dst = Path(r"C:\path\to\slot.modified.save")

entry_order = [
    "screenshot.png",
    "screenshot.tga",
    "extra_info",
    "json",
    "renpy_version",
    "log",
    "signatures",
]

with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
    written = set()
    for name in entry_order:
        p = src / name
        if p.exists():
            zf.writestr(name, p.read_bytes())
            written.add(name)
    for p in sorted(src.iterdir()):
        if p.is_file() and p.name not in written:
            zf.writestr(p.name, p.read_bytes())
```

Never overwrite the original save directly. Write a new file first, validate it, then replace only if the user asks.

## Validate

After repacking:

1. Reopen the new save with `zipfile.ZipFile`.
2. Confirm `json` parses with `json.loads`.
3. Confirm `log` exists and has the expected byte length; byte-level integer patches should normally preserve exact length.
4. Confirm `signatures` exists when the original had it.
5. If a Ren'Py runtime is available, verify with `renpy.savetoken.verify_data(log_bytes, signatures_text, check_verifying=False)`.
6. If using `ecdsa` directly, verify each `signature` line with `ecdsa.VerifyingKey.from_der(public_key).verify(signature, log_bytes)`.
7. Re-disassemble edited `log` windows with `pickletools` and confirm the requested values changed.
8. Keep a backup of the original save until the user confirms the modified save loads.
