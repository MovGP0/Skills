# Campaign repair and script migration

## Select the exact target

Check both executable version and installed content metadata. Patch names can be reused with different content. In the source session, the installed executable was 3.0.1.24371, while reference instructions targeted 3.0.1.24342. Their map checksums differed. The agent used the installed build rather than the historical reference values.

Never infer the content patch from serialization marker 7000 or 7003. Do not copy a donor's whole header or native state into an older save. Those bytes can contain progress and engine state.

## Treat a checkpoint and its companions as one unit

1. Back up the complete folder and verify hashes.
2. Inspect the selected main file and locate its actual stored companion paths.
3. Resolve only that checkpoint's existing snapshots. Report missing explicit paths. Do not replace missing snapshots with another checkpoint or fresh starting state.
4. Obtain the target checksum for every map in the bundle.
5. Create a new main filename and a separate companion folder. Rewrite the stored path strings with a validated Lua-aware adapter.
6. Verify the complete graph and every unrelated byte. Then install only new paths.

`Blizzard/Zones` can be working state. A main save can restore old companion files there on load. Repairing only that working directory can be undone by the next load. Do not overwrite it while the game is active as a routine recovery method.

## Forsaken Kingdom adapter

The source session reviewed [XPlay1990/forsaken-save-repair](https://github.com/XPlay1990/forsaken-save-repair) at commit `30ea5917ddc420198f7992fa09d281badf467bb5`. This tool is separate from the bundled Python helper. It contains map-version profiles, container checks, a Lua graph reader, stored-folder renaming, a graphics flag repair, and selected native-state migrations.

Before using it again:

1. Read its README, license, profile definitions, repair code, and code for any selected migration.
2. Check that the exact installed target build is supported. Inspect the map table's evidence, not just its display text.
3. Pin the source commit. Install dependencies without lifecycle scripts where possible. Keep all processing local.
4. Pass `Uint8Array` values to its browser-oriented functions. A Node `Buffer.slice()` shares storage; code that expects `Uint8Array.slice()` to make a copy can modify the input buffer while calculating CRCs. Use `new Uint8Array(buffer)` to make a copy.
5. Validate every output independently. Do not infer game compatibility from a tool's status label.

Do not vendor private saves, fixed local paths, account IDs, or a local checksum table into a general skill. The skill does not automatically download or run this adapter.

### What the source-session repair changed

Three user-selected saves and six existing companions had recognized source revisions. The repair changed map identity, restored the observed graphics flag where needed, and renamed stored checkpoint paths into isolated companion folders. All original and backup hashes were checked again. A full graph walk ended at each declared boundary, object counts and wait IDs stayed unchanged, bytecode stayed unchanged, and an independent Python check validated all containers.

This evidence covers file-level validation. The user expressed satisfaction, but the agent did not observe an in-game load, travel, resave, or a complete playthrough. Do not upgrade that statement into a stronger result.

## Script changes: conditional research leads

The following notes came from an Act Two recovery procedure. They were not applied in the source-session repair. Use them only when inspection proves that the selected save contains the affected functions/configuration and that the target engine has the required APIs. Refer to map filenames only in user-facing output.

### Random item drops

The notes describe an older `CreateRandomItem` function using:

```text
ChooseRandomItemExWithFilterBJ(level, ITEM_TYPE_EQUIPMENT,
    EQUIPMENT_TYPE_ANY, ITEMTAG_TYPE_DROPPABLE)
```

The proposed target is a protected call:

```text
pcall(ChooseRandomItemExWithFilterAndIncludes,
    ITEM_TYPE_EQUIPMENT, level, EQUIPMENT_TYPE_ANY,
    ITEMTAG_TYPE_DROPPABLE, true, true)
```

Skip the item creation if the protected call fails. This is a Lua bytecode migration, not a string substitution. Confirm argument order, registers, result values, branch targets, constants, upvalues, stack size, and instruction count against actual source and target prototypes. Reuse a constant only if all of its uses are known and safe to change. A constant described as debug-only still needs that proof.

### Transition configuration

For the affected profile, the notes propose these value changes:

| Configuration field | Old value | Proposed target value |
| --- | --- | --- |
| `GameCacheFile` | `FKCache.w3v` | `Campaigns.w3v` |
| `GameCacheMissionKey` | `FK_Transition` | `UndeadRE02Transitions` |
| `ZoneSaveFolder` | `ForsakenKingdom` | `Blizzard\Zones` |

Locate the actual configuration table using its keys, including `UseZoneFolder` and `SaveExtension`. Check each value object's full reference/use set. Do not change another table merely because it has the same text.

The notes propose changing `FK_IsPendingTransitionForCurrentMap` from:

```text
(pendingBool or pendingInt == 1) and source > 0 and target == CurrentZone
```

to:

```text
source > 0 and
    (target == 0 or ((pendingBool or pendingInt == 1) and target == CurrentZone))
```

Confirm that the target scripts use `TransitionSource` and `TransitionTargetArea` with those meanings. Construct a truth table and verify the compiled control flow. Do not infer working bytecode from the high-level expression alone. Preserve all other functions.

### Native state

Some old projectile records need a targeted field migration. Other conversions, especially downgrades, can affect units, camera state, saved API bindings, and record lengths. Apply only the adapter's exact validated type/layout rules. A partial or unknown record blocks conversion.

## Required proof for an advanced adapter

- Input and output containers are valid.
- Source and target map identities are verified for the exact build.
- A full Lua walk ends at the declared boundary before and after every edit.
- Object types/order and back-reference targets remain correct.
- String lengths, code sizes, stack bounds, and all enclosing lengths are correct.
- All changes are accounted for by a recorded edit plan; unchanged spans compare equal.
- Companion selection and path rewriting preserve the checkpoint's own progress.
- Fresh game tests cover load, a new manual save, reload, and travel. Further progress remains unverified until tested.

If a required donor or format detail is missing, ask for it. Do not guess a checksum, invent progression, or disable a guard to force output.
