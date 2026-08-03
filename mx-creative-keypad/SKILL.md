---
name: mx-creative-keypad
description: Create, inspect, modify, and validate Logitech MX Creative Console LP5 profiles for the Keypad or Dialpad. Use when a user requests an .lp5 file, Logi Options+ profile, keypad pages, dial actions, keyboard or text macros, application binding, or SVG action icons. Do not use for .lplug4 plugin development.
license: MIT
compatibility: Requires tools that can read and create ZIP archives and JSON files. Use a current LP5 export from the target Logi Options+ installation when possible.
metadata:
  version: "1.0.0"
---

# MX Creative Keypad LP5 Profiles

Create an importable `.lp5` profile for Logi Options+. Treat an LP5 file as a ZIP archive with JSON metadata and action icon templates.

## Required inputs

Identify these values before generation:

- Target device: MX Creative Keypad, Dialpad, or another supported device.
- Target application and its process or bundle name.
- Page names, control positions, and action behavior.
- Output path and profile display name.
- A current exported `.lp5` example when one is available.
- Icon style, palette, and label requirements.

Ask the user only when a missing choice changes the layout or action behavior. Inspect the local Logi profile data when it can answer the question safely.

## Workflow

1. Inspect repository and workspace instructions before changing files.
2. Inspect the current Git status when the output is inside a repository.
3. Read the supplied LP5 example as a ZIP archive. Do not edit the example.
4. Read [the LP5 format reference](references/lp5-format.md).
5. Confirm the device type from a current export or installed Logi profile. Do not guess an unknown device type.
6. Create an action map before creating files. Record every page, control index, action identifier, label, and icon.
7. Keep standalone profiles independent from native plugins unless the user explicitly requests a plugin-backed profile.
8. Generate package files in a task-specific `.temp/` directory.
9. Generate one clear SVG icon for each action. Embed each SVG as base64 in its matching `.ict` action icon template.
10. Create the ZIP archive with the package files at the archive root. Rename the final ZIP file to `.lp5`.
11. Validate the archive, JSON, actions, and SVG content before delivery.
12. Delete only the task-specific temporary directory after validation.

## Action design

- Bind a standalone application profile to the exact process or bundle name.
- Use generic keyboard, text, application, and macro actions that exist in the target Logi installation.
- Copy keyboard layout identifiers and serialized key formats from a current local export. Do not invent them.
- Use uppercase 32-character hexadecimal identifiers for profile, workspace, page, macro, and editor-action names.
- Keep identifiers unique inside the profile. Deterministic identifiers are acceptable when the generator uses stable input names.
- Keep control order explicit. The control index defines the physical position.
- For long text actions, use short key labels and store the full text in the macro action.
- Use navigation controls for approval menus. Do not create an automatic approval action unless the target session and pending request can be verified.

## SVG icon design

- Use a `64 x 64` or `32 x 32` view box.
- Use simple paths, shapes, and short text that remain clear on a small LCD key.
- Use one semantic accent color per page or action group.
- Use error colors only for destructive actions such as Stop or Exit.
- Keep strong contrast between the background and the glyph.
- Put the full action label in the `.ict` text item. Keep the SVG glyph concise.
- Create a unique SVG payload for every action, even when two actions use similar symbols.
- Do not add separate SVG files to the LP5 archive unless a current exported profile uses them.

## Validation

Verify all of these conditions:

- The final file starts with the ZIP signature `50 4B 03 04`.
- `ApplicationInfo.json`, `ProfileInfo.json`, and `metadata/LoupedeckPackage.yaml` exist at the archive root.
- All JSON files parse successfully.
- The manifest name matches the profile name.
- The application and profile device types match.
- Every layout control action resolves to a defined macro, profile action, or installed native action.
- Every custom action has the expected `.ict` file.
- Every embedded base64 image decodes successfully.
- Every embedded SVG parses as XML.
- Page and control counts match the requested hardware layout.
- The archive contains no temporary files or source-only content.
- The original example and installed Logi profile data are unchanged.

If Logi Options+ import testing is allowed, import the new profile only after the structural checks pass. Do not replace an existing customized profile without explicit permission.

## Delivery

Report:

- The final `.lp5` path.
- The target device and application binding.
- The page, action, and icon counts.
- The validation result.
- Any behavior that requires the target application to be active.
- Any feature that a static LP5 profile cannot provide, such as live session state or verified session targeting.

Do not commit, push, install, or import the profile unless the user requests that action.
