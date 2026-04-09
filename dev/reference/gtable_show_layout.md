# Visualise the layout of a gtable.

This function is a simple wrapper around
[`grid::grid.show.layout()`](https://rdrr.io/r/grid/grid.show.layout.html)
that allows you to inspect the layout of the gtable.

## Usage

``` r
gtable_show_layout(x, ...)
```

## Arguments

- x:

  a gtable object

- ...:

  Arguments passed on to
  [`grid::grid.show.layout`](https://rdrr.io/r/grid/grid.show.layout.html)

  `l`

  :   A Grid layout object.

  `newpage`

  :   A logical value indicating whether to move on to a new page before
      drawing the diagram.

  `vp.ex`

  :   positive number, typically in \\(0,1\]\\, specifying the scaling
      of the layout.

  `bg`

  :   The colour used for the background.

  `cell.border`

  :   The colour used to draw the borders of the cells in the layout.

  `cell.fill`

  :   The colour used to fill the cells in the layout.

  `cell.label`

  :   A logical indicating whether the layout cells should be labelled.

  `label.col`

  :   The colour used for layout cell labels.

  `unit.col`

  :   The colour used for labelling the widths/heights of columns/rows.

  `vp`

  :   A Grid viewport object (or NULL).

## Examples

``` r
gt <- gtable(widths = grid::unit(c(1, 0.5, 2), c("null", "cm", "null")),
             heights = grid::unit(c(0.2, 1, 3), c("inch", "null", "cm")))
gtable_show_layout(gt)

```
