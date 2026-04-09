# Package index

## Construction

- [`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md) :
  Create a new grob table.
- [`gtable_matrix()`](https://gtable.r-lib.org/dev/reference/gtable_matrix.md)
  : Create a gtable from a matrix of grobs.
- [`gtable_col()`](https://gtable.r-lib.org/dev/reference/gtable_col.md)
  : Create a single column gtable
- [`gtable_row()`](https://gtable.r-lib.org/dev/reference/gtable_row.md)
  : Create a single row gtable.
- [`gtable_row_spacer()`](https://gtable.r-lib.org/dev/reference/gtable_spacer.md)
  [`gtable_col_spacer()`](https://gtable.r-lib.org/dev/reference/gtable_spacer.md)
  : Create a row/col spacer gtable.
- [`as.gtable()`](https://gtable.r-lib.org/dev/reference/as.gtable.md) :
  Convert to a gtable

## Modification

- [`gtable_add_grob()`](https://gtable.r-lib.org/dev/reference/gtable_add_grob.md)
  : Add a single grob, possibly spanning multiple rows or columns.
- [`gtable_add_cols()`](https://gtable.r-lib.org/dev/reference/gtable_add_cols.md)
  : Add new columns in specified position.
- [`gtable_add_rows()`](https://gtable.r-lib.org/dev/reference/gtable_add_rows.md)
  : Add new rows in specified position.
- [`gtable_add_padding()`](https://gtable.r-lib.org/dev/reference/gtable_add_padding.md)
  : Add padding around edges of table.
- [`gtable_add_col_space()`](https://gtable.r-lib.org/dev/reference/gtable_add_space.md)
  [`gtable_add_row_space()`](https://gtable.r-lib.org/dev/reference/gtable_add_space.md)
  : Add row/column spacing.
- [`gtable_trim()`](https://gtable.r-lib.org/dev/reference/gtable_trim.md)
  : Trim off empty cells.
- [`gtable_filter()`](https://gtable.r-lib.org/dev/reference/gtable_filter.md)
  : Filter cells by name

## Combining

- [`rbind(`*`<gtable>`*`)`](https://gtable.r-lib.org/dev/reference/bind.md)
  [`cbind(`*`<gtable>`*`)`](https://gtable.r-lib.org/dev/reference/bind.md)
  : Row and column binding for gtables.

## Inspection

- [`is.gtable()`](https://gtable.r-lib.org/dev/reference/is.gtable.md) :
  Is this a gtable?
- [`print(`*`<gtable>`*`)`](https://gtable.r-lib.org/dev/reference/print.gtable.md)
  : Print a gtable object
- [`gtable_show_layout()`](https://gtable.r-lib.org/dev/reference/gtable_show_layout.md)
  : Visualise the layout of a gtable.
- [`gtable_height()`](https://gtable.r-lib.org/dev/reference/gtable_height.md)
  : Returns the height of a gtable, in the gtable's units
- [`gtable_width()`](https://gtable.r-lib.org/dev/reference/gtable_width.md)
  : Returns the width of a gtable, in the gtable's units
