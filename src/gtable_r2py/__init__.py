"""gtable-r2py: Python reimplementation of R's gtable package."""

from gtable_r2py.gtable import GTable, is_gtable, as_gtable
from gtable_r2py.layout_table import LayoutTable, LayoutRow

# Construction
from gtable_r2py.layouts import (
    gtable_col,
    gtable_row,
    gtable_matrix,
    gtable_row_spacer,
    gtable_col_spacer,
)

# Add operations
from gtable_r2py.add import (
    gtable_add_grob,
    gtable_add_rows,
    gtable_add_cols,
)

# Combine
from gtable_r2py.combine import (
    gtable_rbind,
    gtable_cbind,
)

# Modify
from gtable_r2py.modify import (
    gtable_trim,
    gtable_filter,
    gtable_add_padding,
    gtable_add_row_space,
    gtable_add_col_space,
)

# Grid integration
from gtable_r2py.grid_integration import (
    gtable_make_context,
    gtable_make_content,
    gtable_width_details,
    gtable_height_details,
    gtable_show_layout,
    gtable_width,
    gtable_height,
)


# Convenience alias: bare constructor
def gtable(widths=None, heights=None, respect=False, name="layout",
           rownames=None, colnames=None, vp=None):
    """Create a new GTable (convenience wrapper)."""
    return GTable(widths=widths, heights=heights, respect=respect,
                  name=name, rownames=rownames, colnames=colnames, vp=vp)


__all__ = [
    # Classes
    "GTable",
    "LayoutTable",
    "LayoutRow",
    # Core constructor
    "gtable",
    # Type check / conversion
    "is_gtable",
    "as_gtable",
    # Layout constructors
    "gtable_col",
    "gtable_row",
    "gtable_matrix",
    "gtable_row_spacer",
    "gtable_col_spacer",
    # Add
    "gtable_add_grob",
    "gtable_add_rows",
    "gtable_add_cols",
    # Combine
    "gtable_rbind",
    "gtable_cbind",
    # Modify
    "gtable_trim",
    "gtable_filter",
    "gtable_add_padding",
    "gtable_add_row_space",
    "gtable_add_col_space",
    # Grid integration
    "gtable_make_context",
    "gtable_make_content",
    "gtable_width_details",
    "gtable_height_details",
    "gtable_show_layout",
    "gtable_width",
    "gtable_height",
]
