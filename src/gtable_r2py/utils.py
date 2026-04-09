"""Internal utility functions for gtable_r2py."""

from __future__ import annotations

from grid_r2py import Unit, unit_c


def neg_to_pos(x: int, max_val: int) -> int:
    """Convert negative index to positive. -1 → max_val, 0 stays 0."""
    return x if x >= 0 else max_val + 1 + x


def unit_slice(u: Unit, start: int, stop: int) -> Unit:
    """Extract a sub-range from a Unit (workaround: Unit only supports int indexing)."""
    if start >= stop:
        return Unit([], "cm")
    return unit_c(*(u[i] for i in range(start, stop)))


def insert_unit(x: Unit, values: Unit, after: int) -> Unit:
    """Insert *values* into *x* after position *after* (0-based, 0 = prepend)."""
    len_x = len(x)
    if len_x == 0:
        return values
    if len(values) == 0:
        return x
    if after <= 0:
        return unit_c(values, x)
    if after >= len_x:
        return unit_c(x, values)
    head = unit_slice(x, 0, after)
    tail = unit_slice(x, after, len_x)
    return unit_c(head, values, tail)


def compare_unit(x: Unit, y: Unit, comp) -> Unit:
    """Element-wise unit comparison (comp should be unit_pmax or unit_pmin)."""
    if len(y) == 0:
        return x
    if len(x) == 0:
        return y
    return comp(x, y)


def len_same_or_1(x, n: int) -> bool:
    """Check that x has length 1 or n."""
    length = len(x) if hasattr(x, "__len__") else 1
    return length == 1 or length == n
