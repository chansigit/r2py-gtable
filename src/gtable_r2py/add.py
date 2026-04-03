"""Add grobs, rows, and columns to a GTable."""

from __future__ import annotations

import math

from grid_r2py import Grob, is_grob

from gtable_r2py.gtable import GTable
from gtable_r2py.utils import neg_to_pos, insert_unit, len_same_or_1


def gtable_add_grob(
    gt: GTable,
    grobs,
    t: int | list[int],
    l: int | list[int],
    b: int | list[int] | None = None,
    r: int | list[int] | None = None,
    z: float | list[float] = math.inf,
    clip: str | list[str] = "on",
    name: str | list[str] | None = None,
) -> GTable:
    """Add one or more grobs to *gt* at specified positions. Returns *gt*."""
    # Normalise grobs to list
    if is_grob(grobs):
        grobs = [grobs]
    if not isinstance(grobs, list):
        grobs = list(grobs)
    n = len(grobs)

    # Defaults
    if b is None:
        b = t
    if r is None:
        r = l
    if name is None:
        name = gt.name

    # Ensure lists
    def _as_list(x):
        return x if isinstance(x, list) else [x]

    t_list = _as_list(t)
    l_list = _as_list(l)
    b_list = _as_list(b)
    r_list = _as_list(r)
    z_list = _as_list(z)
    clip_list = _as_list(clip)
    name_list = _as_list(name)

    # Validate lengths
    for arg in (t_list, l_list, b_list, r_list, z_list, clip_list, name_list):
        if not len_same_or_1(arg, n):
            raise ValueError(
                f"All arguments must have length 1 or {n} (same as grobs)"
            )

    # Replicate length-1 to length-n
    def _rep(lst, n):
        return lst * n if len(lst) == 1 else lst

    t_list = _rep(t_list, n)
    l_list = _rep(l_list, n)
    b_list = _rep(b_list, n)
    r_list = _rep(r_list, n)
    z_list = _rep(z_list, n)
    clip_list = _rep(clip_list, n)
    name_list = _rep(name_list, n)

    # Resolve negative indices
    nrow = gt.nrow
    ncol = gt.ncol
    t_list = [neg_to_pos(v, nrow) for v in t_list]
    b_list = [neg_to_pos(v, nrow) for v in b_list]
    l_list = [neg_to_pos(v, ncol) for v in l_list]
    r_list = [neg_to_pos(v, ncol) for v in r_list]

    # Resolve z values
    existing_z = gt.layout.z
    finite_new_z = [v for v in z_list if not math.isinf(v)]
    all_z = existing_z + finite_new_z
    if len(all_z) == 0:
        zmin, zmax = 1, 0
    else:
        zmin, zmax = min(all_z), max(all_z)

    neg_inf_count = sum(1 for v in z_list if v == -math.inf)
    neg_inf_idx = 0
    pos_inf_idx = 0
    resolved_z = []
    for v in z_list:
        if v == -math.inf:
            neg_inf_idx += 1
            resolved_z.append(zmin - neg_inf_count + neg_inf_idx - 1)
        elif v == math.inf:
            pos_inf_idx += 1
            resolved_z.append(zmax + pos_inf_idx)
        else:
            resolved_z.append(v)

    # Boolean clip conversion
    clip_list = ["on" if c is True else "off" if c is False else c for c in clip_list]

    # Append to grobs and layout
    gt._grobs.extend(grobs)
    for i in range(n):
        gt.layout.append(
            t=t_list[i], l=l_list[i], b=b_list[i], r=r_list[i],
            z=resolved_z[i], clip=clip_list[i], name=name_list[i],
        )

    return gt


def gtable_add_rows(gt: GTable, heights, pos: int = -1) -> GTable:
    """Insert new rows at *pos*. Returns *gt*."""
    n = len(heights)
    pos = neg_to_pos(pos, len(gt.heights))
    gt.heights = insert_unit(gt.heights, heights, pos)
    gt.layout.shift_rows(offset=n, after=pos)
    return gt


def gtable_add_cols(gt: GTable, widths, pos: int = -1) -> GTable:
    """Insert new columns at *pos*. Returns *gt*."""
    n = len(widths)
    pos = neg_to_pos(pos, len(gt.widths))
    gt.widths = insert_unit(gt.widths, widths, pos)
    gt.layout.shift_cols(offset=n, after=pos)
    return gt


# -- GTable method wiring ---------------------------------------------------

def _add_grob_method(self, grobs, t, l, b=None, r=None, z=math.inf, clip="on", name=None):
    return gtable_add_grob(self, grobs, t, l, b, r, z, clip, name)

def _add_rows_method(self, heights, pos=-1):
    return gtable_add_rows(self, heights, pos)

def _add_cols_method(self, widths, pos=-1):
    return gtable_add_cols(self, widths, pos)

GTable.add_grob = _add_grob_method
GTable.add_rows = _add_rows_method
GTable.add_cols = _add_cols_method
