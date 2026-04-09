# Convert to a gtable

Convert to a gtable

## Usage

``` r
as.gtable(x, ...)

# S3 method for class 'grob'
as.gtable(x, widths = NULL, heights = NULL, ...)
```

## Arguments

- x:

  An object to convert.

- ...:

  Arguments forwarded to methods.

- widths, heights:

  Scalar unit setting the size of the table. Defaults to
  [`grid::grobWidth()`](https://rdrr.io/r/grid/grobWidth.html) and
  [`grid::grobHeight()`](https://rdrr.io/r/grid/grobWidth.html) of `x`
  respectively.

## Value

A gtable object

## Methods (by class)

- `as.gtable(grob)`: Creates a 1-cell gtable containing the grob.
