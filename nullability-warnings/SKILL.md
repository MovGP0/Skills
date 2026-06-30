---
name: nullability-warnings
description: How to fix enabled C# nullable reference type compiler warnings (CS8xxx)
---

# Nullable compiler warnings

Use this skill when the build reports nullable-reference diagnostics such as `CS8602`, `CS8618`, `CS8625`, or nullable contract mismatches on overrides, interfaces, delegates, partial methods, and attributes.

Source reference: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/nullable-warnings
Resolution guide: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/common-tasks/resolve-warnings

## Fixing strategy

- Prefer making the nullability contract true over suppressing the warning. The goal is to make the code null-handling intent explicit.
- First classify the expression null-state: not-null means safe to use; maybe-null needs a check, annotation, initialization, or contract change.
- Add a guard clause, `is not null` pattern, `?.`, `??`, or `??=` when the warning is caused by dereferencing or passing a maybe-null value.
- Add or remove `?` when the API contract is wrong. Use `?` when missing data is a valid domain state; keep the type non-nullable when callers may rely on a value.
- Use nullable static-analysis attributes such as `[NotNullWhen]`, `[NotNullIfNotNull]`, `[MemberNotNull]`, and `[DoesNotReturn]` when helper methods change null-state in a way the compiler cannot infer.
- Initialize non-nullable members through constructor parameters, primary constructors, `required` init properties, or a meaningful declaration default. Do not invent sentinel defaults like `"N/A"` just to silence `CS8618`.
- Verify the project nullable setting when warnings look inconsistent. In this repo, `Directory.Build.props` enables nullable with `<Nullable>enable</Nullable>`.
- Use the null-forgiving operator `!` only when a local invariant is already guaranteed and cannot be expressed cleanly to the compiler.
- For overrides, interface implementations, delegates, and partial methods, align the implementation with the contract instead of changing only the implementation.

## Common groups

- Maybe-null dereference: `CS8602`, `CS8670`.
- Maybe-null assignment, return, argument, throw, or unboxing: `CS8597`, `CS8600`, `CS8601`, `CS8603`, `CS8604`, `CS8605`, `CS8625`, `CS8629`.
- Non-null initialization: `CS8618`.
- Contract mismatch on overrides, interfaces, delegates, partial methods, generics, and attributes: `CS8607`-`CS8624`, `CS8631`, `CS8633`, `CS8634`, `CS8643`-`CS8645`, `CS8667`, `CS8714`, `CS8762`-`CS8777`, `CS8819`, `CS8824`, `CS8825`.
- Nullable switch exhaustiveness: `CS8655`, `CS8847`.

## Enabled nullable diagnostics

### `CS8597` - Thrown value may be null

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `Exception? ex = GetException(); throw ex;`
- Fix: guard first: `throw ex ?? new InvalidOperationException();`.

### `CS8600` - Converting possible null to non-nullable type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `string name = maybeName;` where `maybeName` is `string?`.
- Fix: use `string?`, add a guard, or provide a fallback: `maybeName ?? ""`.

### `CS8601` - Possible null reference assignment

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `_name = maybeName;` when `_name` is non-nullable.
- Fix: validate before assignment or make the field nullable.

### `CS8602` - Dereference of a possibly null reference

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `message.Length` when `message` is `string?`.
- Fix: check `message is not null` before dereferencing.

### `CS8603` - Possible null reference return

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `return null;` from a method declared `string`.
- Fix: return a non-null value or change the return type to `string?`.

### `CS8604` - Possible null reference argument

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `UseName(maybeName);` where `UseName` requires `string`.
- Fix: guard before the call or change the callee parameter to `string?`.

### `CS8605` - Unboxing a possibly null value

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `var count = (int)maybeBoxed;` when the boxed value can be null.
- Fix: check `maybeBoxed is int count` before using it.

### `CS8607` - Possible null value used with NotNull or DisallowNull

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: assigning maybe-null into a `[DisallowNull]` member.
- Fix: guard and throw before assigning.

### `CS8608` - Nullability mismatch in overridden member type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: override type annotation is less or more nullable than the base member.
- Fix: match the base member nullable annotations.

### `CS8609` - Nullability mismatch in overridden return type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: override return annotation differs from the base return annotation.
- Fix: align the return type nullability.

### `CS8610` - Nullability mismatch in overridden type parameter

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: override generic parameter nullability differs from base.
- Fix: make the generic parameter annotations match.

### `CS8611` - Nullability mismatch in partial method type parameter

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: partial method declaration and implementation use different nullable type parameter annotations.
- Fix: make both partial signatures identical.

### `CS8612` - Nullability mismatch in implicitly implemented member type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implicit interface implementation member type differs in nullability.
- Fix: match the interface member type exactly.

### `CS8613` - Nullability mismatch in implicitly implemented return type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implicit interface implementation return type differs in nullability.
- Fix: match the interface return contract.

### `CS8614` - Nullability mismatch in implicitly implemented parameter type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implicit interface implementation parameter type differs in nullability.
- Fix: match the interface parameter contract.

### `CS8615` - Nullability mismatch in implemented member type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implemented member type differs from interface in nullability.
- Fix: align the implementation signature.

### `CS8616` - Nullability mismatch in implemented return type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implemented return type is `string?` while interface returns `string`.
- Fix: return non-null or update the interface contract.

### `CS8617` - Nullability mismatch in implemented parameter type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implemented parameter type is `string` while interface allows `string?`.
- Fix: accept the same nullability as the interface.

### `CS8618` - Non-nullable member is not initialized

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `public string Name { get; set; }` is not initialized by the constructor.
- Fix: initialize it, make it `required`, or declare `string?`.

### `CS8619` - Value nullability does not match target type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: assign `List<string?>` to `IEnumerable<string>`.
- Fix: filter nulls or align element nullability.

### `CS8620` - Argument nullability does not match parameter type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: pass `IEnumerable<string?>` to a parameter requiring `IEnumerable<string>`.
- Fix: validate/filter null elements before the call.

### `CS8621` - Delegate return nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: method used as delegate returns nullable where delegate returns non-null.
- Fix: align return nullability or adapt the delegate.

### `CS8622` - Delegate parameter nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: event handler parameter nullability does not match the event delegate.
- Fix: match the delegate signature exactly.

### `CS8624` - Output argument nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `out string? value` passed to `out string` parameter.
- Fix: align the out/ref variable nullability.

### `CS8625` - Cannot convert null literal to non-nullable reference type

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `string name = null;`.
- Fix: use a non-null value or declare `string?`.

### `CS8629` - Nullable value type may be null

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `int count = maybeCount.Value;` without checking `HasValue`.
- Fix: check `HasValue`, use pattern matching, or provide a default.

### `CS8631` - Type argument nullability does not satisfy constraint

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: nullable type argument used where the generic constraint requires non-null.
- Fix: use a non-nullable type argument or change the constraint.

### `CS8633` - Constraint nullability does not match interface method

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implementation generic constraints differ from interface constraints.
- Fix: match the interface constraints or use explicit implementation.

### `CS8634` - Type argument nullability does not satisfy class constraint

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `T?` used where `T : class` expects non-null class type.
- Fix: use a non-nullable type argument.

### `CS8643` - Explicit interface specifier nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: explicit interface specifier nullability differs from implemented interface.
- Fix: align the explicit interface type.

### `CS8644` - Interface member not implemented because nullability differs

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: inherited interface nullability prevents member implementation.
- Fix: align the base/interface nullability contract.

### `CS8645` - Interface member listed with different nullability

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: same interface member appears through interface paths with different nullability.
- Fix: remove the conflict or implement explicitly.

### `CS8655` - Switch expression does not handle null

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: switch expression over `string?` has no `null` arm.
- Fix: add a `null => ...` arm or guard before the switch.

### `CS8667` - Partial method declarations have inconsistent nullability

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: partial declarations annotate parameters differently.
- Fix: make all partial declarations use the same nullability.

### `CS8670` - Initializer dereferences a possibly null member

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `new Container { Items = { "A" } }` when `Items` may be null.
- Fix: initialize `Items` to a non-null collection.

### `CS8714` - Type argument violates notnull constraint

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: nullable type argument violates a `notnull` constraint.
- Fix: use a non-nullable type argument.

### `CS8762` - Parameter must be non-null on exit

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: method annotated to ensure a parameter is non-null exits without checking it.
- Fix: throw or assign before returning.

### `CS8763` - DoesNotReturn method returns

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `[DoesNotReturn]` method can return normally.
- Fix: always throw/terminate or remove the attribute.

### `CS8764` - Override return nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: override returns nullable where base returns non-null.
- Fix: match the base return nullability.

### `CS8765` - Override parameter nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: override parameter uses narrower nullability than base.
- Fix: match the base parameter nullability.

### `CS8766` - Implemented return nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: interface implementation return nullability differs.
- Fix: match the interface return contract.

### `CS8767` - Implemented parameter nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: interface implementation parameter nullability differs.
- Fix: match the interface parameter contract.

### `CS8768` - Implemented return type nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implemented return type nullability differs by generic/member type.
- Fix: align the implemented return type annotations.

### `CS8769` - Implemented parameter type nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: implemented parameter type nullability differs by generic/member type.
- Fix: align the implemented parameter annotations.

### `CS8770` - DoesNotReturn contract is not satisfied

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: method contract says it does not return, but a path returns.
- Fix: make all paths throw/terminate or remove the attribute.

### `CS8774` - Member must be non-null on exit

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `[MemberNotNull]` member is still maybe-null on exit.
- Fix: initialize the member before returning.

### `CS8775` - Member must be non-null on exit

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: member promised non-null on exit remains maybe-null.
- Fix: assign it or change the annotation.

### `CS8776` - Member name cannot be used in nullability attribute

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `[MemberNotNull("BadName")]` references an invalid member.
- Fix: reference a valid field/property name.

### `CS8777` - Parameter must be non-null on exit

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: `[NotNullWhen(true)]` parameter is not proven non-null.
- Fix: add the required guard or correct the attribute.

### `CS8819` - Partial member nullability mismatch

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: partial member declaration and implementation differ in nullability.
- Fix: make both signatures match.

### `CS8824` - Parameter contract must prove non-null on exit

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: attribute contract says parameter is non-null on exit, but implementation does not prove it.
- Fix: validate the parameter before successful return.

### `CS8825` - Return value must be non-null under attribute contract

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: return value may be null when a parameter contract says it cannot be.
- Fix: return non-null in that path or correct annotations.

### `CS8847` - Switch expression does not handle null input

When it appears: the nullable reference type analysis found this enabled warning in the project.

Example:
- Bad: switch expression over nullable input omits `null`.
- Fix: handle `null` explicitly or guard first.
