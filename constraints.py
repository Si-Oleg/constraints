from collections.abc import Hashable
from dataclasses import dataclass
from typing import Protocol, Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...

    def __le__(self, other: Self, /) -> bool: ...


class Constraint[T](Protocol):
    def allows(self, value: T, /) -> bool: ...


@dataclass(frozen=True, slots=True)
class AnyValue[T]:
    def allows(self, _: T, /) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class OneOf[T: Hashable]:
    values: frozenset[T]

    def __init__(self, values: frozenset[T] | set[T], /) -> None:
        object.__setattr__(self, "values", frozenset(values))

    def allows(self, value: T, /) -> bool:
        return value in self.values


@dataclass(frozen=True, slots=True)
class Range[T: Comparable]:
    minimum: T
    maximum: T
    include_minimum: bool = True
    include_maximum: bool = True

    def __post_init__(self) -> None:
        if self.maximum < self.minimum:
            raise ValueError(
                "The maximum bound must not be less than the minimum bound."
            )

        if (
            self.minimum == self.maximum
            and not (self.include_minimum and self.include_maximum)
        ):
            raise ValueError(
                "An interval with equal bounds must include both boundaries."
            )

    def allows(self, value: T, /) -> bool:
        lower_ok = (
            self.minimum <= value
            if self.include_minimum
            else self.minimum < value
        )

        upper_ok = (
            value <= self.maximum
            if self.include_maximum
            else value < self.maximum
        )

        return lower_ok and upper_ok


@dataclass(frozen=True, slots=True)
class Minimum[T: Comparable]:
    value: T
    inclusive: bool = True

    def allows(self, value: T, /) -> bool:
        return self.value <= value if self.inclusive else self.value < value


@dataclass(frozen=True, slots=True)
class Maximum[T: Comparable]:
    value: T
    inclusive: bool = True

    def allows(self, value: T, /) -> bool:
        return value <= self.value if self.inclusive else value < self.value
