# Bundled tool

`scripts/wc3_save.py` uses Python 3.10 or later and the standard library only. It has no network access code. Read the tool before running it on private data.

## Commands

```text
python scripts/wc3_save.py backup --source "<folder>" --destination "<new backup folder>"
python scripts/wc3_save.py inspect "<save>.w3z"
python scripts/wc3_save.py repair --source "<old>.w3z" --donor "<fresh same-map>.w3z" --output "<new>.w3z" --target-build "<verified version>"
```

The backup destination must not exist and must be outside the source. The backup contains `Originals/` and `manifest.json`. The manifest contains relative paths, lengths, SHA-256 hashes, and source timestamps. Source paths and backup paths are local information. Do not publish a manifest without checking it for private names.

`inspect` validates the complete container but does not execute or parse saved scripts. The `serialization_build` value is the u16 at header offset `0x38`. The tool reports `map_file`, which is the last component of the stored map path, rather than the localized display name. It does not dump saved text.

`repair` checks both inputs, requires the same normalized map path and game identifier/version fields, and requires different map checksums. It does not change the source or donor. It creates only the requested output. The JSON result goes to stdout; redirect it to a separate new report file if needed. Errors go to stderr and return exit code 2.

Outputs use exclusive creation. If output verification fails after creation, the new candidate can remain for diagnosis. It must not be installed. No original is deleted or replaced.

## Supported binary profile

The tool supports the observed 68-byte header, 12-byte block header, and 1 MiB expanded blocks. It limits the expanded container to 1 GiB. It stops on other layouts. A general recovery workflow does not imply one universal parser for all Warcraft III versions.

Only the first block is recompressed. The tool checks that the original first block is reproduced by zlib level 1, window bits 15, memory level 8, default strategy, and `Z_SYNC_FLUSH`. This rejects a different compressor or framing rather than assuming that arbitrary recompression is safe.

The default zlib library can differ across Python builds. If the compression reproduction check fails, investigate the compressor version and original framing. Do not remove the check merely to obtain output.

## Deliberate limits

- No hard-coded campaign checksums or installed build numbers.
- No recursive search of unrelated disks.
- No Lua or native-state migration.
- No claim that valid bytes will run correctly in a newer engine.
- No automatic companion discovery, renaming, or installation.
- No donor creation or launch of the game.

Use a reviewed campaign adapter where the main skill requires one. Keep any adapter changes within an explicit allowed-byte or structural edit plan.

## Validation during development

Copy `scripts/wc3_save.py` and `tests/test_wc3_save.py` into a task-owned `.temp/` directory when host rules require scripts there. Keep the two files in the same directory for this test command:

```text
python -m unittest discover -s "<temporary directory>" -p test_wc3_save.py
```

Tests create synthetic containers. They cover CRC failure, map mismatch, compression framing, payload preservation, an existing output, and complete verified backups. Tests do not contain game data or demonstrate game compatibility.
