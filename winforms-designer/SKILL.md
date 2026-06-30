---
name: winforms-designer
description: Rules for manually editing WinForms *.Designer.cs files, resources, project nesting, InitializeComponent order, and designer-safe event wiring. Use when changing WinForms designer files or related resx/csproj metadata.
---
# WinForms Designer Rules

This document describes the formatting rules for manually edited `*.Designer.cs` files. These files must stay compatible with the Visual Studio WinForms designer, so prefer the designer's generated style over the repository's normal C# style when they differ.

## General Rules

- Keep `*.Designer.cs` files as designer-only files. Do not add business logic, dependency injection, behavior activation, data binding, or command handling here.
- Do not use file-scoped namespaces in `*.Designer.cs` files. Use block-scoped namespaces.
- Use Allman braces.
- Use spaces only, with 4 spaces for C# indentation.
- Keep the standard designer layout:
  - `components` field
  - `Dispose(bool disposing)`
  - `InitializeComponent()`
  - control field declarations at the end of the class
- Keep the generated comments, especially control separator comments:

```csharp
// 
// controlName
// 
```

- Keep explicit framework type names where the designer writes them, for example:

```csharp
this.panel1 = new System.Windows.Forms.Panel();
```

- Do not replace designer-generated literals with `nameof(...)`. The WinForms designer expects string literals for resource keys, names, and property values.
- Do not modernize designer code with target-typed `new`, collection expressions, pattern matching, local functions, or helper abstractions.
- Do not reorder statements unless required by control parenting or initialization order.

## `InitializeComponent()`

- Create controls before they are referenced.
- Keep `SuspendLayout()`, `ResumeLayout(...)`, `BeginInit()`, and `EndInit()` balanced and in the same order as the designer expects.
- Add child controls to their parent only after the child has been instantiated.
- Preserve parent-child order and z-order. `Controls.Add(...)` order is behaviorally relevant.
- Use `resources.ApplyResources(...)` for localized controls when the rest of the file uses resources.
- Keep root control changes explicit. When a control is moved from a `Form` or `XtraTabPage` into a `UserControl`, verify:
  - the root control is added to `this.Controls`
  - `this.AutoScaleMode`, `this.Name`, and resource application target the new root correctly
  - old parent references in `*.resx` files are moved or removed

## Field Declarations

- Declare controls at the end of the designer partial class.
- Use the same visibility as the surrounding designer file.
- Prefer `private` for implementation details.
- Use `internal` only when another partial class or behavior must access a child control directly.
- Keep field names unchanged during moves unless the resource files and all references are updated at the same time.

## Resources

- Preserve `resources.ApplyResources(this.controlName, "controlName");` calls.
- Resource keys must match the exact control field name and property name.
- Do not change `.resx` headers unless intentionally regenerating the full resource file.
- Do not remove assembly references from `.resx` files. WinForms and DevExpress resource entries often require them.
- Keep resource XML formatting stable:
  - 2 spaces for XML indentation
  - no empty lines between the final `</resheader>` and `</root>` except actual `<data>` entries
  - all `<data ...>` entries indented consistently with 2 spaces
- When moving controls, move the corresponding resource entries with scripts for larger moves.

## Project File Nesting

WinForms files must be nested correctly in the owning `*.csproj` file. This keeps Visual Studio and Rider showing the form/control as one designer item and helps the WinForms designer find the matching code-behind and resources.

For a control named `SomeFeature\SomeControl`, use this structure:

```xml
<Compile Update="SomeFeature\SomeControl.cs">
  <SubType>UserControl</SubType>
</Compile>
<Compile Update="SomeFeature\SomeControl.Designer.cs">
  <DependentUpon>SomeControl.cs</DependentUpon>
  <SubType>Designer</SubType>
</Compile>
<EmbeddedResource Update="SomeFeature\SomeControl.resx">
  <DependentUpon>SomeControl.cs</DependentUpon>
</EmbeddedResource>
<EmbeddedResource Update="SomeFeature\SomeControl.*.resx">
  <DependentUpon>SomeControl.cs</DependentUpon>
</EmbeddedResource>
```

For a form, use `Form` instead of `UserControl`:

```xml
<Compile Update="SomeFeature\SomeForm.cs">
  <SubType>Form</SubType>
</Compile>
<Compile Update="SomeFeature\SomeForm.Designer.cs">
  <DependentUpon>SomeForm.cs</DependentUpon>
  <SubType>Designer</SubType>
</Compile>
<EmbeddedResource Update="SomeFeature\SomeForm.resx">
  <DependentUpon>SomeForm.cs</DependentUpon>
  <SubType>Designer</SubType>
</EmbeddedResource>
<EmbeddedResource Update="SomeFeature\SomeForm.*.resx">
  <DependentUpon>SomeForm.cs</DependentUpon>
</EmbeddedResource>
```

Rules:

- `DependentUpon` contains only the file name, not the full relative path.
- The neutral `.resx` file depends on the root `.cs` file, not on `*.Designer.cs`.
- Localized resource files use a wildcard entry like `SomeControl.*.resx` and also depend on the root `.cs` file.
- `*.Designer.cs` must have `<SubType>Designer</SubType>`.
- Root `UserControl` files must have `<SubType>UserControl</SubType>`.
- Root form files must have `<SubType>Form</SubType>`.
- Do not use `LastGenOutput` for WinForms control/form `.resx` files. Reserve it for strongly typed resource files such as `Resources.resx` or `LocalizedStrings.resx`.
- Keep nesting entries near the other WinForms metadata entries in the project file so future moves are easy to review.

## Event Wiring

- Avoid adding new event wiring in `*.Designer.cs` when the control is being refactored toward behaviors.
- If existing designer-generated event wiring is kept, use the standard designer style:

```csharp
this.button1.Click += new System.EventHandler(this.button1_Click);
```

- For new refactored controls, prefer behavior classes and `IBehavior<TControl>` subscriptions outside the designer file.

## Manual Patch Checklist

Before finishing a manual edit to a `*.Designer.cs` file:

1. Open the file and check `BeginInit`/`EndInit` and `SuspendLayout`/`ResumeLayout` pairs.
2. Verify every `Controls.Add(...)` target is the intended parent.
3. Verify every field declared at the end is instantiated in `InitializeComponent()`.
4. Verify every `resources.ApplyResources(...)` key exists in the matching `.resx` file when localized.
5. Verify the root `.cs`, `*.Designer.cs`, neutral `.resx`, and localized `*.resx` files are nested correctly in the owning `*.csproj`.
6. Build the owning project to catch resource and designer compile errors.
