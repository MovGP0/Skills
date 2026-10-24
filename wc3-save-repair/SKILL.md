---
name: wc3-save-repair
description: Back up, inspect, and repair Warcraft III and Warcraft III Reforged saved games (.w3z), including map-file mismatch errors after patches and custom campaign companion saves. Use when a user cannot load a WC3 save after an update, needs a save-format diagnosis, or wants a verified recovery copy. Supports donor-based map checksum repair; campaign Lua and native-state changes require a separately verified procedure.
license: MIT
compatibility: Requires Python 3.10 or later for the bundled tool and local access to the saves. Game tests require the matching Warcraft III installation. Internet access is needed only to check current sources or obtain reviewed external tools.
metadata:
  version: "1.0.0"
---

# Warcraft III save repair

Recover a usable copy while preserving the original campaign state. Use plain language. Do not show story text, character names, or zone display names from the payload. Refer to maps by file name. Do not upload saves to a website or include user saves in this skill.

Read [the file-format reference](references/w3z-format.md) before binary work. Read [the campaign repair reference](references/campaign-repairs.md) before editing companion paths, Lua, or native records.

## 1. Confirm the inputs

1. Find the save folder. On Windows, check the actual Documents known folder, including any OneDrive redirection. A common path is `Documents/Warcraft III/BattleNet/<account>/Campaigns/<campaign>/`. Other clients can use other paths.
2. Identify the saves the user wants. Do not select a save from its apparent story progress. Ask for a missing file or path instead of inventing it.
3. Check the installed executable version and content metadata. Keep the exact patch and build. A save serialization marker such as 7000 or 7003 does not identify the installed patch.
4. Ask the user to exit the game before a backup or installation if it is running. Do not kill the game. A file that changes during the backup is an error.
5. Explain the next step before changing files. Continue within existing user authorization; a new confirmation is not needed for each reversible operation.

## 2. Make a verified backup

Back up the whole campaign folder, including `.w3z`, `.w3v`, `.w3p`, subfolders, and zone snapshots. Prefer backing up the whole Warcraft III Documents folder when practical. Put the backup outside the source tree. Never overwrite an existing backup.

```text
python scripts/wc3_save.py backup --source "<campaign folder>" --destination "<new backup folder>"
```

The command creates `Originals/` and `manifest.json`. It compares source hashes before and after copying, checks every copy, and checks the final file inventory. Stop if verification fails. Keep the backup and manifest after the task ends.

Follow the host's script rules. If scripts must run from `.temp/`, copy the tool there and run that copy. Remove only task-owned temporary files after the work. Do not put durable backups in `.temp/`.

## 3. Inspect before repair

```text
python scripts/wc3_save.py inspect "<backup>/Originals/<save>.w3z"
```

The tool validates the supported container, all block CRCs, decompression sizes, final padding, and both structured map checksum fields. Its JSON output includes only file names and format metadata. Inspection writes no files.

Treat the failure by its evidence:

| Result | Next action |
| --- | --- |
| Invalid header/block CRC, truncated file, or invalid zlib | Investigate file damage or another backup. Do not bypass validation. |
| Unsupported layout | Diagnose that version separately. Do not force this parser onto it. |
| Two map checksum fields disagree | Stop. Investigate the layout or an earlier edit. |
| Valid container with an older map checksum | Obtain a donor for the exact target patch and map. |
| Current map identity but load crash or broken play | Investigate native-state or campaign script changes. A checksum edit alone is insufficient. |

Keep CRC validity, map identity, Lua structure, game loading, and game progression as separate results.

## 4. Obtain map identity evidence

Use a fresh save made on the installed target build in the same map. Ask the user to create it if it is missing. Map paths must agree after slash and case normalization. Do not use a donor from another zone, even in the same act.

For each companion map, obtain its own donor. A documented checksum table is an alternative only if its exact target executable/content build is verified. Record the source and revision. Do not reuse historical checksums for another build with the same patch name.

The helper requires `--target-build` for a report. This label does not prove donor provenance; the agent must check the installation and donor creation separately.

## 5. Repair a checksum-only copy

```text
python scripts/wc3_save.py repair --source "<backup>/Originals/<old>.w3z" --donor "<fresh same-map>.w3z" --output "<new candidate>.w3z" --target-build "<verified executable version>"
```

The tool changes only the encoded map checksum and its structured plain copy in the first block. It preserves the preceding four bytes, the complete save build/duration fields, all other expanded payload bytes, and all later compressed blocks. It uses the observed game compression method and refuses a block whose original compression cannot be reproduced exactly. It rereads the output and checks its SHA-256 and allowed changes. An existing output causes failure.

This operation does not migrate Lua, fix native objects, rename companion paths, or prove compatibility. Never present it as a complete campaign migration.

## 6. Handle campaign companions as a bundle

Identify the main save's stored checkpoint directory from its serialized state. A matching folder name is only a fallback when no stored path exists. Check all explicit references. Never borrow another checkpoint's zone state to fill a gap.

Common directories include `Blizzard/<checkpoint>/`, `FKManualSaves/<checkpoint>/`, and `CustomSaves/<checkpoint>/`. `Blizzard/Zones` can hold working state that is replaced when a checkpoint loads.

Prepare each required map separately. Keep the original checkpoint and its companions unchanged. Use a new main filename and an isolated companion directory. A filename change alone does not redirect stored paths. Use a validated campaign adapter to update the actual Lua strings and framing lengths, or keep the candidates outside the live folder until such an adapter is available. Do not copy over the old companion directory.

See [campaign-specific procedures and limits](references/campaign-repairs.md). Review any attached tool's README and code before use. Pin external code to a commit, preserve its license, and keep saves local.

## 7. Validate and install new files

1. Reread every candidate. Validate header and block CRCs, sizes, map identities, format markers, and padding.
2. Compare expanded input/output bytes. Account for every change. A checksum-only edit must leave the complete Lua bytes unchanged, whether or not a Lua walker is available.
3. If Lua strings or code change, require a complete graph walk before and after. Both walks must end at the declared state boundary. Check object count/order, back-references, all framing lengths, pending waits, and the intended edits.
4. Use an independent CRC/zlib check for campaign adapters. Do not count two calls to the same parser as independent verification.
5. Verify that source and backup hashes still match. Check all output destinations before installation. Create new files exclusively; never replace originals.
6. Install the main candidate and its isolated companion bundle with their relative paths intact. Keep a repair report outside the live campaign folder.

The bundled tool does not install files or rewrite campaign paths. Installation is a separate action after bundle validation.

## 8. Hand back a testable result

Give the backup path, new main filenames, companion paths, exact target build, changes, and verification results. Distinguish file validation from in-game proof. Avoid story details.

Ask the user to load a candidate, make a manual save under a new name immediately, reload that new save, and test travel. Track any failure by file name and symptom. Do not claim a complete playthrough from a successful load. Do not promise that a future update will preserve compatibility.

## References and scope

- [Observed W3Z container, map identity, native records, and Lua state](references/w3z-format.md)
- [Campaign adapters, Forsaken Kingdom findings, and script-change cautions](references/campaign-repairs.md)
- [Tool commands and failure behavior](references/tool-usage.md)

The skill provides a general diagnosis workflow and a narrow executable repair. Unknown native formats, unsupported campaigns, and unverified script migrations require further evidence.
