"""Row and column binding for GTable objects."""

from __future__ import annotations

from functools import reduce

from grid_r2py import unit_pmax, unit_pmin

from gtable_r2py.gtable import GTable
from gtable_r2py.layout_table import LayoutTable
from gtable_r2py.utils import insert_unit, compare_unit
from gtable_r2py.z import z_arrange_gtables


def _copy_gtable(gt: GTable) -> GTable:
    """Shallow copy of a GTable."""
    result = GTable(
        widths=gt.widths, heights=gt.heights,
        respect=gt.respect, name=gt.name,
        rownames=list(gt.rownames) if gt.rownames else None,
        colnames=list(gt.colnames) if gt.colnames else None,
    )
    result.layout = gt.layout.copy()
    result._grobs = list(gt._grobs)
    return result


def gtable_rbind(*gtables: GTable, size: str = "max", z: list | None = None) -> GTable:
    """Combine GTable objects by rows (vertically)."""
    tables = list(gtables)
    if z is not None:
        tables = z_arrange_gtables(tables, z)
    return reduce(lambda x, y: _rbind_two(x, y, size), tables)


def _rbind_two(x: GTable, y: GTable, size: str) -> GTable:
    if len(x.widths) != len(y.widths):
        raise ValueError(
            f"x and y must have the same number of columns "
            f"({len(x.widths)} vs {len(y.widths)})"
        )
    x_nrow = x.nrow
    y_nrow = y.nrow
    if x_nrow == 0:
        return _copy_gtable(y)
    if y_nrow == 0:
        return _copy_gtable(x)

    new_layout = x.layout.copy()
    y_shifted = LayoutTable(
        t=[v + x_nrow for v in y.layout.t],
        l=list(y.layout.l),
        b=[v + x_nrow for v in y.layout.b],
        r=list(y.layout.r),
        z=list(y.layout.z),
        clip=list(y.layout.clip),
        name=list(y.layout.name),
    )
    new_layout.extend(y_shifted)

    new_heights = insert_unit(x.heights, y.heights, after=len(x.heights))
    new_widths = _negotiate_size(x.widths, y.widths, size)

    new_rownames = None
    if x.rownames is not None or y.rownames is not None:
        xr = x.rownames or [None] * x_nrow
        yr = y.rownames or [None] * y_nrow
        new_rownames = list(xr) + list(yr)

    result = GTable(
        widths=new_widths, heights=new_heights,
        respect=x.respect, name=x.name,
        rownames=new_rownames, colnames=x.colnames,
    )
    result.layout = new_layout
    result._grobs = list(x._grobs) + list(y._grobs)
    return result


def gtable_cbind(*gtables: GTable, size: str = "max", z: list | None = None) -> GTable:
    """Combine GTable objects by columns (horizontally)."""
    tables = list(gtables)
    if z is not None:
        tables = z_arrange_gtables(tables, z)
    return reduce(lambda x, y: _cbind_two(x, y, size), tables)


def _cbind_two(x: GTable, y: GTable, size: str) -> GTable:
    if len(x.heights) != len(y.heights):
        raise ValueError(
            f"x and y must have the same number of rows "
            f"({len(x.heights)} vs {len(y.heights)})"
        )
    x_ncol = x.ncol
    y_ncol = y.ncol
    if x_ncol == 0:
        return _copy_gtable(y)
    if y_ncol == 0:
        return _copy_gtable(x)

    new_layout = x.layout.copy()
    y_shifted = LayoutTable(
        t=list(y.layout.t),
        l=[v + x_ncol for v in y.layout.l],
        b=list(y.layout.b),
        r=[v + x_ncol for v in y.layout.r],
        z=list(y.layout.z),
        clip=list(y.layout.clip),
        name=list(y.layout.name),
    )
    new_layout.extend(y_shifted)

    new_widths = insert_unit(x.widths, y.widths, after=len(x.widths))
    new_heights = _negotiate_size(x.heights, y.heights, size)

    new_colnames = None
    if x.colnames is not None or y.colnames is not None:
        xc = x.colnames or [None] * x_ncol
        yc = y.colnames or [None] * y_ncol
        new_colnames = list(xc) + list(yc)

    result = GTable(
        widths=new_widths, heights=new_heights,
        respect=x.respect, name=x.name,
        rownames=x.rownames, colnames=new_colnames,
    )
    result.layout = new_layout
    result._grobs = list(x._grobs) + list(y._grobs)
    return result


def _negotiate_size(x_units, y_units, size: str):
    """Resolve size conflict between two unit vectors."""
    if size == "first":
        return x_units
    elif size == "last":
        return y_units
    elif size == "max":
        return compare_unit(x_units, y_units, unit_pmax)
    elif size == "min":
        return compare_unit(x_units, y_units, unit_pmin)
    else:
        raise ValueError(f"size must be 'first', 'last', 'max', or 'min', got {size!r}")
