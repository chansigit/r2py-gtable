# Trim off empty cells.

This function detects rows and columns that does not contain any grobs
and removes thewm from the gtable. If the rows and/or columns removed
had a non-zero height/width the relative layout of the gtable may
change.

## Usage

``` r
gtable_trim(x)
```

## Arguments

- x:

  a gtable object

## Value

A gtable object

## Examples

``` r
library(grid)
rect <- rectGrob(gp = gpar(fill = "black"))
base <- gtable(unit(c(2, 2, 2), "cm"), unit(c(2, 2, 2), "cm"))

center <- gtable_add_grob(base, rect, 2, 2)
plot(center)

plot(gtable_trim(center))


col <- gtable_add_grob(base, rect, 1, 2, 3, 2)
plot(col)

plot(gtable_trim(col))


row <- gtable_add_grob(base, rect, 2, 1, 2, 3)
plot(row)

plot(gtable_trim(row))
```
