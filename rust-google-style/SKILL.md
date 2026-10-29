---
name: rust-google-style
description: Write, review, and refactor Rust code with Google's Rust Style Guide. Use for Rust style reviews, API design, imports, ownership, error handling, traits, naming, documentation, unsafe code, or explicit requests to follow Google Rust guidelines.
license: MIT
metadata:
  source: https://google.github.io/styleguide/rustguide.html
  specification: https://agentskills.io/specification
---

# Rust Google Style

Use this skill for Rust implementation work and style reviews. For a review request, report findings before you change files. For an implementation request, apply the relevant rules within the requested scope.

## Workflow

1. Read the repository instructions. Inspect the affected code, callers, tests, Cargo manifests, toolchain file, formatter configuration, and lint configuration. Identify the minimum supported Rust version and the build system.
2. Identify the API boundary. Record whether the change affects application code, a reusable library, or an API used outside the repository. Check compatibility before you change a public signature or attribute.
3. Open the relevant source links below. Read each rule with its rationale and exceptions. For a full style audit, read the complete guide. The checklist is a starting point, not a complete copy of the guide.
4. Apply explicit user and repository instructions first. Apply Chromium-only layout, import, async, and thread rules only in Chromium. Apply Fuchsia mutex rules only in Fuchsia.
5. For each finding, identify the location, the applicable rule, the effect on the code, and the smallest useful correction. Separate a correctness defect from a style preference. Check exceptions before you report a violation.
6. Make only the changes needed for the task. Preserve unrelated edits. Do not add dependencies, change the toolchain, enable nightly formatter options, or add stricter lint policies solely to satisfy this skill.
7. Run the applicable checks. Inspect the final diff for changes to behavior, public contracts, generated files, and unrelated formatting.

If the source is unavailable, use the checklist for an initial review. State that the full guide was not checked. Do not claim complete compliance or invent the missing rules.

## Initial checklist

- Put implementations in leaf modules named for their main type.
- Avoid glob imports except documented cases; group imports by module.
- Prefer borrowing; justify shared ownership and deep copies.
- Accept flexible borrowed inputs; weigh iterator and generic APIs against application simplicity.
- Use enums for unclear flags, newtypes for distinct meanings, and named fields.
- Choose `Option`, `Result`, or panic according to the contract.
- Prefer standard traits and derives; add abstractions when needed.
- Document public contracts, panic conditions, and unsafe invariants.
- Isolate necessary unsafe code; explain safety and technical need.
- Prefer matching to `unwrap`; use `expect` for justified invariant failures.
- Check API evolution, accessor names, macros, and readability in the source.
- Use repository formatting; limit formatting exemptions.

## Source sections

The [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html) is the source for the checklist. Open the links for the areas touched by the task, including rules omitted from the checklist.

- [Applicability](https://google.github.io/styleguide/rustguide.html#background) and [API context](https://google.github.io/styleguide/rustguide.html#apply-api-design-rules-in-context)
- [Modules and imports](https://google.github.io/styleguide/rustguide.html#code-organization)
- [Formatting](https://google.github.io/styleguide/rustguide.html#code-formatting-and-aesthetics)
- [Ownership](https://google.github.io/styleguide/rustguide.html#ownership-and-borrowing)
- [Signatures and errors](https://google.github.io/styleguide/rustguide.html#function-inputs-and-outputs)
- [Data models](https://google.github.io/styleguide/rustguide.html#types)
- [Traits](https://google.github.io/styleguide/rustguide.html#traits)
- [Concurrency](https://google.github.io/styleguide/rustguide.html#concurrency)
- [Macros](https://google.github.io/styleguide/rustguide.html#macros)
- [Naming](https://google.github.io/styleguide/rustguide.html#naming)
- [Documentation](https://google.github.io/styleguide/rustguide.html#when-and-how-to-write-documentation)
- [Safety and API evolution](https://google.github.io/styleguide/rustguide.html#other-rust-features)
- [Implementation](https://google.github.io/styleguide/rustguide.html#implementation-concerns)
- [Tests](https://google.github.io/styleguide/rustguide.html#use-the-right-per-codebase-test-framework)

## Validation

Use the repository's check commands and supported feature sets. For a Cargo project without custom commands, select from these commands. Replace `PACKAGE` with the affected package name.

```sh
cargo fmt --all -- --check
cargo check --package PACKAGE
cargo test --package PACKAGE
cargo clippy --package PACKAGE --all-targets
```

Run documentation tests when examples change. Use the required target and features for conditional code. Do not enable every feature by default; some feature combinations are incompatible. Use the repository's build and test tools for a project that does not use Cargo.

A formatter or Clippy pass does not prove that an API follows the guide. Review the applicable design rules separately. Report existing failures and checks that could not run. Do not claim that unexecuted checks passed.

## Report

State what changed and why. Include the validation result and any remaining limitation. For review findings, include a file location, a source link, the relevant context or exception, and a proposed correction.

Example review format:

> `src/example.rs:42`: Describe the observed code and its effect. Link the applicable rule. Explain why its exceptions do not apply, then propose a focused change.

When a repository rule differs from the guide, state which rule you followed. When no applicable finding remains, say so and identify the scope reviewed.

## Skill format

This skill uses the [Agent Skills specification](https://agentskills.io/specification). Its metadata supports discovery; its instructions define the workflow; its source links provide details when needed.
