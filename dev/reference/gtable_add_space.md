# Add row/column spacing.

Adds `width` space between the columns or `height` space between the
rows, effictvely pushing the existing cells apart.

## Usage

``` r
gtable_add_col_space(x, width)

gtable_add_row_space(x, height)
```

## Arguments

- x:

  a gtable object

- width:

  a vector of units of length 1 or ncol - 1

- height:

  a vector of units of length 1 or nrow - 1

## Value

A gtable with the additional rows or columns added

## See also

Other gtable manipulation:
[`gtable_add_cols()`](https://gtable.r-lib.org/dev/reference/gtable_add_cols.md),
[`gtable_add_grob()`](https://gtable.r-lib.org/dev/reference/gtable_add_grob.md),
[`gtable_add_padding()`](https://gtable.r-lib.org/dev/reference/gtable_add_padding.md),
[`gtable_add_rows()`](https://gtable.r-lib.org/dev/reference/gtable_add_rows.md),
[`gtable_filter()`](https://gtable.r-lib.org/dev/reference/gtable_filter.md)

## Examples

``` r
library(grid)

rect <- rectGrob()
rect_mat <- matrix(rep(list(rect), 9), nrow = 3)

gt <- gtable_matrix("rects", rect_mat, widths = unit(rep(1, 3), "null"),
                    heights = unit(rep(1, 3), "null"))

plot(gt)


# Add spacing between the grobs
# same height between all rows
gt <- gtable_add_row_space(gt, unit(0.5, "cm"))

# Different width between the columns
gt <- gtable_add_col_space(gt, unit(c(0.5, 1), "cm"))

plot(gt)
```
