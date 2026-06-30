---
name: compiler-warnings
description: Routing guide for enabled compiler and analyzer warnings in this Bendex solution
---

# Compiler warning routing

Use this skill first when a build warning appears. It routes each enabled warning family to the dedicated skill that contains the meaning and examples.

The current solution warning policy is derived from `Machines.slnx`, `Props\Analyzers.props`, `.editorconfig`, and project `WarningsAsErrors` settings.

## Diagnostic family skills

- `RCS*`: use `../rcs-warnings/SKILL.md`.
- `CA*`: use `../code-analysis-warnings/SKILL.md`.
- `CS8xxx` nullable warnings: use `../nullability-warnings/SKILL.md`.
- Other `CS*` compiler warnings: use `../csharp-compiler-warnings/SKILL.md`.
- `IDE*`: use `../ide-warnings/SKILL.md`.
- `MSB*`: use `../msbuild-warnings/SKILL.md`.
- `NU*`: use `../nuget-warnings/SKILL.md`.
- `xUnit*`: use `../xunit-warnings/SKILL.md`.

## Active analyzer packages

Projects that import `Props\Analyzers.props` get these analyzer packages:

- `Bendex.Analyzers`
- `Microsoft.CodeAnalysis.NetAnalyzers`
- `Microsoft.CodeAnalysis.CSharp.CodeStyle`
- `Roslynator.Analyzers`
- `Roslynator.Formatting.Analyzers`
- `Roslynator.CodeAnalysis.Analyzers`
- `MessagePipe.Analyzer`
- `Microsoft.CodeAnalysis.Metrics`

## Fixing policy

- Prefer fixing the warning over suppressing it.
- Keep nullability fixes in the `nullability` skill and analyzer-specific fixes in the matching family skill.
- Suppress only when the diagnostic is wrong for the local context and the project already has an appropriate suppression pattern.
