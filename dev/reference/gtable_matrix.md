# Create a gtable from a matrix of grobs.

This function takes a matrix of grobs and create a gtable matching with
the grobs in the same position as they were in the matrix, with the
given heights and widths.

## Usage

``` r
gtable_matrix(
  name,
  grobs,
  widths = NULL,
  heights = NULL,
  z = NULL,
  respect = FALSE,
  clip = "on",
  vp = NULL
)
```

## Arguments

- name:

  a string giving the name of the table. This is used to name the layout
  viewport

- grobs:

  a single grob or a list of grobs

- widths:

  a unit vector giving the width of each column

- heights:

  a unit vector giving the height of each row

- z:

  a numeric matrix of the same dimensions as `grobs`, specifying the
  order that the grobs are drawn.

- respect:

  a logical vector of length 1: should the aspect ratio of height and
  width specified in null units be respected. See
  [`grid.layout()`](https://rdrr.io/r/grid/grid.layout.html) for more
  details

- clip:

  should drawing be clipped to the specified cells (`"on"`), the entire
  table (`"inherit"`), or not at all (`"off"`)

- vp:

  a grid viewport object (or NULL).

## Value

A gtable of the same dimensions as the grobs matrix.

## See also

Other gtable construction:
[`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md),
[`gtable_col()`](https://gtable.r-lib.org/dev/reference/gtable_col.md),
[`gtable_row()`](https://gtable.r-lib.org/dev/reference/gtable_row.md),
[`gtable_spacer`](https://gtable.r-lib.org/dev/reference/gtable_spacer.md)

## Examples

``` r
library(grid)
a <- rectGrob(gp = gpar(fill = "red"))
b <- circleGrob()
c <- linesGrob()

row <- matrix(list(a, b, c), nrow = 1)
col <- matrix(list(a, b, c), ncol = 1)
mat <- matrix(list(a, b, c, nullGrob()), nrow = 2)

gtable_matrix("demo", row, unit(c(1, 1, 1), "null"), unit(1, "null"))
#> TableGrob (1 x 3) "demo": 3 grobs
#>   z     cells name                   grob
#> 1 1 (1-1,1-1) demo     rect[GRID.rect.48]
#> 2 2 (1-1,2-2) demo circle[GRID.circle.49]
#> 3 3 (1-1,3-3) demo   lines[GRID.lines.50]
gtable_matrix("demo", col, unit(1, "null"), unit(c(1, 1, 1), "null"))
#> TableGrob (3 x 1) "demo": 3 grobs
#>   z     cells name                   grob
#> 1 1 (1-1,1-1) demo     rect[GRID.rect.48]
#> 2 2 (2-2,1-1) demo circle[GRID.circle.49]
#> 3 3 (3-3,1-1) demo   lines[GRID.lines.50]
gtable_matrix("demo", mat, unit(c(1, 1), "null"), unit(c(1, 1), "null"))
#> TableGrob (2 x 2) "demo": 4 grobs
#>   z     cells name                   grob
#> 1 1 (1-1,1-1) demo     rect[GRID.rect.48]
#> 2 2 (2-2,1-1) demo circle[GRID.circle.49]
#> 3 3 (1-1,2-2) demo   lines[GRID.lines.50]
#> 4 4 (2-2,2-2) demo     null[GRID.null.51]

# Can specify z ordering
z <- matrix(c(3, 1, 2, 4), nrow = 2)
gtable_matrix("demo", mat, unit(c(1, 1), "null"), unit(c(1, 1), "null"), z = z)
#> TableGrob (2 x 2) "demo": 4 grobs
#>   z     cells name                   grob
#> 1 3 (1-1,1-1) demo     rect[GRID.rect.48]
#> 2 1 (2-2,1-1) demo circle[GRID.circle.49]
#> 3 2 (1-1,2-2) demo   lines[GRID.lines.50]
#> 4 4 (2-2,2-2) demo     null[GRID.null.51]
```
