"""GTable: table-based layout grob container."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from grid_r2py import GTree, GList, Grob, Unit, Viewport, is_grob
from grid_r2py import grob_width, grob_height, unit_c

from gtable_r2py.layout_table import LayoutTable

if TYPE_CHECKING:
    pass


class GTable(GTree):
    """A table-based layout engine for arranging grobs in rows and columns.

    Extends GTree. Grobs are stored in ``self._grobs`` (a plain list) alongside
    a ``self.layout`` (LayoutTable) that tracks each grob's position.
    GTree's ``self.children`` is set during ``make_content()`` for rendering.
    """

    def __init__(
        self,
        widths: Unit | None = None,
        heights: Unit | None = None,
        respect: bool = False,
        name: str = "layout",
        rownames: list[str] | None = None,
        colnames: list[str] | None = None,
        vp: Viewport | None = None,
    ) -> None:
        super().__init__(name=name, vp=vp)
        self.widths: Unit = widths if widths is not None else Unit([], "cm")
        self.heights: Unit = heights if heights is not None else Unit([], "cm")
        self.respect: bool = respect
        self.rownames: list[str] | None = list(rownames) if rownames is not None else None
        self.colnames: list[str] | None = list(colnames) if colnames is not None else None
        self.layout: LayoutTable = LayoutTable()
        self._grobs: list[Grob] = []
        # Stash the user-supplied vp so make_context can rebuild idempotently.
        self._user_vp = vp

    # -- Dimensions ---------------------------------------------------------

    @property
    def nrow(self) -> int:
        return len(self.heights)

    @property
    def ncol(self) -> int:
        return len(self.widths)

    def dim(self) -> tuple[int, int]:
        return (self.nrow, self.ncol)

    def __len__(self) -> int:
        """Number of grobs."""
        return len(self._grobs)

    # -- Size queries -------------------------------------------------------

    def total_width(self) -> Unit:
        """Sum of column widths."""
        if len(self.widths) == 0:
            return Unit(0, "cm")
        result = self.widths[0]
        for i in range(1, len(self.widths)):
            result = result + self.widths[i]
        return result

    def total_height(self) -> Unit:
        """Sum of row heights."""
        if len(self.heights) == 0:
            return Unit(0, "cm")
        result = self.heights[0]
        for i in range(1, len(self.heights)):
            result = result + self.heights[i]
        return result

    # -- Repr ---------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"TableGrob ({self.nrow} x {self.ncol}) "
            f"'{self.name}': {len(self)} grobs"
        )

    # -- Transpose ----------------------------------------------------------

    def transpose(self) -> GTable:
        """Swap rows and columns in-place. Returns self."""
        old_t = list(self.layout.t)
        old_l = list(self.layout.l)
        old_b = list(self.layout.b)
        old_r = list(self.layout.r)
        self.layout._t = old_l
        self.layout._l = old_t
        self.layout._b = old_r
        self.layout._r = old_b
        self.widths, self.heights = self.heights, self.widths
        return self

    # -- Subsetting ---------------------------------------------------------

    def __getitem__(self, key):
        """Matrix-style subsetting: gt[rows, cols]."""
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("GTable subsetting requires [rows, cols]")
        row_key, col_key = key
        return self._subset(row_key, col_key)

    def _resolve_index(self, key, size: int, names: list[str] | None) -> list[int]:
        """Resolve a row/col key to a list of 1-based indices."""
        if isinstance(key, slice):
            indices = range(*key.indices(size))
            return [i + 1 for i in indices]
        if isinstance(key, int):
            if key < 0:
                key = size + key
            return [key + 1]  # convert to 1-based
        if isinstance(key, str):
            if names is None:
                raise KeyError(f"no names to match '{key}'")
            return [names.index(key) + 1]
        if isinstance(key, (list, range)):
            result = []
            for k in key:
                result.extend(self._resolve_index(k, size, names))
            return result
        raise TypeError(f"invalid index type: {type(key)}")

    def _subset(self, row_key, col_key) -> GTable:
        """Subset this gtable by rows and columns. Returns a new GTable."""
        rows = self._resolve_index(row_key, self.nrow, self.rownames)
        cols = self._resolve_index(col_key, self.ncol, self.colnames)

        rows_set = set(rows)
        cols_set = set(cols)

        # Keep grobs whose full extent is within the selection
        keep = []
        for i in range(len(self.layout)):
            row_i = self.layout[i]
            in_rows = all(r in rows_set for r in range(row_i.t, row_i.b + 1))
            in_cols = all(c in cols_set for c in range(row_i.l, row_i.r + 1))
            keep.append(in_rows and in_cols)

        # Build index remapping (old 1-based -> new 1-based)
        sorted_rows = sorted(rows)
        sorted_cols = sorted(cols)
        row_map = {old: new for new, old in enumerate(sorted_rows, 1)}
        col_map = {old: new for new, old in enumerate(sorted_cols, 1)}

        # Build new heights/widths using unit_c
        new_heights = unit_c(*(self.heights[r - 1] for r in sorted_rows)) if sorted_rows else Unit([], "cm")
        new_widths = unit_c(*(self.widths[c - 1] for c in sorted_cols)) if sorted_cols else Unit([], "cm")

        new_rownames = [self.rownames[r - 1] for r in sorted_rows] if self.rownames else None
        new_colnames = [self.colnames[c - 1] for c in sorted_cols] if self.colnames else None

        # Build new layout and grobs
        new_layout = LayoutTable()
        new_grobs = []
        for i in range(len(self.layout)):
            if keep[i]:
                row_i = self.layout[i]
                new_layout.append(
                    t=row_map[row_i.t], l=col_map[row_i.l],
                    b=row_map[row_i.b], r=col_map[row_i.r],
                    z=row_i.z, clip=row_i.clip, name=row_i.name,
                )
                new_grobs.append(self._grobs[i])

        result = GTable(
            widths=new_widths, heights=new_heights,
            respect=self.respect, name=self.name,
            rownames=new_rownames, colnames=new_colnames,
        )
        result.layout = new_layout
        result._grobs = new_grobs
        return result


# -- Module-level functions -------------------------------------------------


def is_gtable(x) -> bool:
    """Return True if *x* is a GTable instance."""
    return isinstance(x, GTable)


def as_gtable(x, widths: Unit | None = None, heights: Unit | None = None) -> GTable:
    """Convert *x* to a GTable.

    - GTable passes through unchanged.
    - A single Grob is wrapped in a 1x1 GTable.
    - Everything else raises TypeError.
    """
    if isinstance(x, GTable):
        return x
    if is_grob(x):
        w = widths if widths is not None else grob_width(x)
        h = heights if heights is not None else grob_height(x)
        from gtable_r2py.add import gtable_add_grob
        gt = GTable(widths=w, heights=h)
        gtable_add_grob(gt, x, t=1, l=1)
        return gt
    raise TypeError(f"Cannot convert {type(x).__name__} to GTable")
