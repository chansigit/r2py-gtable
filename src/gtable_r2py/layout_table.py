"""Column-oriented layout data structure for GTable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LayoutRow:
    """Single-row view into a LayoutTable."""

    t: int
    l: int
    b: int
    r: int
    z: float
    clip: str
    name: str


class LayoutTable:
    """Column-oriented storage of grob placement metadata.

    Stores 7 parallel lists (t, l, b, r, z, clip, name) with both
    column-level and row-level access.
    """

    __slots__ = ("_t", "_l", "_b", "_r", "_z", "_clip", "_name")

    def __init__(
        self,
        t: list[int] | None = None,
        l: list[int] | None = None,
        b: list[int] | None = None,
        r: list[int] | None = None,
        z: list[float] | None = None,
        clip: list[str] | None = None,
        name: list[str] | None = None,
    ) -> None:
        self._t: list[int] = list(t) if t is not None else []
        self._l: list[int] = list(l) if l is not None else []
        self._b: list[int] = list(b) if b is not None else []
        self._r: list[int] = list(r) if r is not None else []
        self._z: list[float] = list(z) if z is not None else []
        self._clip: list[str] = list(clip) if clip is not None else []
        self._name: list[str] = list(name) if name is not None else []

    # -- Column access (properties return the internal list) ----------------

    @property
    def t(self) -> list[int]:
        return self._t

    @property
    def l(self) -> list[int]:
        return self._l

    @property
    def b(self) -> list[int]:
        return self._b

    @property
    def r(self) -> list[int]:
        return self._r

    @property
    def z(self) -> list[float]:
        return self._z

    @property
    def clip(self) -> list[str]:
        return self._clip

    @property
    def name(self) -> list[str]:
        return self._name

    # -- Length -------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._t)

    # -- Row access ---------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return LayoutRow(
                t=self._t[key], l=self._l[key], b=self._b[key], r=self._r[key],
                z=self._z[key], clip=self._clip[key], name=self._name[key],
            )
        if isinstance(key, slice):
            return LayoutTable(
                t=self._t[key], l=self._l[key], b=self._b[key], r=self._r[key],
                z=self._z[key], clip=self._clip[key], name=self._name[key],
            )
        if isinstance(key, list) and key and isinstance(key[0], bool):
            return self.filter(key)
        raise TypeError(f"invalid index type: {type(key)}")

    # -- Mutation -----------------------------------------------------------

    def append(self, *, t: int, l: int, b: int, r: int, z: float, clip: str, name: str) -> None:
        self._t.append(t)
        self._l.append(l)
        self._b.append(b)
        self._r.append(r)
        self._z.append(z)
        self._clip.append(clip)
        self._name.append(name)

    def extend(self, other: LayoutTable) -> None:
        self._t.extend(other._t)
        self._l.extend(other._l)
        self._b.extend(other._b)
        self._r.extend(other._r)
        self._z.extend(other._z)
        self._clip.extend(other._clip)
        self._name.extend(other._name)

    # -- Filtering ----------------------------------------------------------

    def filter(self, mask: list[bool]) -> LayoutTable:
        """Return a new LayoutTable keeping only rows where mask is True."""
        return LayoutTable(
            t=[v for v, m in zip(self._t, mask) if m],
            l=[v for v, m in zip(self._l, mask) if m],
            b=[v for v, m in zip(self._b, mask) if m],
            r=[v for v, m in zip(self._r, mask) if m],
            z=[v for v, m in zip(self._z, mask) if m],
            clip=[v for v, m in zip(self._clip, mask) if m],
            name=[v for v, m in zip(self._name, mask) if m],
        )

    # -- Bulk shifts (for add_rows/add_cols) --------------------------------

    def shift_rows(self, offset: int, after: int) -> None:
        """Shift t and b by *offset* for entries where t > after or b > after."""
        self._t = [v + offset if v > after else v for v in self._t]
        self._b = [v + offset if v > after else v for v in self._b]

    def shift_cols(self, offset: int, after: int) -> None:
        """Shift l and r by *offset* for entries where l > after or r > after."""
        self._l = [v + offset if v > after else v for v in self._l]
        self._r = [v + offset if v > after else v for v in self._r]

    # -- Copy ---------------------------------------------------------------

    def copy(self) -> LayoutTable:
        return LayoutTable(
            t=list(self._t), l=list(self._l), b=list(self._b), r=list(self._r),
            z=list(self._z), clip=list(self._clip), name=list(self._name),
        )

    # -- Repr ---------------------------------------------------------------

    def __repr__(self) -> str:
        return f"LayoutTable({len(self)} rows)"
