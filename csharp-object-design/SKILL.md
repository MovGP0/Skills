---
name: csharp-object-design
description: correct modelling of C# datastructures for maintainable code
---
# Coding Guidelines: Modeling Domain Objects in C\#

Purpose: Practical guidelines for modeling rich domain objects in C# with side-by-side bad vs. better examples, rationale, and usage notes. Apply these patterns to design expressive, safe, and maintainable domain models.

## Principles for Modeling Domain Objects

### Model concepts, not storage shapes

Bad: Database/JSON-shaped class that ignores domain meaning

```c#
public sealed class OrderData
{
    public int Id { get; set; }
    public string CustomerName { get; set; } = "";
    public decimal Total { get; set; }
    public string Status { get; set; } = "";
}
```

Problems:

- CustomerName is a raw string instead of a concept.
- Total has no currency or rules.
- Status is stringly-typed.
- Type says nothing about allowed behaviors.

Better: Domain language and behavior embedded in types

```c#
public enum OrderStatus
{
    Draft,
    Submitted,
    Paid,
    Shipped,
    Cancelled
}

public sealed record PersonName(string Value)
{
    public PersonName(string value) : this()
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Name must not be empty.", nameof(value));

        Value = value.Trim();
    }

    public string Value { get; } = Value;
}

public sealed record Money(decimal Amount, string Currency)
{
    public Money(decimal amount, string currency) : this()
    {
        if (amount < 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        if (string.IsNullOrWhiteSpace(currency))
            throw new ArgumentException("Currency is required.", nameof(currency));

        Amount = amount;
        Currency = currency;
    }

    public decimal Amount { get; } = Amount;
    public string Currency { get; } = Currency;
}

public sealed class Order
{
    public Order(int id, PersonName customerName, Money total)
    {
        Id = id;
        CustomerName = customerName;
        Total = total;
        Status = OrderStatus.Draft;
    }

    public int Id { get; }
    public PersonName CustomerName { get; }
    public Money Total { get; private set; }
    public OrderStatus Status { get; private set; }

    public void Submit()
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException("Only draft orders can be submitted.");

        Status = OrderStatus.Submitted;
    }
}
```

### Prefer rich domain objects over anemic DTO-style objects

Bad: Logic outside, invariants unprotected

```c#
public sealed class BankAccount
{
    public decimal Balance { get; set; }
}

public sealed class BankAccountService
{
    public void Withdraw(BankAccount account, decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        if (account.Balance < amount)
            throw new InvalidOperationException("Insufficient funds.");

        account.Balance -= amount;
    }
}
```

Better: Entity owns behavior and guards its state

```c#
public sealed class BankAccount
{
    public BankAccount(decimal initialBalance)
    {
        if (initialBalance < 0)
            throw new ArgumentOutOfRangeException(nameof(initialBalance));

        Balance = initialBalance;
    }

    public decimal Balance { get; private set; }

    public void Deposit(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        Balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        if (Balance < amount)
            throw new InvalidOperationException("Insufficient funds.");

        Balance -= amount;
    }
}
```

### Use value objects where equality is by value

Bad: Primitive obsession leads to leaky validation and accidental equality

```c#
public sealed class User
{
    public string Email { get; set; } = "";
}
```

Better: Encapsulate validation and normalization in a value object

```c#
public sealed record EmailAddress
{
    public EmailAddress(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Email must not be empty.", nameof(value));

        string normalized = value.Trim().ToLowerInvariant();

        if (!normalized.Contains('@'))
            throw new ArgumentException("Email is invalid.", nameof(value));

        Value = normalized;
    }

    public string Value { get; }

    public override string ToString() => Value;
}

public sealed class User
{
    public User(EmailAddress emailAddress)
    {
        EmailAddress = emailAddress;
    }

    public EmailAddress EmailAddress { get; }
}
```

Usage

```c#
var first = new EmailAddress("Test@Example.com");
var second = new EmailAddress("test@example.com");

bool same = first == second; // true
```

### Preserve invariants inside the type

Bad: Invalid values are allowed and must be checked everywhere else

```c#
public sealed class PercentageDiscount
{
    public decimal Percent { get; set; }
}
```

Better: Constructor enforces the valid range

```c#
public sealed record PercentageDiscount
{
    public PercentageDiscount(decimal percent)
    {
        if (percent < 0 || percent > 100)
            throw new ArgumentOutOfRangeException(nameof(percent), "Discount must be between 0 and 100.");

        Percent = percent;
    }

    public decimal Percent { get; }
}
```

### Eliminate invalid states instead of checking for them everywhere

Bad: Boolean flags and nullables create contradictory combinations

```c#
public sealed class Payment
{
    public bool IsPaid { get; set; }
    public DateTime? PaidAtUtc { get; set; }
}
```

Better: Represent state explicitly with a closed set of possibilities

```c#
public abstract record PaymentStatus;

public sealed record Unpaid : PaymentStatus;

public sealed record Paid(DateTime PaidAtUtc) : PaymentStatus;

public sealed class Payment
{
    public Payment()
    {
        Status = new Unpaid();
    }

    public PaymentStatus Status { get; private set; }

    public void MarkPaid(DateTime paidAtUtc)
    {
        if (Status is Paid)
            throw new InvalidOperationException("Payment is already marked as paid.");

        Status = new Paid(paidAtUtc);
    }
}
```

### Encapsulate mutation; prefer immutability for value-like concepts

Bad: Mutable bags of public setters introduce shared-state bugs

```c#
public sealed class Address
{
    public string Street { get; set; } = "";
    public string City { get; set; } = "";
    public string PostalCode { get; set; } = "";
}
```

Better: Immutable value object; controlled change via with-expressions

```c#
public sealed record Address
{
    public Address(string street, string city, string postalCode)
    {
        if (string.IsNullOrWhiteSpace(street))
            throw new ArgumentException("Street is required.", nameof(street));
        if (string.IsNullOrWhiteSpace(city))
            throw new ArgumentException("City is required.", nameof(city));
        if (string.IsNullOrWhiteSpace(postalCode))
            throw new ArgumentException("Postal code is required.", nameof(postalCode));

        Street = street.Trim();
        City = city.Trim();
        PostalCode = postalCode.Trim();
    }

    public string Street { get; }
    public string City { get; }
    public string PostalCode { get; }
}
```

Usage

```c#
Address oldAddress = new("Main Street 1", "Vienna", "1010");
Address newAddress = oldAddress with { PostalCode = "1020" };
```

For entities, allow mutation but keep it controlled through methods.

### Treat collections and relationships as part of the model

Bad: Exposed mutable collections break aggregate rules

```c#
public sealed class Order
{
    public List<OrderLine> Lines { get; } = new();
}

public sealed class OrderLine
{
    public string ProductCode { get; set; } = "";
    public int Quantity { get; set; }
}
```

Better: Hide the list; expose intention-revealing operations

```c#
public sealed class Order
{
    private readonly List<OrderLine> orderLines = new();

    public IReadOnlyList<OrderLine> OrderLines => orderLines;

    public void AddLine(string productCode, int quantity)
    {
        if (string.IsNullOrWhiteSpace(productCode))
            throw new ArgumentException("Product code is required.", nameof(productCode));

        if (quantity <= 0)
            throw new ArgumentOutOfRangeException(nameof(quantity));

        OrderLine? existingLine = orderLines.SingleOrDefault(line => line.ProductCode == productCode);
        if (existingLine is not null)
        {
            existingLine.IncreaseQuantity(quantity);
            return;
        }

        orderLines.Add(new OrderLine(productCode, quantity));
    }
}

public sealed class OrderLine
{
    public OrderLine(string productCode, int quantity)
    {
        if (string.IsNullOrWhiteSpace(productCode))
            throw new ArgumentException("Product code is required.", nameof(productCode));
        if (quantity <= 0)
            throw new ArgumentOutOfRangeException(nameof(quantity));

        ProductCode = productCode;
        Quantity = quantity;
    }

    public string ProductCode { get; }
    public int Quantity { get; private set; }

    public void IncreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));

        Quantity += amount;
    }
}
```

### Push behavior to the place where the data has meaning

Bad: Procedural helpers operate on passive data structures

```c#
public sealed class Money
{
    public decimal Amount { get; set; }
    public string Currency { get; set; } = "";
}

public static class PricingFunctions
{
    public static Money Add(Money left, Money right)
    {
        if (left.Currency != right.Currency)
            throw new InvalidOperationException("Currencies must match.");

        return new Money
        {
            Amount = left.Amount + right.Amount,
            Currency = left.Currency
        };
    }
}
```

Better: The concept owns its operations and invariants

```c#
public sealed record Money
{
    public Money(decimal amount, string currency)
    {
        if (string.IsNullOrWhiteSpace(currency))
            throw new ArgumentException("Currency is required.", nameof(currency));

        Amount = amount;
        Currency = currency.Trim().ToUpperInvariant();
    }

    public decimal Amount { get; }
    public string Currency { get; }

    public Money Add(Money other)
    {
        if (other is null)
            throw new ArgumentNullException(nameof(other));

        if (Currency != other.Currency)
            throw new InvalidOperationException("Currencies must match.");

        return new Money(Amount + other.Amount, Currency);
    }
}
```

Usage

```c#
Money total = new Money(10m, "EUR").Add(new Money(5m, "EUR"));
```

### Use factories/builders when construction has rules

Bad: Objects can be created in half-baked, inconsistent shapes

```c#
public sealed class Subscription
{
    public string Email { get; set; } = "";
    public DateTime StartDateUtc { get; set; }
    public DateTime EndDateUtc { get; set; }
    public bool AutoRenew { get; set; }
}
```

Better: Factory centralizes creation logic and enforces invariants

```c#
public sealed class Subscription
{
    private Subscription(EmailAddress emailAddress, DateTime startDateUtc, DateTime endDateUtc, bool autoRenew)
    {
        EmailAddress = emailAddress;
        StartDateUtc = startDateUtc;
        EndDateUtc = endDateUtc;
        AutoRenew = autoRenew;
    }

    public EmailAddress EmailAddress { get; }
    public DateTime StartDateUtc { get; }
    public DateTime EndDateUtc { get; }
    public bool AutoRenew { get; }

    public static Subscription CreateAnnual(EmailAddress emailAddress, DateTime startDateUtc, bool autoRenew)
    {
        DateTime endDateUtc = startDateUtc.AddYears(1);

        if (endDateUtc <= startDateUtc)
            throw new InvalidOperationException("End date must be after start date.");

        return new Subscription(emailAddress, startDateUtc, endDateUtc, autoRenew);
    }
}
```

Usage

```c#
Subscription subscription = Subscription.CreateAnnual(
    new EmailAddress("person@example.com"),
    DateTime.UtcNow,
    autoRenew: true);
```

### Reduce primitive obsession

Bad: Everything is string/int/decimal with unspecified units and formats

```c#
public sealed class Shipment
{
    public string TrackingNumber { get; set; } = "";
    public string CountryCode { get; set; } = "";
    public decimal Weight { get; set; }
}
```

Better: Narrow domain types communicate meaning and constraints

```c#
public sealed record CountryCode
{
    public CountryCode(string value)
    {
        if (string.IsNullOrWhiteSpace(value) || value.Trim().Length != 2)
            throw new ArgumentException("Country code must be a 2-letter ISO code.", nameof(value));

        Value = value.Trim().ToUpperInvariant();
    }

    public string Value { get; }
}

public sealed record Kilograms
{
    public Kilograms(decimal value)
    {
        if (value <= 0)
            throw new ArgumentOutOfRangeException(nameof(value));

        Value = value;
    }

    public decimal Value { get; }
}

public sealed record TrackingNumber
{
    public TrackingNumber(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Tracking number is required.", nameof(value));

        Value = value.Trim();
    }

    public string Value { get; }
}

public sealed class Shipment
{
    public Shipment(TrackingNumber trackingNumber, CountryCode destinationCountryCode, Kilograms weight)
    {
        TrackingNumber = trackingNumber;
        DestinationCountryCode = destinationCountryCode;
        Weight = weight;
    }

    public TrackingNumber TrackingNumber { get; }
    public CountryCode DestinationCountryCode { get; }
    public Kilograms Weight { get; }
}
```

## Common Pitfalls vs. Good Practices

| **What bad models do** | **What good models do** |
| --- | --- |
| - Public setters everywhere - Strings standing in for concepts - Contradictory/nullable state combos | - Constructors/factories enforce validity - Value objects wrap meaningful concepts - Illegal states are unrepresentable |
| - Business rules pushed to services - Entities mirror database rows | - Behavior lives where the data has meaning - Aggregates protect their invariants |

## Litmus Test

> Can I create a nonsensical instance of the type without cheating?

If yes, the model is usually too weak. Strengthen the type with invariants and behavior until invalid states are impossible to represent.

## Adoption Checklist

- Replace primitive properties that carry meaning (email, money, country, weights) with value objects.
- Make value-like concepts immutable; expose with-expressions for changes.
- Hide collections; add intention-revealing methods that enforce rules.
- Push domain operations onto the owning type, not helper services.
- Guard all constructors/factories with input validation and invariant checks.

## **Sources / Further Reading**

Mapping each principle to key sources:

- Model concepts, not storage shapes: [Evans, Domain-Driven Design (2003)](https://www.domainlanguage.com/ddd/); Vernon, Implementing DDD (2013); Fowler, 

  [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html).
- Prefer rich domain objects over anemic DTOs: Fowler, 

  [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html); Evans (2003); Vernon (2013).
- Use value objects, equality by value: [Evans (2003); Vernon (2013); Wlaschin, Domain Modeling Made Functional (2018)](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/).
- Preserve invariants inside the type: [Evans (2003); Vernon (2013); Robert C. Martin, Clean Code (2008)](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000003457/9780132350884) (guard clauses).
- Eliminate invalid states: [Wlaschin (2018) — illegal states unrepresentable; Option vs null](https://fsharpforfunandprofit.com/posts/designing-with-types-intro/); Evans (2003).
- Encapsulate mutation; prefer immutability: [Microsoft Docs — C# records and with-expressions](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record); Evans (2003).
- Collections and relationships are part of the model: Evans (2003) — Aggregates; Vernon (2013) — consistency boundaries.
- Push behavior to where data has meaning: Evans (2003); Vernon (2013); Martin, Clean Code (2008).
- Use factories/builders when construction has rules: Evans (2003); Vernon (2013); Martin, Clean Code (2008).
- Reduce primitive obsession: Evans (2003) — Value Objects; Vernon (2013); Wlaschin (2018).
