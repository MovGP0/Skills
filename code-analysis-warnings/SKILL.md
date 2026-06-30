---
name: code-analysis-warnings
description: Microsoft code analysis CA warning meanings and examples
---

# Code analysis warnings

Use this skill when the build reports enabled CA* diagnostics.

### Code analysis diagnostics (`CA`)

### `CA1069` - Enums should not have duplicate values

What it flags: The enum defines two names with the same constant value without an intentional alias pattern.

Example:
- Bad: `enum Status { New = 0, Created = 0 }`.
- Fix: remove the duplicate value or document intentional aliases with a clear naming pattern.

### `CA1501` - Avoid excessive inheritance

What it flags: A type has an inheritance chain that is too deep to maintain comfortably.

Example:
- Bad: `ScreenEditor : EditorBase : ControlBase : FrameworkBase : ...`.
- Fix: flatten the hierarchy or move behavior into composed services.

### `CA1502` - Avoid excessive complexity

What it flags: A method has high cyclomatic complexity.

Example:
- Bad: one method has many nested `if`, `switch`, and loop branches.
- Fix: split decision logic into smaller named methods or strategies.

### `CA1505` - Avoid unmaintainable code

What it flags: A type or assembly has a high maintainability risk.

Example:
- Bad: a class grows into a large mixed-responsibility workflow.
- Fix: split responsibilities and reduce complexity before adding more behavior.

### `CA1506` - Avoid excessive class coupling

What it flags: A type or method is coupled to too many other types.

Example:
- Bad: one service directly references many unrelated concrete types.
- Fix: introduce narrower abstractions or move orchestration to focused collaborators.

### `CA1822` - Mark members as static

What it flags: An instance member does not use instance state and can be static.

Example:
- Bad: `public int Count() => 1;` in an instance class without using instance members.
- Fix: mark it `static` or use actual instance state.

### `CA2002` - Do not lock on objects with weak identity

What it flags: Code locks on a type, string, or other object with weak identity.

Example:
- Bad: `lock (typeof(Cache))` or `lock ("global")`.
- Fix: lock on a private readonly object owned by the class.

### `CA2011` - Avoid infinite recursion in property accessors

What it flags: A property accessor recursively reads or writes the same property.

Example:
- Bad: `set { Count = value; }` inside the `Count` property.
- Fix: assign the backing field: `_count = value;`.

### `CA2211` - Non-constant fields should not be visible

What it flags: A visible static field is mutable and can be changed globally.

Example:
- Bad: `public static List<string> Names;`.
- Fix: expose a property with controlled mutation or make the field readonly/private.
