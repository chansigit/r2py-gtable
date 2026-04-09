# Add padding around edges of table.

This is a convenience function for adding an extra row and an extra
column at each edge of the table.

## Usage

``` r
gtable_add_padding(x, padding)
```

## Arguments

- x:

  a [`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md)
  object

- padding:

  vector of length 4: top, right, bottom, left. Normal recycling rules
  apply.

## Value

A gtable object

## See also

Other gtable manipulation:
[`gtable_add_cols()`](https://gtable.r-lib.org/dev/reference/gtable_add_cols.md),
[`gtable_add_grob()`](https://gtable.r-lib.org/dev/reference/gtable_add_grob.md),
[`gtable_add_rows()`](https://gtable.r-lib.org/dev/reference/gtable_add_rows.md),
[`gtable_add_space`](https://gtable.r-lib.org/dev/reference/gtable_add_space.md),
[`gtable_filter()`](https://gtable.r-lib.org/dev/reference/gtable_filter.md)

## Examples

``` r
library(grid)
gt <- gtable(unit(1, "null"), unit(1, "null"))
gt <- gtable_add_grob(gt, rectGrob(gp = gpar(fill = "black")), 1, 1)

plot(gt)

plot(cbind(gt, gt))

plot(rbind(gt, gt))


pad <- gtable_add_padding(gt, unit(1, "cm"))
plot(pad)

plot(cbind(pad, pad))

plot(rbind(pad, pad))
```
