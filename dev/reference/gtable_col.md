# Create a single column gtable

This function stacks a list of grobs into a single column gtable of the
given width and heights.

## Usage

``` r
gtable_col(
  name,
  grobs,
  width = NULL,
  heights = NULL,
  z = NULL,
  vp = NULL,
  clip = "inherit"
)
```

## Arguments

- name:

  a string giving the name of the table. This is used to name the layout
  viewport

- grobs:

  a single grob or a list of grobs

- width:

  a unit vector giving the width of this column

- heights:

  a unit vector giving the height of each row

- z:

  a numeric vector giving the order in which the grobs should be
  plotted. Use `Inf` (the default) to plot above or `-Inf` below all
  existing grobs. By default positions are on the integers, giving
  plenty of room to insert new grobs between existing grobs.

- vp:

  a grid viewport object (or NULL).

- clip:

  should drawing be clipped to the specified cells (`"on"`), the entire
  table (`"inherit"`), or not at all (`"off"`)

## Value

A gtable with one column and as many rows as elements in the grobs list.

## See also

Other gtable construction:
[`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md),
[`gtable_matrix()`](https://gtable.r-lib.org/dev/reference/gtable_matrix.md),
[`gtable_row()`](https://gtable.r-lib.org/dev/reference/gtable_row.md),
[`gtable_spacer`](https://gtable.r-lib.org/dev/reference/gtable_spacer.md)

## Examples

``` r
library(grid)
a <- rectGrob(gp = gpar(fill = "red"))
b <- circleGrob()
c <- linesGrob()
gt <- gtable_col("demo", list(a, b, c))
gt
#> TableGrob (3 x 1) "demo": 3 grobs
#>   z     cells name                   grob
#> 1 1 (1-1,1-1) demo     rect[GRID.rect.27]
#> 2 2 (2-2,1-1) demo circle[GRID.circle.28]
#> 3 3 (3-3,1-1) demo   lines[GRID.lines.29]
plot(gt)

gtable_show_layout(gt)
```
