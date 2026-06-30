---
name: nuget-warnings
description: NuGet restore warning meanings and examples
---

# NuGet warnings

Use this skill when restore reports enabled NU* diagnostics.

### NuGet diagnostics (`NU`)

### `NU1405` - Package downgrade or dependency graph inconsistency

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: restore detects an inconsistent package graph or downgrade condition.
- Fix: align direct and transitive package versions.

### `NU1504` - Duplicate PackageReference items

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: same package appears in multiple `PackageReference` items.
- Fix: keep one reference and centralize the version.

### `NU1603` - Dependency resolved to approximate best match

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: requested dependency version is unavailable, so NuGet picks an approximate match.
- Fix: request an available version or update the dependency range.

### `NU1604` - Package dependency does not contain an inclusive lower bound

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: dependency lacks a lower bound.
- Fix: specify an inclusive minimum version.

### `NU1605` - Detected package downgrade

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: direct or transitive package downgrade is detected.
- Fix: reference the higher compatible version directly or align packages.

### `NU1608` - Package version outside dependency constraint

What it flags: NuGet restore reported a package graph, version, or dependency-range issue.

Example:
- Bad: resolved package version is outside another package constraint.
- Fix: choose package versions with compatible dependency ranges.
