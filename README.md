# Constraints

A lightweight, type-safe collection of reusable constraints for validating
values against predefined conditions.

The `constraints.py` module provides a set of immutable, generic constraint
implementations that define whether a value satisfies a particular condition.
It offers a consistent interface for expressing unrestricted values, finite
sets, numeric or ordered intervals, and minimum or maximum boundaries.

The module is designed to be easily integrated into validation systems,
configuration management, data models, and other applications that require
declarative value restrictions.

## Features

-   **Generic constraints** — Support for different value types through
    Python's type parameter syntax.
-   **Structural typing** — A common `Constraint[T]` protocol allows custom
    constraint implementations.
-   **Unrestricted values** — `AnyValue` accepts any value without applying
    restrictions.
-   **Finite value sets** — `OneOf` restricts values to a predefined
    collection of hashable elements.
-   **Intervals** — `Range` defines lower and upper bounds with independently
    configurable inclusivity.
-   **Minimum and maximum boundaries** — `Minimum` and `Maximum` enforce
    individual lower and upper limits.
-   **Immutability** — Constraint implementations use frozen, slotted
    dataclasses.
-   **Type safety** — Generic type parameters and protocols provide static
    type checking support.

## Requirements

-   Python 3.12 or later.
-   No third-party dependencies.

The module uses PEP 695 type parameter syntax, introduced in Python 3.12.

## Installation

The module has no external dependencies.

Copy `constraints.py` into the project and import the required classes:

```python
from constraints import (
    AnyValue,
    Constraint,
    Maximum,
    Minimum,
    OneOf,
    Range,
)
```

## Usage

All constraints implement the `Constraint[T]` protocol and expose a single
method:

```python
allows(value: T, /) -> bool
```

The method returns `True` when the supplied value satisfies the constraint
and `False` otherwise.

### Unrestricted values

`AnyValue` represents the absence of restrictions. It accepts every value of
the specified type.

```python
constraint = AnyValue[int]()

assert constraint.allows(42)
assert constraint.allows(-10)
assert constraint.allows(0)
```

### Finite sets

`OneOf` accepts only values contained in a predefined set.

The constructor accepts either a `set` or a `frozenset` and stores the values
internally as a `frozenset`.

```python
constraint = OneOf({1, 2, 3})

assert constraint.allows(1)
assert constraint.allows(2)
assert not constraint.allows(4)
```

It also supports other hashable types:

```python
constraint = OneOf({"red", "green", "blue"})

assert constraint.allows("red")
assert constraint.allows("blue")
assert not constraint.allows("yellow")
```

An empty set represents a constraint that rejects every value.

```python
constraint = OneOf(set())

assert not constraint.allows(1)
```

### Ranges

`Range` restricts values to an interval defined by lower and upper bounds.

Both boundaries are inclusive by default.

```python
constraint = Range(10, 100)

assert constraint.allows(10)
assert constraint.allows(50)
assert constraint.allows(100)
assert not constraint.allows(101)
```

Boundary inclusivity can be configured independently using `include_minimum`
and `include_maximum`.

```python
# Exclusive lower bound, inclusive upper bound.
constraint = Range(
    10,
    100,
    include_minimum=False,
    include_maximum=True,
)

assert not constraint.allows(10)
assert constraint.allows(11)
assert constraint.allows(100)
```

```python
# Exclusive boundaries.
constraint = Range(
    0.0,
    1.0,
    include_minimum=False,
    include_maximum=False,
)

assert constraint.allows(0.5)
assert not constraint.allows(0.0)
assert not constraint.allows(1.0)
```

The constructor validates the interval definition and raises `ValueError` if:

-   The maximum bound is less than the minimum bound.
-   Both bounds are equal, but at least one boundary is exclusive.

### Minimum boundary

`Minimum` requires a value to be greater than or equal to a specified lower
bound.

```python
constraint = Minimum(10)

assert constraint.allows(10)
assert constraint.allows(15)
assert not constraint.allows(9)
```

To make the lower boundary exclusive, set `inclusive=False`.

```python
constraint = Minimum(10, inclusive=False)

assert not constraint.allows(10)
assert constraint.allows(11)
```

### Maximum boundary

`Maximum` requires a value to be less than or equal to a specified upper
bound.

```python
constraint = Maximum(100)

assert constraint.allows(100)
assert constraint.allows(50)
assert not constraint.allows(101)
```

To make the upper boundary exclusive, set `inclusive=False`.

```python
constraint = Maximum(100, inclusive=False)

assert not constraint.allows(100)
assert constraint.allows(99)
```

## Custom constraints

The `Constraint[T]` protocol defines the structural interface for implementing
custom constraints.

Any class that provides a compatible `allows` method can be used wherever a
`Constraint[T]` is expected. Explicit inheritance from the protocol is not
required.

For example:

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Positive:
    """A constraint accepting only positive values."""

    def allows(self, value: int, /) -> bool:
        return value > 0


constraint: Constraint[int] = Positive()

assert constraint.allows(10)
assert not constraint.allows(-5)
```

This allows domain-specific validation rules to coexist with the built-in
implementations through a common interface.

## API Reference

| Component       | Description                                                                           |
| --------------- | ------------------------------------------------------------------------------------- |
| `Comparable`    | Protocol defining the ordering comparison operations required by ordered constraints. |
| `Constraint[T]` | Structural protocol defining the common constraint interface.                         |
| `AnyValue[T]`   | Accepts every value.                                                                  |
| `OneOf[T]`      | Accepts values belonging to a finite set of hashable elements.                        |
| `Range[T]`      | Accepts values within a bounded interval.                                             |
| `Minimum[T]`    | Accepts values satisfying a lower-bound condition.                                    |
| `Maximum[T]`    | Accepts values satisfying an upper-bound condition.                                   |

### Type requirements

-   `OneOf[T]` requires `T` to be hashable.
-   `Range[T]`, `Minimum[T]`, and `Maximum[T]` require `T` to support the
    comparison operations defined by `Comparable`.
-   `AnyValue[T]` and `Constraint[T]` do not impose additional runtime
    restrictions on the value type.

## Design Notes

All built-in constraint implementations are immutable. Their state cannot be
reassigned after initialization.

The implementations use `frozen=True` and `slots=True` to provide immutable,
memory-efficient instances.

Constraints perform validation through the `allows` method and do not raise
exceptions when a value fails to satisfy a condition. Invalid interval
definitions, however, are rejected during `Range` initialization.

The module does not perform implicit type conversion or coercion. Values are
evaluated using the comparison and membership semantics of their underlying
Python types.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
