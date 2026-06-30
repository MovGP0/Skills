---
name: csharp-compiler-warnings
description: Non-nullability C# compiler warning meanings and examples
---

# C# compiler warnings

## C# compiler diagnostics (`CS`)

Use this skill for enabled C# compiler diagnostics that are not nullable-reference warnings. For nullable `CS8xxx` warnings, use `../nullability-warnings/SKILL.md`.

### `CS0162` - Unreachable code detected

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: code after `return`, `throw`, or an always-false branch.
- Fix: remove the unreachable statement or correct the control flow.

### `CS0168` - Variable is declared but never used

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: `catch (Exception ex) { LogFailure(); }` without using `ex`.
- Fix: remove the variable or use it, for example in logging.

### `CS0219` - Variable is assigned but its value is never used

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: `var result = Calculate();` and `result` is never read.
- Fix: remove the assignment or use the value.

### `CS0628` - New protected member declared in sealed type

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: `protected void M()` in a sealed class.
- Fix: make the member private or unseal the class if inheritance is intended.

### `CS1696` - Single-line comment or end-of-line expected

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: malformed preprocessor or comment syntax near a directive.
- Fix: correct the directive/comment so the compiler can parse the line.

### `CS1998` - Async method lacks await operators

What it flags: The C# compiler reported code that is unreachable, unused, malformed, or inconsistent with language rules.

Example:
- Bad: `async Task SaveAsync() { Save(); }` with no `await`.
- Fix: remove `async` and return a completed task, or await real async work.
