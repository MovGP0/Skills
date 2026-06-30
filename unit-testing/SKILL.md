---
name: unit-testing
description: Guides unit test setup, naming, TestOf usage, Arrange/Act/Assert structure, ServiceLocator initialization, and Shouldy assertions. Use when adding, reviewing, or fixing unit tests.
---
# Unit Testing

## Test setup
- You may need to initialize a unit test with a `ServiceLocator`. Especially for logging:
```csharp
[TestOf(typeof(SettingsProvider), nameof(SettingsProvider.LoadSettings))]
public sealed class LoadSettingsTests: IDisposable
{
    public LoadSettingsTests(ITestOutputHelper testOutputHelper)
    {
        ServiceLocator.Cleanup();
        ServiceLocator.Initialize(services =>
        {
            services.AddLogging(logger =>
            {
                logger.SetMinimumLevel(LogLevel.Debug);
                logger.AddXUnit(testOutputHelper);
            });
        });
    }

    public void Dispose() => ServiceLocator.Cleanup();

    // tests come here...
```
- The name of a test (`Fact`/`Theory`) should start with the name "Should", followed by the expected result and the action taken. Setting the `DisplayName` property improves readability.
```csharp
[Fact(DisplayName = "Should return user settings when invoked")]
public void ShouldReturnUserSettingsWhenInvoked()
```
- Structure the unit tests using `// Arrange`, `// Act` and `// Assert` comments. You may also use `// Cleanup` or `// Arrange & Act` or `// Act & Assert` in rare situations.
- Name the object beeing testet as `subject` and the (primary) result value `result`:
```csharp
// Arrange
var subject = new SomeTypeUnderTest();

// Act
var result = subject.DoSomething();
```
- Use Shouldy for assertions. Use one assertion only, but you may use `ShouldSatisfyAllConditions` when multiple assertions are required:
```csharp
result.ShouldSatisfyAllConditions(
    () => /* first assertion */,
    () => /* second assertion */,
    () => /* third assertion */,
    // add more assertions as required
);
```
- You may also nest assertions:
```csharp
result.ShouldSatisfyAllConditions(
    () => result.Value.ShouldNotBeNull().ShouldBe("foobar"),
    // add more assertions as required
);
```

## Usage of `[TestOf]` Attribute
- Use `[TestOf(typeof(ClassName))]` on test classes to indicate the class under test.
- Use `[TestOf(typeof(ClassName), nameof(ClassName.MethodName))]` or `[TestOf(typeof(ClassName), nameof(ClassName.PropertyName))]` for nested test classes.
- Use the `ILObjectNames` class for special .NET objects like operators and constructors.

**Examples:**
```csharp
[TestOf(typeof(TypeUnderTest)]
public static class TypeUnderTestTests
{
    [TestOf(typeof(TypeUnderTest), ILObjectNames.Constructor)]
    public sealed class ConstructorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.Deconstructor)]
    public sealed class DeconstructorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.Indexer)]
    public sealed class IndexerTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.op_Addition)]
    public sealed class AdditionOperatorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.op_MultiplicationAssignment)]
    public sealed class MultiplicationAssignmentOperatorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.op_GreaterThanOrEqualAssignment)]
    public sealed class GreaterThanOrEqualAssignmentOperatorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.op_Implicit)]
    public sealed class ImplicitOperatorTests { /* ... */ }

    [TestOf(typeof(TypeUnderTest), ILObjectNames.op_Explicit)]
    public sealed class ExplicitOperatorTests { /* ... */ }
}
```
