# Add new columns in specified position.

Insert new columns in a gtable and adjust the grob placement
accordingly. If columns are added in the middle of a grob spanning
multiple columns, the grob will continue to span them all. If a column
is added to the left or right of a grob, the grob will not span the new
column(s).

## Usage

``` r
gtable_add_cols(x, widths, pos = -1)
```

## Arguments

- x:

  a [`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md)
  object

- widths:

  a unit vector giving the widths of the new columns

- pos:

  new columns will be added to the right of this position. Defaults to
  adding col on right. `0` adds on the left.

## Value

A gtable with the new columns added.

## See also

Other gtable manipulation:
[`gtable_add_grob()`](https://gtable.r-lib.org/dev/reference/gtable_add_grob.md),
[`gtable_add_padding()`](https://gtable.r-lib.org/dev/reference/gtable_add_padding.md),
[`gtable_add_rows()`](https://gtable.r-lib.org/dev/reference/gtable_add_rows.md),
[`gtable_add_space`](https://gtable.r-lib.org/dev/reference/gtable_add_space.md),
[`gtable_filter()`](https://gtable.r-lib.org/dev/reference/gtable_filter.md)

## Examples

``` r
library(grid)
rect <- rectGrob(gp = gpar(fill = "#00000080"))
tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
dim(tab)
#> [1] 3 3
plot(tab)


# Grobs will continue to span over new rows if added in the middle
tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
dim(tab2)
#> [1] 3 4
plot(tab2)


# But not when added to left (0) or right (-1, the default)
tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
dim(tab3)
#> [1] 3 5
plot(tab3)

```
