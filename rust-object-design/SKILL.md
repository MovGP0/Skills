---
name: rust-object-design
description: Guide Rust domain object and data structure design for expressive, maintainable code. Use when modeling Rust structs, enums, newtypes, value objects, entities, aggregates, builders, domain invariants, state machines, or when reviewing Rust code for primitive obsession, anemic models, invalid states, public mutable fields, or misplaced business behavior.
---

# Coding Guidelines: Modeling Domain Objects in Rust

Purpose: Apply Rust's type system, ownership model, privacy, enums, traits, and `Result`-returning constructors to design expressive, safe, and maintainable domain models.

## Principles for Modeling Domain Objects

### Model concepts, not storage shapes

Bad: Database/JSON-shaped struct that ignores domain meaning

```rust
pub struct OrderData {
    pub id: i64,
    pub customer_name: String,
    pub total: f64,
    pub status: String,
}
```

Problems:

- `customer_name` is a raw string instead of a concept.
- `total` has no currency, precision strategy, or rules.
- `status` is stringly typed.
- Public fields allow invalid mutation from anywhere.

Better: Domain language and behavior embedded in types

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OrderStatus {
    Draft,
    Submitted,
    Paid,
    Shipped,
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PersonName(String);

impl PersonName {
    pub fn new(value: impl Into<String>) -> Result<Self, DomainError> {
        let value = value.into().trim().to_owned();
        if value.is_empty() {
            return Err(DomainError::InvalidName);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Money {
    minor_units: i64,
    currency: CurrencyCode,
}

impl Money {
    pub fn new(minor_units: i64, currency: CurrencyCode) -> Result<Self, DomainError> {
        if minor_units < 0 {
            return Err(DomainError::NegativeMoney);
        }
        Ok(Self { minor_units, currency })
    }
}

pub struct Order {
    id: OrderId,
    customer_name: PersonName,
    total: Money,
    status: OrderStatus,
}

impl Order {
    pub fn new(id: OrderId, customer_name: PersonName, total: Money) -> Self {
        Self {
            id,
            customer_name,
            total,
            status: OrderStatus::Draft,
        }
    }

    pub fn submit(&mut self) -> Result<(), DomainError> {
        if self.status != OrderStatus::Draft {
            return Err(DomainError::InvalidOrderTransition);
        }
        self.status = OrderStatus::Submitted;
        Ok(())
    }
}
```

### Prefer rich domain objects over anemic DTO-style objects

Bad: Logic outside, invariants unprotected

```rust
pub struct BankAccount {
    pub balance_cents: i64,
}

pub fn withdraw(account: &mut BankAccount, amount_cents: i64) -> Result<(), DomainError> {
    if amount_cents <= 0 {
        return Err(DomainError::InvalidAmount);
    }
    if account.balance_cents < amount_cents {
        return Err(DomainError::InsufficientFunds);
    }
    account.balance_cents -= amount_cents;
    Ok(())
}
```

Better: Entity owns behavior and guards its state

```rust
pub struct BankAccount {
    balance_cents: i64,
}

impl BankAccount {
    pub fn new(initial_balance_cents: i64) -> Result<Self, DomainError> {
        if initial_balance_cents < 0 {
            return Err(DomainError::InvalidAmount);
        }
        Ok(Self { balance_cents: initial_balance_cents })
    }

    pub fn balance_cents(&self) -> i64 {
        self.balance_cents
    }

    pub fn deposit(&mut self, amount_cents: i64) -> Result<(), DomainError> {
        if amount_cents <= 0 {
            return Err(DomainError::InvalidAmount);
        }
        self.balance_cents += amount_cents;
        Ok(())
    }

    pub fn withdraw(&mut self, amount_cents: i64) -> Result<(), DomainError> {
        if amount_cents <= 0 {
            return Err(DomainError::InvalidAmount);
        }
        if self.balance_cents < amount_cents {
            return Err(DomainError::InsufficientFunds);
        }
        self.balance_cents -= amount_cents;
        Ok(())
    }
}
```

### Use newtypes for value objects

Bad: Primitive obsession leads to repeated validation and argument mixups

```rust
pub struct User {
    pub email: String,
}
```

Better: Encapsulate validation and normalization in a value object

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct EmailAddress(String);

impl EmailAddress {
    pub fn parse(value: impl Into<String>) -> Result<Self, DomainError> {
        let normalized = value.into().trim().to_lowercase();
        if normalized.is_empty() || !normalized.contains('@') {
            return Err(DomainError::InvalidEmail);
        }
        Ok(Self(normalized))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl std::fmt::Display for EmailAddress {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

pub struct User {
    email: EmailAddress,
}

impl User {
    pub fn new(email: EmailAddress) -> Self {
        Self { email }
    }
}
```

Usage:

```rust
let first = EmailAddress::parse("Test@Example.com")?;
let second = EmailAddress::parse("test@example.com")?;
assert_eq!(first, second);
```

### Preserve invariants inside the type

Bad: Invalid values are allowed and must be checked everywhere else

```rust
pub struct PercentageDiscount {
    pub percent: f32,
}
```

Better: Constructor enforces the valid range

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct PercentageDiscount {
    percent: f32,
}

impl PercentageDiscount {
    pub fn new(percent: f32) -> Result<Self, DomainError> {
        if !(0.0..=100.0).contains(&percent) {
            return Err(DomainError::InvalidDiscount);
        }
        Ok(Self { percent })
    }

    pub fn percent(self) -> f32 {
        self.percent
    }
}
```

Use `Result<Self, E>` for fallible construction. Use `Self` directly only when every input accepted by the function is valid.

### Eliminate invalid states with enums

Bad: Boolean flags and options create contradictory combinations

```rust
pub struct Payment {
    pub is_paid: bool,
    pub paid_at_utc: Option<time::OffsetDateTime>,
}
```

Better: Represent state explicitly with a closed set of possibilities

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PaymentStatus {
    Unpaid,
    Paid { paid_at_utc: time::OffsetDateTime },
}

pub struct Payment {
    status: PaymentStatus,
}

impl Payment {
    pub fn new() -> Self {
        Self { status: PaymentStatus::Unpaid }
    }

    pub fn mark_paid(&mut self, paid_at_utc: time::OffsetDateTime) -> Result<(), DomainError> {
        if matches!(self.status, PaymentStatus::Paid { .. }) {
            return Err(DomainError::PaymentAlreadyPaid);
        }
        self.status = PaymentStatus::Paid { paid_at_utc };
        Ok(())
    }
}
```

Prefer an enum when only one of several states is valid. Prefer typestate only when compile-time state transitions are worth the added complexity.

### Encapsulate mutation; prefer immutability for value-like concepts

Bad: Mutable public fields introduce shared-state bugs

```rust
pub struct Address {
    pub street: String,
    pub city: String,
    pub postal_code: String,
}
```

Better: Immutable value object; controlled changes return a new value

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Address {
    street: String,
    city: String,
    postal_code: String,
}

impl Address {
    pub fn new(street: String, city: String, postal_code: String) -> Result<Self, DomainError> {
        if street.trim().is_empty() || city.trim().is_empty() || postal_code.trim().is_empty() {
            return Err(DomainError::InvalidAddress);
        }

        Ok(Self {
            street: street.trim().to_owned(),
            city: city.trim().to_owned(),
            postal_code: postal_code.trim().to_owned(),
        })
    }

    pub fn with_postal_code(&self, postal_code: String) -> Result<Self, DomainError> {
        Self::new(self.street.clone(), self.city.clone(), postal_code)
    }
}
```

For entities, allow mutation through intention-revealing methods. For value objects, prefer `Clone` plus validated replacement methods.

### Treat collections and relationships as part of the model

Bad: Exposed mutable collections break aggregate rules

```rust
pub struct Order {
    pub lines: Vec<OrderLine>,
}

pub struct OrderLine {
    pub product_code: String,
    pub quantity: u32,
}
```

Better: Hide the collection; expose operations that enforce rules

```rust
pub struct Order {
    lines: Vec<OrderLine>,
}

impl Order {
    pub fn lines(&self) -> &[OrderLine] {
        &self.lines
    }

    pub fn add_line(&mut self, product_code: ProductCode, quantity: NonZeroU32) {
        if let Some(line) = self.lines.iter_mut().find(|line| line.product_code == product_code) {
            line.increase_quantity(quantity);
            return;
        }

        self.lines.push(OrderLine::new(product_code, quantity));
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrderLine {
    product_code: ProductCode,
    quantity: NonZeroU32,
}

impl OrderLine {
    fn new(product_code: ProductCode, quantity: NonZeroU32) -> Self {
        Self { product_code, quantity }
    }

    fn increase_quantity(&mut self, amount: NonZeroU32) {
        self.quantity = NonZeroU32::new(self.quantity.get() + amount.get())
            .expect("sum of two non-zero quantities is non-zero");
    }
}
```

Expose slices, iterators, or read-only views instead of `&mut Vec<T>` unless callers truly own collection invariants.

### Push behavior to the place where data has meaning

Bad: Procedural helpers operate on passive data structures

```rust
pub struct Money {
    pub amount_cents: i64,
    pub currency: String,
}

pub fn add_money(left: Money, right: Money) -> Result<Money, DomainError> {
    if left.currency != right.currency {
        return Err(DomainError::CurrencyMismatch);
    }
    Ok(Money {
        amount_cents: left.amount_cents + right.amount_cents,
        currency: left.currency,
    })
}
```

Better: The concept owns its operations and invariants

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Money {
    amount_cents: i64,
    currency: CurrencyCode,
}

impl Money {
    pub fn add(&self, other: &Self) -> Result<Self, DomainError> {
        if self.currency != other.currency {
            return Err(DomainError::CurrencyMismatch);
        }
        Ok(Self {
            amount_cents: self.amount_cents + other.amount_cents,
            currency: self.currency.clone(),
        })
    }
}
```

Use associated functions and methods when the behavior belongs to the type. Use services for orchestration across aggregates, I/O, policies, or behavior that does not belong to a single concept.

### Use factories or builders when construction has rules

Bad: Objects can be created in half-baked, inconsistent shapes

```rust
pub struct Subscription {
    pub email: String,
    pub start_date_utc: time::OffsetDateTime,
    pub end_date_utc: time::OffsetDateTime,
    pub auto_renew: bool,
}
```

Better: Factory centralizes creation logic and enforces invariants

```rust
pub struct Subscription {
    email: EmailAddress,
    start_date_utc: time::OffsetDateTime,
    end_date_utc: time::OffsetDateTime,
    auto_renew: bool,
}

impl Subscription {
    pub fn annual(
        email: EmailAddress,
        start_date_utc: time::OffsetDateTime,
        auto_renew: bool,
    ) -> Result<Self, DomainError> {
        let end_date_utc = start_date_utc + time::Duration::days(365);
        if end_date_utc <= start_date_utc {
            return Err(DomainError::InvalidSubscriptionPeriod);
        }

        Ok(Self {
            email,
            start_date_utc,
            end_date_utc,
            auto_renew,
        })
    }
}
```

Use a builder when many optional inputs must be assembled before validation. Keep the final `build()` method responsible for all cross-field invariants.

### Reduce primitive obsession

Bad: Everything is `String`, `i64`, or `f64` with unspecified units and formats

```rust
pub struct Shipment {
    pub tracking_number: String,
    pub country_code: String,
    pub weight: f64,
}
```

Better: Narrow domain types communicate meaning and constraints

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CountryCode(String);

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Kilograms(f64);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct TrackingNumber(String);

pub struct Shipment {
    tracking_number: TrackingNumber,
    destination_country: CountryCode,
    weight: Kilograms,
}
```

Wrap primitives when they carry domain meaning, have validation rules, can be confused with other values of the same primitive type, or need domain-specific formatting.

## Rust-Specific Guidance

- Prefer private fields plus constructors and methods for invariant-bearing types.
- Derive only traits that preserve the domain meaning. Avoid deriving `Default` if the default value is invalid or meaningless.
- Prefer `NonZeroU32`, `NonEmpty` wrappers, bounded newtypes, and enums over runtime comments.
- Use `Option<T>` for actual absence, not for invalid intermediate states.
- Use `Result<T, DomainError>` for expected domain validation failures. Reserve `panic!` for impossible internal invariant violations.
- Use owned fields for domain objects unless borrowing is central to the model. Avoid spreading lifetimes through domain types just to save allocations.
- Keep serialization DTOs separate from rich domain types when external formats permit invalid or partial data.
- Keep aggregate boundaries explicit. Do not expose mutable internals that let callers bypass business rules.

## Common Pitfalls vs. Good Practices

| What weak models do | What strong models do |
| --- | --- |
| Public fields everywhere | Private fields and intention-revealing methods |
| Strings and numbers stand in for concepts | Newtypes wrap meaningful domain values |
| `bool` and `Option` combinations represent state | Enums represent valid states directly |
| Business rules live in procedural helpers | Behavior lives where the data has meaning |
| DTOs are used as domain entities | DTOs are mapped into validated domain types |
| `Default` creates invalid placeholders | Constructors/factories enforce invariants |

## Litmus Test

Can a caller create a nonsensical instance of the type without using `unsafe`, reflection-like tricks, or test-only constructors?

If yes, strengthen the model with privacy, newtypes, enums, validated constructors, and behavior on the owning type until invalid states are hard or impossible to represent.

## Adoption Checklist

- Replace meaningful primitive fields such as email, money, country, weight, and identifiers with newtypes.
- Make value-like concepts immutable and comparable by value.
- Hide collections and expose operations that preserve aggregate rules.
- Replace contradictory flags and nullable fields with enums.
- Push domain operations onto the owning type instead of helper modules.
- Guard constructors, factories, and builders with validation and invariant checks.
- Separate external DTOs from internal domain models when input can be malformed or incomplete.

## Sources / Further Reading

- Eric Evans, Domain-Driven Design (2003)
- Vaughn Vernon, Implementing Domain-Driven Design (2013)
- Martin Fowler, Anemic Domain Model
- Scott Wlaschin, Domain Modeling Made Functional
- Rust API Guidelines: predictability, type safety, and ownership conventions
- Rust Design Patterns: newtype, builder, typestate, and encapsulation patterns
