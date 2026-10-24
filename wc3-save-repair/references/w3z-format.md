# Observed Warcraft III W3Z file format

This reference describes the profile observed in Warcraft III: Reforged campaign saves with serialization markers 7000 and 7003. It gives exact offsets for that profile. It is not a complete specification for every Warcraft III release or every native object. Reject another layout until it has been examined.

All integer fields below are little-endian unless stated otherwise. Offsets in the container tables are file offsets. Offsets in the map identity and Lua sections are offsets in the concatenated expanded payload. A map checksum written as `e18988c1` means the four bytes `E1 89 88 C1`, not a number to reverse.

## 1. Container header

The supported header is exactly `0x44` (68) bytes.

| Offset | Size | Type | Meaning and validation |
| --- | --- | --- | --- |
| `0x00` | 28 | bytes | `Warcraft III recorded game` followed by `1A 00`. |
| `0x1C` | 4 | u32 | Header size; 68 in this profile. |
| `0x20` | 4 | u32 | Complete stored file size, including header and block headers. |
| `0x24` | 4 | u32 | Container header version; 1 in this profile. |
| `0x28` | 4 | u32 | Meaningful expanded payload size; excludes final zero padding. |
| `0x2C` | 4 | u32 | Number of compressed blocks. |
| `0x30` | 4 | u32/bytes | Game identifier. Observed integer `0x57335850`, stored as `50 58 33 57`. Preserve it. |
| `0x34` | 4 | u32 | Game/serialization version field. Observed 10200. This is not the installed patch version. |
| `0x38` | 2 | u16 | Save serialization build marker, including observed 7000 and 7003. |
| `0x3A` | 2 | u16 | Flags. Preserve them. Do not treat `0x38..0x3B` as an editable patch-build u32. |
| `0x3C` | 4 | u32 | Duration field. Preserve it; the repair does not infer its units. |
| `0x40` | 4 | u32 | CRC32 of all 68 header bytes with this field set to zero. |

Use the standard reflected CRC-32/ISO-HDLC result returned by Python `binascii.crc32(data) & 0xffffffff`. The test vector `123456789` gives `0xCBF43926`.

For the supported block profile, if `N` is the count and `L` is the meaningful size:

```text
N > 0
(N - 1) * 1048576 < L <= N * 1048576
```

Do not change a build marker simply to match the current game. In earlier recovery work, this caused a load crash. A marker alone does not identify which content patch wrote a file.

## 2. Compressed blocks

The first block starts at `0x44`. Each block has this framing:

| Relative offset | Size | Meaning |
| --- | --- | --- |
| `+0` | 4 | Compressed byte count `C`. |
| `+4` | 4 | Expanded byte count `U`; exactly `0x100000` in the supported profile. |
| `+8` | 4 | Folded block checksum. |
| `+12` | `C` | zlib-wrapped compressed bytes. |

The next block starts at `current + 12 + C`. The last block must end exactly at the stored file size. Concatenate expanded blocks in order. Bytes after the meaningful payload size must be zero. The final block still expands to a full 1 MiB.

### Block checksum

```text
fold(x) = (x XOR (x >> 16)) AND 0xFFFF
H = little_endian_u32(C) || little_endian_u32(U) || 00 00 00 00
checksum = fold(CRC32(H)) OR (fold(CRC32(compressed_bytes)) << 16)
```

The low half covers the 12-byte header with its checksum zeroed. The high half covers the compressed bytes. Store the final u32 little-endian.

### Compression method

The observed game method is zlib, level 1, window bits 15, memory level 8, default strategy, with `Z_SYNC_FLUSH`. Blocks can lack a final zlib end marker. A decoder must accept this framing while checking the exact expanded length and that all input was consumed.

```python
stream = zlib.compressobj(1, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
compressed = stream.compress(raw) + stream.flush(zlib.Z_SYNC_FLUSH)
```

Do not replace it with `zlib.compress(raw)`: its normal finalization changes the stream framing. Reproduce an unchanged original block byte for byte before selecting compression parameters. A different zlib library version can affect reproduction.

For a checksum-only edit, recompress only the first block. Copy later framed compressed blocks byte for byte. Update the first block's compressed length and block checksum, then the total file size and header CRC. The payload size and block count stay unchanged.

## 3. Map identity in the first expanded block

The first expanded block begins with a NUL-terminated ASCII map path in the observed profile. Its path can use `/` or `\`. Use slash and case normalization only for comparison; preserve the original stored path.

The encoded game settings appear later in the same block. The game name before them can be localized, so do not search only for the English text `Local Game`.

### Encoded settings string

The observed English layout includes `Local Game\0\0`, then an encoded string ending at a NUL. Locate it by structure:

1. Search the first 512 bytes for a nonzero candidate preceded by two NUL bytes.
2. Read the candidate up to its terminating NUL.
3. Decode it and require a byte-for-byte encode/decode round trip.
4. Require that the decoded map path matches the leading map path.
5. Check the slot-table structure and the second checksum. Reject ambiguous candidates.

The encoding processes groups of up to seven decoded bytes:

```text
mask byte, encoded byte 1, ..., encoded byte 7
```

Mask bit 0 is set by the observed encoder. For decoded byte `j` within the group, use mask bit `j + 1`:

- Odd decoded byte: store it unchanged and set its mask bit.
- Even decoded byte: store byte + 1 and clear its mask bit.

To decode, keep a byte when its bit is set; otherwise subtract 1. Thus encoded data bytes are nonzero and the NUL can delimit the string. The mask is not a payload byte.

| Offset in decoded settings | Size | Meaning |
| --- | --- | --- |
| `0..8` | 9 | Settings bytes; preserve them. |
| `9..12` | 4 | Map checksum, in stored byte order. |
| `13..first NUL` | variable | Map path. |
| after map path | variable | Remaining settings; preserve them. |

Change only decoded bytes 9 through 12, then re-encode the complete settings string. Its encoded length must remain unchanged. A checksum edit can also change its group mask byte.

### Plain checksum after the slot table

Let `E` be the expanded-payload offset of the encoded settings' terminating NUL.

```text
slot_start = E + 9
slot_size = u16(payload, slot_start)
slot_count = u8(payload, slot_start + 2)
slot_size == 1 + slot_count * 9 + 6
plain_checksum_offset = slot_start + 2 + slot_size + 4
```

The slot table contains the count byte, `slot_count` records of nine bytes, and six trailer bytes. This repair treats the records and trailer as opaque. The four bytes immediately before the plain checksum are also opaque and must remain unchanged.

The four bytes at `plain_checksum_offset` must match decoded settings bytes 9 through 12 before repair. Replace these two structured copies. Do not replace every matching byte sequence in the payload: unrelated values can match by chance.

For decoded checksum byte index `i` in `9..12`, allowed encoded changes are:

```text
mask_offset = settings_start + 8 * floor(i / 7)
data_offset = mask_offset + 1 + (i modulo 7)
```

Together with the four plain checksum bytes, these offsets define the checksum-only allowed-change set. Byte equality outside that set proves that the rest of the expanded payload, including Lua, was preserved.

## 4. Player graphics flag

A profile-specific player record can follow the plain checksum. The reviewed Forsaken Kingdom tool recognizes `u32(1)`, a printable NUL-terminated player name, then a u32 graphics flag. Fresh campaign starts in that profile wrote 4; some later saves wrote 0. Restoring 4 resolved missing-model behavior for those tested saves.

This is not a general W3Z repair rule. Do not search for arbitrary `01 00 00 00` patterns and change the following word. Require the exact player-record context, a known original value, an observed donor, and a separate allowed-byte check. The bundled generic tool leaves this flag unchanged.

## 5. Saved Lua and its enclosing frame

Warcraft saves can include an Eris-style serialized Lua graph. The observed header is:

```text
45 52 49 53 04 52 06 9E BF 04 04 08
 E  R  I  S
```

This is a 32-bit-number Lua 5.3-derived profile. Do not assume that stock Lua bytecode dumps or a general Lua library will read it. Scripts are data during repair; never execute them.

Let `P` be the first byte of the validated Eris header, `S` its declared state length, `W` the number of pending wait IDs, and `T = P - 24 - 4*W`.

| Payload offset | Size | Meaning |
| --- | --- | --- |
| `T` | 4 | Observed framing tag bytes `8E 31 46 1C`. |
| `T + 4` | 4 | Outer length `S + 28 + 4*W`. |
| `T + 8` | 4 | Pending wait count `W`. |
| `T + 12` | 4 | Observed zero word. |
| `T + 16` | `4*W` | Pending wait IDs; preserve order and values. |
| `P - 8` | 4 | Middle length `S + 16`. |
| `P - 4` | 4 | State length `S`. |
| `P` | `S` | Eris header and one complete serialized root value. |

These are three validated length fields in the reviewed implementation. Earlier informal notes referred to additional framing words; do not write guessed fields. Confirm the actual frame against a complete graph walk and donor evidence.

Require `walker_end == P + S`. A string search for `ERIS` is insufficient because saved text can contain the same bytes. Validate the full header, frame, and graph. If the state size changes, update each validated enclosing length, the meaningful payload size, and any affected native enclosing lengths. Rebuild block count/padding only when required. Do not discard nonzero trailing state.

### Value tags

Each value begins with an i32 tag in the observed profile. A full parser must register reference-bearing objects in serialization order before reading their children.

| Tag | Value | Observed body |
| --- | --- | --- |
| 0 | nil | None. Also terminates a table's key/value sequence. |
| 1 | Boolean | u8 flag, 0 or 1. |
| 2 | Profile-specific scalar | Eight bytes consumed by the reviewed reader; its meaning remains unverified. Preserve it. |
| 3 | Number | u8 subtype/flag followed by four number bytes. Do not reinterpret without the subtype contract. |
| 4 | String | u64 byte length, then that many bytes; no required terminating NUL. |
| 5 | Table | Special-form u8 flag. If set, one value. Otherwise u32 ID, key/value pairs until a nil key, then one metatable value. |
| 6 | Closure | u8 C/Lua flag, u8 upvalue count, first value (prototype for Lua closures), then the upvalue values. |
| 7 | Userdata | Special-form u8 flag. If set, one value. Otherwise u64 byte length, u32 field, raw bytes, then one value. |
| 8 | Thread | Stack, execution frames, and open upvalues; see below. |
| 9 | Prototype | Code, constants, child prototypes, upvalue descriptors, and optional debug data; see below. |
| 12 | Upvalue | One serialized value. |
| 13 | Permanent reference | u8 kind followed by one serialized value. |
| greater than 14 | Back-reference | Object index is `tag - 14`. It must refer to an object already registered. |

Tags 10, 11, and 14 are not accepted by the reviewed reader. Bound every length, count, and reference. In the reviewed profile, u64 counts and offsets had zero high words. Another profile requires new evidence.

Do not add or remove objects during a narrow string or bytecode edit. That changes reference indices. Keep object types and order. A byte-for-byte comparison of all unchanged spans is stronger than checking object count alone.

### Prototype layout

After tag 9, the reviewed reader consumes an 11-byte fixed prototype header, then:

1. i32 instruction count and that many four-byte instructions.
2. i32 constant count and serialized constant values.
3. i32 child-prototype count and serialized child values.
4. i32 upvalue count and two bytes per descriptor.
5. u8 flag for optional debug data.
6. If debug data is present: one value, i32 line-info count and four bytes per entry, i32 local count, eight bytes and one value per local, then one value per upvalue name.

Do not relabel opaque header fields without verifying them. A source-line or debug-name match alone is not proof that a prototype is the function to patch. Check its instructions, constants, closure bindings, and call sites.

### Thread layout

The supplied recovery notes describe this layout: u32 ID, u64 field, u8 field, i32 allocated stack count, u64 used-slot count, and the slot values. Then come u8 status, u64 error-function field, call frames, an extra u64 only when status is 1, and open upvalues as `(u64 index, value)` until a zero index.

A call frame has u64 function slot, u64 top, i16 result count, u8 call-status flags, conditional fields, and a final u8 last-frame flag. The notes associate bit `0x02` with u64 base/saved-PC and bit `0x10` with a u64 extra field; a continuation can add a flag, u32 context, and a value.

The reviewed upstream walker uses a specific conditional order that differs from the preliminary notes: it reads the `0x10` field before the `0x02` fields, and its continuation branch is an alternative to the `0x02` branch. Therefore the bit combinations and complete continuation layout are not established here as a universal contract. Use the pinned, reviewed walker only for its proven profile, require exact end-of-state validation, and stop on an unverified thread layout. Do not use a partial walker to authorize a script edit.

## 6. Native object state

The expanded payload also contains engine-owned records outside Lua. The reviewed campaign adapter uses `espi` record markers and bounded record lengths to locate allocation and instance tables. Type identifiers can be stored in byte order that differs from their readable names. Matching a text marker alone is unsafe.

Some patch changes insert fields into native unit, projectile, or camera records. A map checksum change cannot migrate those layouts. Require a documented source/target layout, exact type and object-ID checks, enclosing-length checks, unchanged-script proof, and a donor or game test. Unknown layouts must stop conversion.

This reference does not claim to specify the complete native payload. The bundled tool preserves it byte for byte outside the two map identity fields.

## 7. Companion files are separate containers

Each companion `.w3z` has its own header, map identity, compressed blocks, and possibly Lua/native state. It needs its own target map checksum. The main save's serialized script can store its checkpoint directory as ordinary tag-4 strings. Renaming a directory on disk does not change these strings.

To isolate a repaired checkpoint, change only the verified stored path strings, update their u64 byte lengths and all enclosing Lua lengths, and walk the graph again. References to those string objects must remain valid. Keep the original companion snapshots; working zone files are not interchangeable with checkpoint snapshots.

## Evidence and limits

- This session validated nine new files from three checkpoints against target executable 3.0.1.24371: complete container checks, Python/zlib checks, complete Lua walks, and unchanged bytecode. In-game load and travel were not observed by the agent. No private save data is bundled here.
- The map identity, CRC, compression, and Lua-frame rules were cross-checked against reviewed [Forsaken Save Repair source](https://github.com/XPlay1990/forsaken-save-repair/tree/30ea5917ddc420198f7992fa09d281badf467bb5/src). This is a pinned source snapshot, not a promise of current support.
- Compare the independent [donor checksum tool](https://github.com/josefgraus/w3z_map_checksum_repair) when needed. Read its current source before use; its supported layout can differ.
- Treat the user's campaign-specific Lua repair notes as leads that need local evidence. They do not establish a complete format for unrelated maps or builds.
