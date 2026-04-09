"""Modification operations for GTable: trim, filter, padding, spacing."""

from __future__ import annotations

import re

from grid_r2py import Unit

from gtable_r2py.gtable import GTable
from gtable_r2py.layout_table import LayoutTable
from gtable_r2py.add import gtable_add_rows, gtable_add_cols
from gtable_r2py.utils import unit_slice


def gtable_trim(gt: GTable) -> GTable:
    """Remove empty rows and columns, returning a new GTable."""
    if len(gt) == 0:
        return GTable(respect=gt.respect, name=gt.name, vp=gt.vp)

    layout = gt.layout
    col_min = min(min(layout.l), min(layout.r))
    col_max = max(max(layout.l), max(layout.r))
    row_min = min(min(layout.t), min(layout.b))
    row_max = max(max(layout.t), max(layout.b))

    new_widths = unit_slice(gt.widths, col_min - 1, col_max)
    new_heights = unit_slice(gt.heights, row_min - 1, row_max)

    new_layout = LayoutTable(
        t=[v - row_min + 1 for v in layout.t],
        l=[v - col_min + 1 for v in layout.l],
        b=[v - row_min + 1 for v in layout.b],
        r=[v - col_min + 1 for v in layout.r],
        z=list(layout.z),
        clip=list(layout.clip),
        name=list(layout.name),
    )

    result = GTable(
        widths=new_widths, heights=new_heights,
        respect=gt.respect, name=gt.name,
    )
    result.layout = new_layout
    result._grobs = list(gt._grobs)
    return result


def gtable_filter(
    gt: GTable,
    pattern: str,
    fixed: bool = False,
    trim: bool = True,
    invert: bool = False,
) -> GTable:
    """Subset grobs by name pattern, returning a new GTable."""
    names = gt.layout.name
    if fixed:
        matches = [pattern in n for n in names]
    else:
        matches = [bool(re.search(pattern, n)) for n in names]

    if invert:
        matches = [not m for m in matches]

    new_layout = gt.layout.filter(matches)
    new_grobs = [g for g, m in zip(gt._grobs, matches) if m]

    result = GTable(
        widths=gt.widths, heights=gt.heights,
        respect=gt.respect, name=gt.name,
    )
    result.layout = new_layout
    result._grobs = new_grobs

    if trim:
        result = gtable_trim(result)

    return result


def gtable_add_padding(gt: GTable, padding) -> GTable:
    """Add padding around table edges. Returns *gt*.

    *padding* is a Unit of length 1 (uniform) or 4 (CSS order: top, right,
    bottom, left).
    """
    # padding can be a Unit of length 1 or 4; replicate to length 4
    if len(padding) == 1:
        p = [padding] * 4
    else:
        p = [padding[i % len(padding)] for i in range(4)]

    gtable_add_rows(gt, p[0], pos=0)        # top
    gtable_add_cols(gt, p[1], pos=-1)        # right
    gtable_add_rows(gt, p[2], pos=-1)        # bottom
    gtable_add_cols(gt, p[3], pos=0)         # left
    return gt


def gtable_add_row_space(gt: GTable, height) -> GTable:
    """Insert spacing between rows. Returns *gt*."""
    n = gt.nrow - 1
    if n <= 0:
        return gt

    if len(height) == 1:
        heights = [height] * n
    elif len(height) == n:
        heights = [height[i] for i in range(n)]
    else:
        raise ValueError(f"height must be length 1 or nrow-1 ({n})")

    for i in reversed(range(n)):
        gtable_add_rows(gt, heights[i], pos=i + 1)

    return gt


def gtable_add_col_space(gt: GTable, width) -> GTable:
    """Insert spacing between columns. Returns *gt*."""
    n = gt.ncol - 1
    if n <= 0:
        return gt

    if len(width) == 1:
        widths = [width] * n
    elif len(width) == n:
        widths = [width[i] for i in range(n)]
    else:
        raise ValueError(f"width must be length 1 or ncol-1 ({n})")

    for i in reversed(range(n)):
        gtable_add_cols(gt, widths[i], pos=i + 1)

    return gt


# -- GTable method wiring ---------------------------------------------------

def _trim_method(self):
    return gtable_trim(self)

def _filter_method(self, pattern, fixed=False, trim=True, invert=False):
    return gtable_filter(self, pattern, fixed, trim, invert)

def _add_padding_method(self, padding):
    return gtable_add_padding(self, padding)

def _add_row_space_method(self, height):
    return gtable_add_row_space(self, height)

def _add_col_space_method(self, width):
    return gtable_add_col_space(self, width)

GTable.trim = _trim_method
GTable.filter = _filter_method
GTable.add_padding = _add_padding_method
GTable.add_row_space = _add_row_space_method
GTable.add_col_space = _add_col_space_method
