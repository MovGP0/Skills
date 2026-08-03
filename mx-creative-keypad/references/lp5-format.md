# LP5 Format Reference

Use this reference after the skill workflow selects LP5 profile creation or inspection.

## Archive structure

An `.lp5` file is a ZIP archive. A typical standalone profile contains:

```text
ApplicationInfo.json
ProfileInfo.json
ApplicationIcon.png             # Optional
ActionIcons/
  <action-id>.ict
ActionImages/                    # Optional
metadata/
  LoupedeckPackage.yaml
  ProfilePreview.json
  AdvancedInfo.json
```

Place these entries at the archive root. Do not add a parent directory around them.

## Device types

Use a current export to confirm the device type.

Known examples:

| Device type | Observed layout |
| --- | --- |
| `Loupedeck70` | MX Creative Keypad profile with nine LCD key controls per page. |
| `Loupedeck71` | MX Creative Dialpad profile with four press controls and two dial controls. |

Do not infer the meaning of another device type from its number. Inspect a current profile from the target installation.

## Standalone application binding

Use a standalone application record when the profile does not require an installed native plugin:

```json
{
  "$type": "Loupedeck.Service.SupportedApplicationInfo, LoupedeckService",
  "name": "@_example_application",
  "displayName": "Example Application",
  "description": "Custom controls for Example Application.",
  "deviceType": "Loupedeck70",
  "nativePluginName": null,
  "hasNativePlugin": false,
  "processOrBundleName": "ExampleProcess",
  "modes": [
    {
      "$type": "Loupedeck.Service.ApplicationMode, LoupedeckService",
      "name": "main",
      "parentModeName": null,
      "displayName": "Main"
    }
  ],
  "defaultProfileName": "PROFILE_ID",
  "isEnabled": true
}
```

On Windows, use the process name format observed in a current profile or plugin. It often omits `.exe`.

Use matching standalone fields in `ProfileInfo.json`:

```json
{
  "applicationName": "@_example_application",
  "nativePluginName": null,
  "hasNativePlugin": false,
  "additionalNativePluginNames": [
    "DefaultWin"
  ]
}
```

Use `DefaultMac` instead of `DefaultWin` only when a current macOS profile requires it.

## Manifest

The profile manifest is `metadata/LoupedeckPackage.yaml`:

```yaml
type: Profile5
name: PROFILE_ID
displayName: Example Profile
version: 1.0.0.0
```

The `name` must match the profile identifier in `ProfileInfo.json` and the default profile identifier in `ApplicationInfo.json`.

## Layout records

The common layout type names are:

```text
Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayout7, LoupedeckService
Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayoutMode7, LoupedeckService
Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayoutWorkspace7, LoupedeckService
Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayoutPage7, LoupedeckService
Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayoutControl7, LoupedeckService
```

A key control uses `pressAction`. A dial control uses `rotateAction`:

```json
{
  "$type": "Loupedeck.Service.Devices.Loupedeck7Devices.ProfileLayoutControl7, LoupedeckService",
  "controlId": 0,
  "pressAction": "$@Generic___@Macro___MACRO_ID",
  "rotateAction": null
}
```

Keep `controlId` values zero-based and in physical layout order.

## Macro commands

A custom macro uses this action identifier:

```text
$@Generic___@Macro___MACRO_ID
```

The matching `macroCommands` entry uses the identifier without the prefix:

```json
{
  "$type": "Loupedeck.Service.ApplicationProfileMacroCommand, LoupedeckService",
  "isCommand": true,
  "name": "MACRO_ID",
  "displayName": "Example",
  "description": "",
  "groupName": "Example",
  "superGroupName": "@macro",
  "supportedOs": "All",
  "supportedModes": [
    "main"
  ],
  "showAsSingleAction": false,
  "actionEditorCommands": [],
  "isMultiState": false,
  "actions": []
}
```

### Text input

A generic text action can appear in a macro action list:

```text
$@Generic___@TypeText___Text to enter
```

Test text that contains separators, control characters, or non-ASCII characters against a current exported profile. Do not assume an escaping rule.

### Keyboard input

A keyboard macro normally declares an editor action:

```json
{
  "$type": "Loupedeck.Service.MacroActionEditorCommand, LoupedeckService",
  "name": "KEY_ACTION_ID",
  "templateName": "$@Generic___@KeyboardKey",
  "actionParameters": {
    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.String, System.Private.CoreLib]], System.Private.CoreLib",
    "keyboardKey": "Return___LOCAL_LAYOUT_ID___Return___"
  }
}
```

Put `KEY_ACTION_ID` in the macro `actions` array at the point where the key must run.

Valid normalized key names include values such as:

```text
Escape
Return
Tab
ArrowUp
ArrowDown
PageUp
PageDown
ControlOrCommand+KeyV
ControlOrCommand+Shift+KeyT
```

Copy `LOCAL_LAYOUT_ID` and the complete serialized key form from the target installation. Keyboard layout values can differ between systems and exports.

Use generic sleep actions when a sequence needs a short delay:

```text
$@Generic___@Sleep___500
```

## Action icon templates

Name each custom icon file after its complete action identifier:

```text
ActionIcons/$@Generic___@Macro___MACRO_ID.ict
```

An `.ict` file is JSON. The `image` value can contain a base64-encoded SVG:

```json
{
  "backgroundColor": 4278190080,
  "items": [
    {
      "$type": "Loupedeck.Service.ActionIconImageItem, LoupedeckShared",
      "image": "BASE64_ENCODED_SVG",
      "imageFileName": "",
      "imageColor": 4294967295,
      "imageRotation": "None",
      "isVisible": true,
      "itemType": "Image",
      "area": {
        "x": 16,
        "y": 0,
        "width": 68,
        "height": 68
      }
    },
    {
      "$type": "Loupedeck.Service.ActionIconTextItem, LoupedeckShared",
      "text": "Example",
      "textColor": 4294967295,
      "fontSize": 5,
      "fontName": "Brown Logitech Pan Light",
      "isVisible": true,
      "itemType": "Text",
      "area": {
        "x": 0,
        "y": 68,
        "width": 100,
        "height": 32
      }
    }
  ]
}
```

This format does not require a separate PNG conversion. Keep a PNG fallback only when a current target profile proves that it is required.

## Packaging checks

After creating the archive:

1. Confirm the first bytes are `PK` or hexadecimal `50 4B 03 04`.
2. List the archive entries and confirm that required files are at the root.
3. Extract to a new temporary directory.
4. Parse all JSON files.
5. Compare the manifest, application, profile, mode, and device identifiers.
6. Resolve every layout action against macros, profile actions, or installed actions.
7. Decode every icon image.
8. Parse every decoded SVG as XML.
9. Confirm page and control counts.
10. Confirm that the installed Logi profile store and source examples are unchanged.

Do not claim Logi Options+ import compatibility from the ZIP signature alone. Report structural validation separately from an actual import test.
