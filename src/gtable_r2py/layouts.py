"""Convenience layout constructors for GTable."""

from __future__ import annotations

import math

from grid_r2py import Unit, Grob, Viewport

from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob, gtable_add_cols, gtable_add_rows


def gtable_col(
    name: str,
    grobs: list[Grob],
    width: Unit | None = None,
    heights: Unit | None = None,
    z: list[float] | None = None,
    vp: Viewport | None = None,
    clip: str = "inherit",
) -> GTable:
    """Stack grobs in a single-column GTable."""
    n = len(grobs)
    if heights is None:
        heights = Unit([1] * n, "null")
    if width is None:
        width = Unit(1, "null")

    if z is not None and len(z) != n:
        raise ValueError("z must be None or same length as grobs")
    z_val = z if z is not None else [math.inf] * n

    gt = GTable(widths=width, heights=heights, name=name, vp=vp)
    gtable_add_grob(gt, grobs, t=list(range(1, n + 1)), l=[1] * n, z=z_val, clip=clip)
    return gt


def gtable_row(
    name: str,
    grobs: list[Grob],
    height: Unit | None = None,
    widths: Unit | None = None,
    z: list[float] | None = None,
    vp: Viewport | None = None,
    clip: str = "inherit",
) -> GTable:
    """Arrange grobs side-by-side in a single-row GTable."""
    n = len(grobs)
    if widths is None:
        widths = Unit([1] * n, "null")
    if height is None:
        height = Unit(1, "null")

    if z is not None and len(z) != n:
        raise ValueError("z must be None or same length as grobs")
    z_val = z if z is not None else [math.inf] * n

    gt = GTable(widths=widths, heights=height, name=name, vp=vp)
    gtable_add_grob(gt, grobs, t=[1] * n, l=list(range(1, n + 1)), z=z_val, clip=clip)
    return gt


def gtable_matrix(
    name: str,
    grobs: list[list[Grob]],
    widths: Unit,
    heights: Unit,
    z: list[list[float]] | None = None,
    respect: bool = False,
    clip: str = "on",
    vp: Viewport | None = None,
) -> GTable:
    """Create a GTable from a 2D list of grobs (row-major)."""
    nrow = len(grobs)
    ncol = len(grobs[0]) if nrow > 0 else 0

    if len(widths) != ncol:
        raise ValueError("widths must match number of columns in grobs")
    if len(heights) != nrow:
        raise ValueError("heights must match number of rows in grobs")

    # Flatten grobs and build positions (row-major)
    flat_grobs = []
    flat_t = []
    flat_l = []
    flat_z = []
    for r in range(nrow):
        for c in range(ncol):
            flat_grobs.append(grobs[r][c])
            flat_t.append(r + 1)
            flat_l.append(c + 1)
            if z is not None:
                flat_z.append(z[r][c])

    gt = GTable(widths=widths, heights=heights, name=name, respect=respect, vp=vp)
    gtable_add_grob(
        gt, flat_grobs, t=flat_t, l=flat_l,
        z=flat_z if flat_z else [math.inf] * len(flat_grobs),
        clip=clip,
    )
    return gt


def gtable_row_spacer(widths: Unit) -> GTable:
    """Create a zero-row GTable with the given column widths."""
    gt = GTable()
    gtable_add_cols(gt, widths)
    return gt


def gtable_col_spacer(heights: Unit) -> GTable:
    """Create a zero-column GTable with the given row heights."""
    gt = GTable()
    gtable_add_rows(gt, heights)
    return gt
