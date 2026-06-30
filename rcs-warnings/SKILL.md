---
name: rcs-warnings
description: Roslynator RCS analyzer warning meanings and examples
---

# Roslynator analyzer warnings

Use this skill when the build reports an RCS* diagnostic from Roslynator analyzers.

## Roslynator analyzers (RCS)

### `RCS0003` - Add blank line after using directive list

What it flags: Roslynator reports code that violates this rule: Add blank line after using directive list.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0003

Example:
- Bad: `using System;` is followed immediately by `namespace App;`.
- Fix: add a blank line between the using list and the namespace/type.

### `RCS0041` - Remove new line between 'if' keyword and 'else' keyword

What it flags: Roslynator reports code that violates this rule: Remove new line between 'if' keyword and 'else' keyword.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0041

Example:
- Bad: `}` and `else` are separated by an extra newline.
- Fix: keep `else` directly after the closing brace according to project style.

### `RCS0044` - Use carriage return + linefeed as new line

What it flags: Roslynator reports code that violates this rule: Use carriage return + linefeed as new line.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0044

Example:
- Bad: file uses LF-only line endings.
- Fix: save the file with CRLF line endings.

### `RCS0046` - Use spaces instead of tab

What it flags: Roslynator reports code that violates this rule: Use spaces instead of tab.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0046

Example:
- Bad: indentation contains tab characters.
- Fix: replace tabs with spaces.

### `RCS0058` - Normalize whitespace at the end of a file

What it flags: Roslynator reports code that violates this rule: Normalize whitespace at the end of a file.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0058

Example:
- Bad: trailing spaces or extra whitespace at the end of a file.
- Fix: remove end-of-file whitespace and keep one final newline.

### `RCS0063` - Remove unnecessary blank line

What it flags: Roslynator reports code that violates this rule: Remove unnecessary blank line.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS0063

Example:
- Bad: an extra blank line splits code where the style expects none.
- Fix: remove the unnecessary blank line.

### `RCS1001` - Add braces (when expression spans over multiple lines)

What it flags: Roslynator reports code that violates this rule: Add braces (when expression spans over multiple lines).

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1001

Example:
- Bad: a multiline `if` body is written without braces.
- Fix: add braces when the expression spans multiple lines.

### `RCS1003` - Add braces to if-else (when expression spans over multiple lines)

What it flags: Roslynator reports code that violates this rule: Add braces to if-else (when expression spans over multiple lines).

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1003

Example:
- Bad: multiline `if`/`else` branches omit braces.
- Fix: add braces to both branches.

### `RCS1013` - Use predefined type

What it flags: Roslynator reports code that violates this rule: Use predefined type.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1013

Example:
- Bad: `System.String value` in C# code.
- Fix: use predefined aliases such as `string`, `int`, and `bool`.

### `RCS1016` - Use block body or expression body

What it flags: Roslynator reports code that violates this rule: Use block body or expression body.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1016

Example:
- Bad: member body form differs from configured style.
- Fix: convert between block body and expression body as requested.

### `RCS1019` - Order modifiers

What it flags: Roslynator reports code that violates this rule: Order modifiers.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1019

Example:
- Bad: `static public`.
- Fix: use standard order, e.g. `public static`.

### `RCS1034` - Remove redundant 'sealed' modifier

What it flags: Roslynator reports code that violates this rule: Remove redundant 'sealed' modifier.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1034

Example:
- Bad: redundant `sealed` modifier is present.
- Fix: remove `sealed` where Roslynator reports it redundant.

### `RCS1035` - Remove redundant comma in initializer

What it flags: Roslynator reports code that violates this rule: Remove redundant comma in initializer.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1035

Example:
- Bad: `new[] { 1, 2, }` where style disallows the comma.
- Fix: remove the redundant comma.

### `RCS1037` - Remove trailing white-space

What it flags: Roslynator reports code that violates this rule: Remove trailing white-space.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1037

Example:
- Bad: a line ends with spaces before the newline.
- Fix: remove trailing whitespace.

### `RCS1038` - Remove empty statement

What it flags: Roslynator reports code that violates this rule: Remove empty statement.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1038

Example:
- Bad: a stray `;` creates an empty statement.
- Fix: remove the empty statement.

### `RCS1039` - Remove argument list from attribute

What it flags: Roslynator reports code that violates this rule: Remove argument list from attribute.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1039

Example:
- Bad: `[Obsolete()]` when no arguments are supplied.
- Fix: use `[Obsolete]`.

### `RCS1044` - Remove original exception from throw statement

What it flags: Roslynator reports code that violates this rule: Remove original exception from throw statement.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1044

Example:
- Bad: `catch (Exception ex) { throw ex; }`.
- Fix: use `throw;` to preserve the stack trace.

### `RCS1047` - Non-asynchronous method name should not end with 'Async'

What it flags: Roslynator reports code that violates this rule: Non-asynchronous method name should not end with 'Async'.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1047

Example:
- Bad: `public void SaveAsync()` returns `void`.
- Fix: return `Task` or rename the method.

### `RCS1055` - Unnecessary semicolon at the end of declaration

What it flags: Roslynator reports code that violates this rule: Unnecessary semicolon at the end of declaration.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1055

Example:
- Bad: `public string Name { get; set; };`.
- Fix: remove the unnecessary semicolon.

### `RCS1059` - Avoid locking on publicly accessible instance

What it flags: Roslynator reports code that violates this rule: Avoid locking on publicly accessible instance.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1059

Example:
- Bad: `lock (this)` or `lock (typeof(Foo))`.
- Fix: lock on a private readonly object.

### `RCS1060` - Declare each type in separate file

What it flags: Roslynator reports code that violates this rule: Declare each type in separate file.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1060

Example:
- Bad: one file declares unrelated top-level types.
- Fix: move each top-level type to its own file.

### `RCS1075` - Avoid empty catch clause that catches System. Exception

What it flags: Roslynator reports code that violates this rule: Avoid empty catch clause that catches System. Exception.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1075

Example:
- Bad: `catch (Exception) { }`.
- Fix: handle, log, rethrow, or remove the catch.

### `RCS1091` - Remove empty region

What it flags: Roslynator reports code that violates this rule: Remove empty region.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1091

Example:
- Bad: `#region Old code` contains no members.
- Fix: remove the empty region.

### `RCS1093` - File contains no code

What it flags: Roslynator reports code that violates this rule: File contains no code.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1093

Example:
- Bad: a `.cs` file contains only comments or whitespace.
- Fix: remove the file or add the intended code.

### `RCS1094` - Declare using directive on top level

What it flags: Roslynator reports code that violates this rule: Declare using directive on top level.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1094

Example:
- Bad: `using System;` is inside a namespace when top-level usings are expected.
- Fix: move using directives to the top level.

### `RCS1102` - Make class static

What it flags: Roslynator reports code that violates this rule: Make class static.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1102

Example:
- Bad: a class contains only static members but is not static.
- Fix: mark the class `static`.

### `RCS1110` - Declare type inside namespace

What it flags: Roslynator reports code that violates this rule: Declare type inside namespace.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1110

Example:
- Bad: top-level type is declared outside a namespace.
- Fix: put the type in the correct namespace.

### `RCS1145` - Remove redundant 'as' operator

What it flags: Roslynator reports code that violates this rule: Remove redundant 'as' operator.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1145

Example:
- Bad: `var text = value as string;` where `value` is already `string`.
- Fix: remove the redundant `as` conversion.

### `RCS1172` - Use 'is' operator instead of 'as' operator

What it flags: Roslynator reports code that violates this rule: Use 'is' operator instead of 'as' operator.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1172

Example:
- Bad: `var c = o as Control; if (c != null) ...`.
- Fix: use `if (o is Control c) ...`.

### `RCS1211` - Remove unnecessary 'else'

What it flags: Roslynator reports code that violates this rule: Remove unnecessary 'else'.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1211

Example:
- Bad: `if (done) { return; } else { Work(); }`.
- Fix: remove the unnecessary `else`.

### `RCS1225` - Make class sealed

What it flags: Roslynator reports code that violates this rule: Make class sealed.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1225

Example:
- Bad: class can be inherited although no inheritance is intended.
- Fix: mark the class `sealed` when appropriate.

### `RCS1242` - Do not pass non-read-only struct by read-only reference

What it flags: Roslynator reports code that violates this rule: Do not pass non-read-only struct by read-only reference.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1242

Example:
- Bad: `void M(in MutableStruct value)` for a non-readonly struct.
- Fix: pass by value or make the struct readonly if intended.

### `RCS1259` - Remove empty syntax

What it flags: Roslynator reports code that violates this rule: Remove empty syntax.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1259

Example:
- Bad: empty braces, argument list, or similar empty syntax remains.
- Fix: remove the empty syntax.

### `RCS1260` - Add/remove trailing comma

What it flags: Roslynator reports code that violates this rule: Add/remove trailing comma.

Documentation: https://josefpihrt.github.io/docs/roslynator/analyzers/RCS1260

Example:
- Bad: initializer comma style differs from formatter settings.
- Fix: add or remove the trailing comma to match the rule.
