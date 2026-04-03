"""Z-order management (internal)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gtable_r2py.gtable import GTable


def z_normalise(gt: GTable, start: int = 1) -> GTable:
    """Renumber z values to consecutive integers starting at *start*."""
    layout = gt.layout
    if len(layout) == 0:
        return gt
    z_vals = layout.z
    sorted_indices = sorted(range(len(z_vals)), key=lambda i: (z_vals[i], i))
    ranks = [0] * len(z_vals)
    for rank, idx in enumerate(sorted_indices):
        ranks[idx] = rank + start
    layout._z = ranks
    return gt


def z_arrange_gtables(gtables: list[GTable], z: list[int | float]) -> list[GTable]:
    """Normalise z values across multiple gtables according to relative *z* ordering."""
    if len(gtables) != len(z):
        raise ValueError("gtables and z must be the same length")
    zmax = 0
    for i in sorted(range(len(z)), key=lambda i: z[i]):
        if len(gtables[i].layout) > 0:
            z_normalise(gtables[i], zmax + 1)
            zmax = max(gtables[i].layout.z)
    return gtables
