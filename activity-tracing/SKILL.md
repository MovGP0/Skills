---
name: activity-tracing
description: Guides activity tracing with generated ActivitySources, tags, parent activities, exception status handling, and registration. Use when adding or reviewing OpenTelemetry activity tracing in Bendex flows.
---
# Activity Tracing

- Use activity tracing for user-triggered flows, important domain actions, and cross-component transitions where we need to see call order and inputs.
- Do not add activity tracking to
    - Constructors, destructors
    - HandleCreated events
    - `Dispose()` methods.
    - Properties (including `Get<PropertyName>()` or `Set<PropertyName>()` methods)
    - Methods that are called often, like `OnLoad()`, `OnDraw()` or `OnMouseMove()`
    - *.Designer.cs files
- Prefer activity tracing instead of `LogDebug` in methods that are traced; remove those debug logs when adding tracing.
- Implementation pattern:
    - Ensure the class has `[GenerateActivitySources]` and `using System.Diagnostics;`.
    - Wrap method bodies with `using var activity = <Type>ActivitySources.<MethodName>.Create(parentActivity);`.
    - Add key inputs via `activity?.AddTag("arg.<name>", value);`.
    - On exceptions: `activity?.AddException(ex); activity?.SetStatus(ActivityStatusCode.Error, ex.Message);` then rethrow.
    - If a method has a parent activity, pass it through to downstream calls and to `Create(parentActivity)`.
    - Register the generated activity sources in the module `ActivitySources.cs` (e.g. add `.Concat(<Type>ActivitySources.GetAll())` to the module's `GetAll()` method).

Example:
```csharp
[GenerateActivitySources]
public sealed class ExampleService
{
    public void DoWork(int stepIndex, Activity? parentActivity = null)
    {
        using var activity = ExampleServiceActivitySources.DoWork.Create(parentActivity);
        activity?.AddTag("arg.stepIndex", stepIndex);
        try
        {
            // work here
        }
        catch (Exception ex)
        {
            activity?.AddException(ex);
            activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
            throw;
        }
    }
}
```

Event Handler:
```csharp
public void OnSomeEvent(object? sender, EventArgs args)
{
    using var activity = ExampleServiceActivitySources.OnSomeEvent.Create();
    try
    {
        // work here
    }
    catch (Exception ex)
    {
        activity?.AddException(ex);
        activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
        throw;
    }
}
```
