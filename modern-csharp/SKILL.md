---
name: modern-csharp
description: Modern C# style guidance for Bendex and MicroSea code changes, including primary constructors, expression-bodied members, var usage, target-typed new, lambdas, and pattern matching.
---

# Modern C# style

Use this skill when writing or refactoring C# in Bendex or MicroSea projects. This skill is for intentional code style and modernization decisions. When a specific `IDE*` diagnostic is the trigger, also use `../ide-warnings/SKILL.md` for the diagnostic-specific fix.

## Scope

- Modernize code you are already touching.
- Keep changes local to the feature, bug fix, or warning cleanup in progress.
- Do not perform broad style-only rewrites unless the user explicitly asks for that cleanup.
- Prefer the existing style in the surrounding file when it conflicts with a rule here.
- Do not modernize generated code, `*.Designer.cs`, or resource output unless the relevant specialized skill says it is safe.

## Core rules

- Use file-scoped namespaces in new C# files.
- Use primary constructors when constructor parameters are only used for initialization or dependency capture.
- Prefer `var` when the type is obvious from the right-hand side; keep explicit types when they improve readability or the right-hand side is not enough context.
- Prefer target-typed `new()` when the target type is visible and readability remains clear.
- Prefer object and collection initializers over repeated assignment after construction.
- Prefer null-propagation, null-coalescing, and throw expressions when they make the intent clearer.
- Prefer pattern matching over separate type checks and casts.
- Prefer switch expressions for simple value mapping.
- Prefer expression-bodied members for single-expression properties, accessors, operators, conversions, lambdas, and short local functions.
- For ordinary methods, use an expression body only when it stays readable and does not hide important control flow.
- Write calls, constructors, and primary constructors with multiple arguments as a vertical argument list.
- Keep Allman braces for block-bodied code, including single-line blocks.

## Services

Services in this project are commonly resolved by dependency injection and must remain visible to tooling that prunes unused types.

- Add `[DoNotPruneType]` to service classes that are resolved through dependency injection.
- Implement the service or base interface used for registration and resolution.
- Keep the service interface visible in the declaration instead of relying only on concrete type registration.

## Primary constructors

Use a primary constructor when it removes boilerplate without making lifetime or validation behavior less obvious.

Good candidates:

```csharp
[DoNotPruneType]
public sealed class CustomerService(
    IRepository repository,
    ILogger<CustomerService> logger)
    : ICustomerService
{
    public Customer Load(int id)
    {
        logger.LogDebug("Loading customer {CustomerId}", id);
        return repository.Get(id);
    }
}
```

Keep a normal constructor when:

- Constructor logic has meaningful branching, validation, or exception messages.
- Several overloads delegate to one canonical constructor.
- XML documentation on constructor parameters is important and would become less readable.
- The type is serialized, reflected, designer-created, or framework-created and constructor shape is part of a contract.

If a constructor parameter is stored in a field because the field name improves readability, keep the field. Otherwise, use the primary constructor parameter directly.

## Argument lists

Write multiple arguments top-to-bottom instead of left-to-right. This keeps diffs stable and avoids long lines.

Prefer:

```csharp
var result = factory.Create(
    customerId,
    machineId,
    cancellationToken);
```

Avoid:

```csharp
var result = factory.Create(customerId, machineId, cancellationToken);
```

## Expression bodies and lambdas

Prefer expression-bodied form for one-expression members:

```csharp
public bool IsEnabled => _settings.Enabled;

public string GetDisplayName() => $"{FirstName} {LastName}";

items.Select(item => item.Name);
```

Keep a block body when:

- The body has more than one statement.
- The expression needs comments to be understood.
- Debugging, tracing, or exception handling is clearer with statements.
- The expression would wrap awkwardly or obscure the domain operation.

For lambdas, prefer expression form for a single returned expression. Use a block lambda when there are multiple statements, logging, tracing, local variables, or deliberate side effects.

## Implicit typing

C# methods require explicit return types. Do not invent implicit method return types. Use implicit typing for locals and lambdas where the language supports it and the result remains obvious.

Prefer:

```csharp
var result = new MachineState(); // or: MachineState result = new();
Func<int, bool> isValid = value => value > 0;
```

Avoid:

```csharp
var result = GetValue();
```

when `GetValue()` does not make the type or domain role clear.

When returning a newly constructed value whose type is the same as the method return type, use target-typed construction:

```csharp
public MachineState CreateState()
{
    return new(
        machineId,
        settings);
}
```

Avoid repeating the return type:

```csharp
public MachineState CreateState()
{
    return new MachineState(
        machineId,
        settings);
}
```

## Compatibility boundaries

- Check the target framework and language version before using newer syntax such as collection expressions, list patterns, required members, or raw string literals.
- Be careful in `net472` and mixed-framework projects where analyzers may allow syntax that older tooling, generators, or designers handle poorly.
- Do not change public API shape only for style.
- Do not change serialization names, constructor binding, reflection behavior, dependency injection registration, or XAML/WinForms designer activation as a side effect of modernization.

## Verification

- Build the smallest relevant project or solution after modernization.
- Run focused tests when behavior could have changed.
- Run `.\BuildScripts\Update-FileLineEndings.ps1 -Git` after editing files in Bendex or MicroSea repositories.
