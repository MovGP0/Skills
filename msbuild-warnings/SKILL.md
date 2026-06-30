---
name: msbuild-warnings
description: MSBuild warning meanings and examples
---

# MSBuild warnings

Use this skill when the build reports enabled MSB* diagnostics.

### MSBuild diagnostics (`MSB`)

### `MSB3245` - Could not resolve assembly reference

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: project references an assembly path/name MSBuild cannot resolve.
- Fix: fix the reference, package, hint path, or target framework.

### `MSB3270` - Processor architecture mismatch

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: AnyCPU project references x86-only or x64-only assemblies.
- Fix: align platform targets or references.

### `MSB3277` - Found conflicts between different versions of an assembly

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: different projects require different versions of the same assembly.
- Fix: align package versions or binding redirects.

### `MSB3568` - Duplicate item or resource name in build input

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: duplicate resource or generated item names collide.
- Fix: give items unique logical names or remove duplicates.

### `MSB3884` - Rule set file not found or invalid

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: project references a missing ruleset file.
- Fix: restore the ruleset path or remove/update the property.

### `MSB4011` - Project import was ignored because it was already imported

What it flags: MSBuild reported a build configuration, reference, import, or resource issue.

Example:
- Bad: the same props/targets file is imported twice.
- Fix: remove the duplicate import or guard it.
