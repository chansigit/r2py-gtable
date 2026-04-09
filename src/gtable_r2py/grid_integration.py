"""Grid integration: make_context, make_content, dimension details, show_layout."""

from __future__ import annotations

from grid_r2py import (
    GTree, GList, Viewport, Layout, Unit,
    set_children,
)
from grid_r2py.vp_collections import VpStack
from grid_r2py import show_layout as grid_show_layout

from gtable_r2py.gtable import GTable


def _gtable_layout(gt: GTable) -> Layout:
    """Create a grid Layout from a GTable's dimensions."""
    return Layout(
        nrow=gt.nrow,
        ncol=gt.ncol,
        widths=gt.widths,
        heights=gt.heights,
        respect=gt.respect,
    )


def _vpname(layout_row) -> str:
    """Generate viewport name from a layout row: 'name.t-r-b-l'."""
    return f"{layout_row.name}.{layout_row.t}-{layout_row.r}-{layout_row.b}-{layout_row.l}"


def gtable_make_context(gt: GTable) -> GTable:
    """Set up the layout viewport for rendering. Modifies *gt* in place.

    Idempotent: always rebuilds from the original user-supplied vp stored in
    ``gt._user_vp``, so repeated calls (e.g. during redraws) do not nest
    viewports deeper each time.
    """
    layout_vp = Viewport(
        layout=_gtable_layout(gt),
        name=gt.name,
    )
    user_vp = gt._user_vp
    if user_vp is None:
        gt.vp = layout_vp
    else:
        gt.vp = VpStack([user_vp, layout_vp])
    return gt


def gtable_make_content(gt: GTable) -> GTable:
    """Wrap each grob in a viewport-bearing GTree, sorted by z. Modifies *gt*."""
    if len(gt) == 0:
        set_children(gt, [])
        return gt

    layout = gt.layout

    children_with_z = []
    for i in range(len(layout)):
        row = layout[i]
        vp_name = _vpname(row)
        child_vp = Viewport(
            name=vp_name,
            layout_pos_row=(row.t, row.b),
            layout_pos_col=(row.l, row.r),
            clip=row.clip,
        )
        child_tree = GTree(
            children=[gt._grobs[i]],
            name=vp_name,
            vp=child_vp,
        )
        children_with_z.append((row.z, i, child_tree))

    children_with_z.sort(key=lambda x: (x[0], x[1]))
    sorted_children = [c for _, _, c in children_with_z]

    set_children(gt, sorted_children)
    return gt


def gtable_width_details(gt: GTable) -> Unit:
    """Return the total width of the GTable."""
    return gt.total_width()


def gtable_height_details(gt: GTable) -> Unit:
    """Return the total height of the GTable."""
    return gt.total_height()


def gtable_width(gt: GTable) -> Unit:
    """Return the total width of *gt* (sum of column widths)."""
    return gt.total_width()


def gtable_height(gt: GTable) -> Unit:
    """Return the total height of *gt* (sum of row heights)."""
    return gt.total_height()


def gtable_show_layout(gt: GTable, **kwargs) -> None:
    """Visualise the layout of a GTable."""
    layout = _gtable_layout(gt)
    grid_show_layout(layout, **kwargs)


# -- GTable method wiring ---------------------------------------------------

def _make_context_method(self):
    return gtable_make_context(self)

def _make_content_method(self):
    return gtable_make_content(self)

GTable.make_context = _make_context_method
GTable.make_content = _make_content_method

def _show_layout_method(self, **kwargs):
    return gtable_show_layout(self, **kwargs)

GTable.show_layout = _show_layout_method
