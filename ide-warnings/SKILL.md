---
name: ide-warnings
description: .NET IDE code style warning meanings and examples
---

# .NET code-style warnings

Use this skill when the build reports enabled IDE* diagnostics.

### .NET code-style diagnostics (`IDE`)

### `IDE0001` - Simplify name

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: fully qualified name is used when an import makes it unnecessary.
- Fix: simplify the name.

### `IDE0002` - Simplify member access

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `this.member` or type qualification is unnecessary for access.
- Fix: simplify member access.

### `IDE0003` - Remove this or Me qualification

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `this._value` where qualification is not required by style.
- Fix: remove `this.`.

### `IDE0004` - Remove unnecessary cast

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `(string)name` where `name` is already string.
- Fix: remove the unnecessary cast.

### `IDE0005` - Remove unnecessary using directive

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: unused `using System.Text;`.
- Fix: remove the unused using.

### `IDE0007` - Use var instead of explicit type

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `Customer customer = GetCustomer();` where style prefers `var`.
- Fix: use `var customer = GetCustomer();`.

### `IDE0009` - Add this or Me qualification

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `_value` where style requires `this._value`.
- Fix: add the configured qualification.

### `IDE0010` - Add missing cases to switch statement

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: switch statement omits enum cases.
- Fix: add missing cases or a default case.

### `IDE0011` - Add braces

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `if (ready) Run();`.
- Fix: add braces.

### `IDE0016` - Use throw expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `if (x is null) throw ...; return x;`.
- Fix: use a throw expression when it improves clarity.

### `IDE0017` - Use object initializer

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: create object then assign simple properties one by one.
- Fix: use an object initializer.

### `IDE0018` - Inline variable declaration

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: declare an out variable before the call.
- Fix: inline the declaration in the `out` argument.

### `IDE0019` - Use pattern matching

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `var c = o as Control; if (c != null)`.
- Fix: use `if (o is Control c)`.

### `IDE0021` - Use expression body for constructors

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: constructor body only delegates one expression where expression body is preferred.
- Fix: use an expression-bodied constructor if style allows.

### `IDE0022` - Use expression body for methods

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: method body only returns one expression.
- Fix: use expression body if style requires.

### `IDE0023` - Use expression body for conversion operators

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: conversion operator uses a trivial block body.
- Fix: use expression body if style requires.

### `IDE0024` - Use expression body for operators

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: operator uses a trivial block body.
- Fix: use expression body if style requires.

### `IDE0025` - Use expression body for properties

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: property getter only returns one expression.
- Fix: use expression-bodied property if style requires.

### `IDE0026` - Use expression body for indexers

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: indexer getter only returns one expression.
- Fix: use expression-bodied indexer if style requires.

### `IDE0027` - Use expression body for accessors

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: accessor only returns or assigns one expression.
- Fix: use expression-bodied accessor if style requires.

### `IDE0028` - Use collection initializer

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: create collection then call `Add` repeatedly.
- Fix: use collection initializer.

### `IDE0029` - Use coalesce expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `x == null ? fallback : x`.
- Fix: use `x ?? fallback`.

### `IDE0030` - Use coalesce expression for nullable

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: nullable value manually checked before fallback.
- Fix: use a coalesce expression.

### `IDE0031` - Use null propagation

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `x == null ? null : x.Name`.
- Fix: use `x?.Name`.

### `IDE0032` - Use auto property

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: property only wraps a backing field with no logic.
- Fix: use an auto-property.

### `IDE0033` - Use explicitly provided tuple name

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: tuple field name is repeated unnecessarily.
- Fix: rely on the explicitly provided tuple name.

### `IDE0034` - Simplify default expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `default(string)`.
- Fix: use `default` where target type is clear.

### `IDE0035` - Remove unreachable code

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: code remains after an unconditional return/throw.
- Fix: remove unreachable code.

### `IDE0036` - Order modifiers

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `static public`.
- Fix: order modifiers consistently, e.g. `public static`.

### `IDE0037` - Use inferred member name

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: anonymous object repeats obvious member name.
- Fix: use inferred member name.

### `IDE0039` - Use local function

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: lambda assigned only for local reuse.
- Fix: use a local function where clearer.

### `IDE0041` - Use is null check

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `object.ReferenceEquals(value, null)`.
- Fix: use `value is null`.

### `IDE0042` - Deconstruct variable declaration

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: assign tuple fields manually after tuple-returning call.
- Fix: use deconstruction.

### `IDE0045` - Use conditional expression for assignment

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `if` assigns one of two values to the same variable.
- Fix: use a conditional expression when readable.

### `IDE0046` - Use conditional expression for return

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `if` returns one of two values.
- Fix: use a conditional expression when readable.

### `IDE0049` - Use language keywords instead of framework type names

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `System.String`.
- Fix: use `string`.

### `IDE0050` - Convert anonymous type to tuple

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: anonymous type is used like a tuple.
- Fix: use a tuple when names/types fit.

### `IDE0051` - Remove unused private member

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: private method is never used.
- Fix: remove it or call it intentionally.

### `IDE0052` - Remove unread private member

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: private field is written but never read.
- Fix: remove it or read it intentionally.

### `IDE0053` - Use expression body for lambdas

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: lambda block only returns one expression.
- Fix: use expression-bodied lambda.

### `IDE0054` - Use compound assignment

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `x = x + 1`.
- Fix: use `x += 1`.

### `IDE0056` - Use index operator

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `items[items.Length - 1]`.
- Fix: use `items[^1]`.

### `IDE0057` - Use range operator

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `text.Substring(1, text.Length - 2)`.
- Fix: use range syntax when readable.

### `IDE0058` - Remove unnecessary expression value

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `Compute();` where the returned value is intentionally ignored but analyzer expects discard.
- Fix: assign to discard or remove the call if unnecessary.

### `IDE0059` - Remove unnecessary assignment

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: assigned value is overwritten before being read.
- Fix: remove the assignment.

### `IDE0061` - Use expression body for local functions

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: local function block only returns one expression.
- Fix: use expression body if style requires.

### `IDE0063` - Use simple using statement

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `using (...) { ... }` where simple using is preferred.
- Fix: use `using var`.

### `IDE0070` - Use System.HashCode

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: hand-written hash code combination.
- Fix: use `HashCode.Combine`.

### `IDE0071` - Simplify interpolation

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: interpolation contains unnecessary `.ToString()`.
- Fix: simplify the interpolation.

### `IDE0072` - Add missing cases to switch expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: switch expression omits enum values.
- Fix: add arms for missing values.

### `IDE0074` - Use compound assignment

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `x = x && y`.
- Fix: use compound assignment where valid.

### `IDE0075` - Simplify conditional expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `condition ? true : false`.
- Fix: use `condition`.

### `IDE0080` - Remove unnecessary suppression operator

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `value!` where nullability analysis already proves non-null.
- Fix: remove `!`.

### `IDE0082` - Convert typeof to nameof

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `typeof(Customer).Name` for a symbol name.
- Fix: use `nameof(Customer)`.

### `IDE0090` - Use new expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `new Customer()` when target type is clear.
- Fix: use target-typed `new()` if project style allows.

### `IDE0100` - Remove unnecessary equality operator

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: unnecessary `== true` or `== false`.
- Fix: simplify the boolean expression.

### `IDE0110` - Remove unnecessary discard

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `_ = value;` discard is unnecessary.
- Fix: remove the discard.

### `IDE0120` - Simplify LINQ expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: verbose LINQ chain can be simplified.
- Fix: apply the simpler LINQ form suggested by the analyzer.

### `IDE0130` - Namespace does not match folder structure

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: namespace does not match the folder path.
- Fix: move the file or change the namespace.

### `IDE0150` - Prefer null check over type check

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `x is string ? x != null : false` style checks.
- Fix: prefer direct null checks over type checks when appropriate.

### `IDE0160` - Use block-scoped namespace

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: file-scoped namespace is used where block-scoped is configured.
- Fix: use block-scoped namespace.

### `IDE0161` - Use file-scoped namespace

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: block-scoped namespace is used where file-scoped is configured.
- Fix: use file-scoped namespace.

### `IDE0180` - Use tuple swap

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: swap uses a temporary variable.
- Fix: use tuple swap `(a, b) = (b, a)`.

### `IDE0200` - Remove unnecessary lambda expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: lambda only calls another method with same arguments.
- Fix: use method group conversion.

### `IDE0210` - Convert to top-level statements

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: Program class boilerplate where top-level statements are preferred.
- Fix: convert to top-level statements if appropriate.

### `IDE0211` - Convert from top-level statements

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: top-level statements where explicit Program is preferred.
- Fix: convert to Program.Main if configured.

### `IDE0220` - Add explicit cast in foreach loop

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: foreach conversion is implicit and unclear.
- Fix: add an explicit cast in the foreach source.

### `IDE0230` - Use UTF-8 string literal

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: UTF-8 byte array literal built from string at runtime.
- Fix: use UTF-8 string literal when available.

### `IDE0240` - Nullable directive is unnecessary

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: nullable directive repeats the project default.
- Fix: remove unnecessary directive.

### `IDE0241` - Nullable directive is unnecessary

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: nullable directive is redundant for the current context.
- Fix: remove unnecessary directive.

### `IDE0270` - Use coalesce throw expression

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: null guard throws in a separate statement.
- Fix: use `value ?? throw ...` when readable.

### `IDE0290` - Use primary constructor

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: constructor only assigns parameters to members.
- Fix: use a primary constructor if project style allows.

### `IDE0300` - Use collection expression for array

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `new int[] { 1, 2 }` where collection expression is preferred.
- Fix: use `[1, 2]`.

### `IDE0301` - Use collection expression for empty collection

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: `Array.Empty<int>()` where collection expression is preferred.
- Fix: use `[]` where target type is clear.

### `IDE0302` - Use collection expression for stackalloc

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: stackalloc initializer can use collection expression.
- Fix: use collection expression syntax.

### `IDE0303` - Use collection expression for Create method

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: collection factory call can use collection expression.
- Fix: use collection expression syntax.

### `IDE0304` - Use collection expression for builder

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: builder pattern collection creation can use collection expression.
- Fix: use collection expression syntax.

### `IDE0305` - Use collection expression for fluent calls

What it flags: The .NET code-style analyzer found code that differs from the configured style or can be simplified.

Example:
- Bad: fluent collection creation can use collection expression.
- Fix: use collection expression syntax.
