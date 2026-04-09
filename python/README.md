# gtable-r2py

Python reimplementation of R's [gtable](https://gtable.r-lib.org) package — a layout engine built on top of `grid` for arranging graphical objects (grobs) in a table-based grid.

## Installation

```bash
pip install gtable-r2py
```

**Requires:** Python >= 3.10, [grid-r2py](https://github.com/chansigit/grid-r2py) >= 0.1.0

## Quick start

```python
from grid_r2py import Unit, RectGrob, CircleGrob

from gtable_r2py import (
    gtable, gtable_add_grob, gtable_add_rows, gtable_add_cols,
    gtable_rbind, gtable_cbind, gtable_trim, gtable_filter,
)

# Create an empty 2x3 table
gt = gtable(
    widths=Unit([1, 2, 1], "cm"),
    heights=Unit([1, 1], "cm"),
    name="demo",
)
gt
# TableGrob (2 x 3) 'demo': 0 grobs

# Add grobs at specific cells
rect = RectGrob(name="rect")
circ = CircleGrob(name="circ")
gtable_add_grob(gt, rect, t=1, l=1)           # top-left cell
gtable_add_grob(gt, circ, t=1, l=2, r=3)      # top row, spans columns 2-3

len(gt)  # 2 grobs
```

## Core concepts

A `GTable` is a `GTree` subclass that holds:

- **`widths`** / **`heights`** — `Unit` vectors defining column widths and row heights
- **`layout`** — a `LayoutTable` tracking each grob's position (t, l, b, r), z-order, clip mode, and name
- **`_grobs`** — a list of grobs placed in the table

Grobs can span multiple rows/columns, and GTable objects can be nested.

## API reference

### Construction

| Function | Description |
|----------|-------------|
| `gtable(widths, heights, ...)` | Create an empty GTable |
| `gtable_col(name, grobs, ...)` | Stack grobs vertically in a single column |
| `gtable_row(name, grobs, ...)` | Arrange grobs side-by-side in a single row |
| `gtable_matrix(name, grobs, widths, heights, ...)` | 2D grid from a row-major list of lists |
| `gtable_row_spacer(widths)` | Zero-row GTable (column spacer) |
| `gtable_col_spacer(heights)` | Zero-column GTable (row spacer) |

### Adding grobs, rows, and columns

| Function | Description |
|----------|-------------|
| `gtable_add_grob(gt, grobs, t, l, b=None, r=None, z=inf, clip="on", name=None)` | Add one or more grobs at specified cell positions |
| `gtable_add_rows(gt, heights, pos=-1)` | Insert new rows at position |
| `gtable_add_cols(gt, widths, pos=-1)` | Insert new columns at position |

Positions use **1-based indexing** (matching R convention). Negative indices count from the end.

### Combining tables

| Function | Description |
|----------|-------------|
| `gtable_rbind(*gtables, size="max")` | Stack tables vertically (must have same number of columns) |
| `gtable_cbind(*gtables, size="max")` | Join tables horizontally (must have same number of rows) |

The `size` parameter controls how dimension conflicts are resolved: `"first"`, `"last"`, `"max"`, or `"min"`.

### Modifying tables

| Function | Description |
|----------|-------------|
| `gtable_trim(gt)` | Remove empty rows and columns (returns new GTable) |
| `gtable_filter(gt, pattern, fixed=False, trim=True, invert=False)` | Subset grobs by name pattern (returns new GTable) |
| `gtable_add_padding(gt, padding)` | Add padding around edges — Unit of length 1 (uniform) or 4 (CSS order: top, right, bottom, left) |
| `gtable_add_row_space(gt, height)` | Insert spacing between rows |
| `gtable_add_col_space(gt, width)` | Insert spacing between columns |

### Grid integration

| Function | Description |
|----------|-------------|
| `gtable_make_context(gt)` | Set up the layout viewport for rendering |
| `gtable_make_content(gt)` | Wrap grobs in viewport-bearing GTrees, sorted by z-order |
| `gtable_width(gt)` / `gtable_height(gt)` | Total width/height as a Unit |
| `gtable_show_layout(gt)` | Visualise the table layout |

### Type checking

| Function | Description |
|----------|-------------|
| `is_gtable(x)` | Check if `x` is a GTable |
| `as_gtable(x, widths=None, heights=None)` | Convert a grob to a 1x1 GTable |

### GTable methods

Most functions are also available as methods on GTable instances:

```python
gt.add_grob(grob, t=1, l=1)
gt.add_rows(Unit([1], "cm"))
gt.add_cols(Unit([1], "cm"))
gt.trim()
gt.filter("panel")
gt.add_padding(Unit(0.5, "cm"))
gt.add_row_space(Unit(0.2, "cm"))
gt.add_col_space(Unit(0.2, "cm"))
gt.transpose()
gt.make_context()
gt.make_content()
gt.show_layout()
```

### Subsetting

GTable supports matrix-style indexing with `[rows, cols]`:

```python
# By integer (0-based Python convention)
sub = gt[0, 0]          # first row, first column
sub = gt[0:2, :]        # first two rows, all columns

# By name (requires rownames/colnames set)
gt.rownames = ["top", "bottom"]
sub = gt["top", :]
```

## Examples

### Building a plot layout from scratch

```python
from grid_r2py import Unit, PointsGrob, NullGrob

from gtable_r2py import (
    gtable, gtable_add_grob, gtable_add_padding,
    gtable_add_row_space, gtable_add_col_space,
)

# Set up a 2x2 grid
gt = gtable(
    widths=Unit([1, 1], "null"),
    heights=Unit([1, 1], "null"),
    name="plot_grid",
)

# Place grobs in each cell
for r in range(1, 3):
    for c in range(1, 3):
        grob = PointsGrob(name=f"panel-{r}-{c}")
        gtable_add_grob(gt, grob, t=r, l=c)

# Add spacing and padding
gtable_add_row_space(gt, Unit(0.5, "cm"))
gtable_add_col_space(gt, Unit(0.5, "cm"))
gtable_add_padding(gt, Unit(1, "cm"))

gt
# TableGrob (5 x 5) 'plot_grid': 4 grobs
```

### Combining tables

```python
from grid_r2py import Unit, RectGrob

from gtable_r2py import gtable_col, gtable_row, gtable_rbind, gtable_cbind

# Create two single-column tables
left = gtable_col("left", [RectGrob(name="a"), RectGrob(name="b")])
right = gtable_col("right", [RectGrob(name="c"), RectGrob(name="d")])

# Join horizontally
combined = gtable_cbind(left, right)
combined
# TableGrob (2 x 2) 'left': 4 grobs
```

### Filtering and trimming

```python
from gtable_r2py import gtable_filter

# Keep only grobs whose names match a regex
panels_only = gtable_filter(gt, r"panel")

# Invert: remove matching grobs
no_panels = gtable_filter(gt, r"panel", invert=True)
```

## Relationship to R's gtable

This package is a faithful port of [r-lib/gtable](https://github.com/r-lib/gtable) (v0.3.6). Key differences from the R version:

| Aspect | R (gtable) | Python (gtable-r2py) |
|--------|-----------|----------------------|
| Indexing | 1-based throughout | Cell positions are 1-based; Python `__getitem__` is 0-based |
| Mutability | Copy-on-modify (R semantics) | In-place mutation for add/modify operations; trim/filter return new objects |
| Dependencies | grid, rlang, cli | grid-r2py |
| Not ported | `gtable_align` / `gtable_join` | Marked as non-functional in R source; omitted |
