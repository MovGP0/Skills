---
name: xunit-warnings
description: xUnit analyzer warning meanings and examples
---

# xUnit warnings

Use this skill when the build reports enabled xUnit* diagnostics.

### xUnit diagnostics

### `xUnit1013` - Public method should be marked as test

What it flags: The analyzer reported code that violates the enabled project warning policy.

Example:
- Bad: public test-like method is not marked with `[Fact]` or `[Theory]`.
- Fix: add the correct xUnit attribute or make the helper non-public.
