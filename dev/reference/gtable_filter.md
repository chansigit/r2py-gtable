# Filter cells by name

Normally a gtable is considered a matrix when indexing so that indexing
is working on the cell layout and not on the grobs it contains.
`gtable_filter` allows you to subset the grobs by name and optionally
remove rows or columns if left empty after the subsetting

## Usage

``` r
gtable_filter(x, pattern, fixed = FALSE, trim = TRUE, invert = FALSE)
```

## Arguments

- x:

  a gtable object

- pattern:

  character string containing a [regular
  expression](https://rdrr.io/r/base/regex.html) (or character string
  for `fixed = TRUE`) to be matched in the given character vector.
  Coerced by [`as.character`](https://rdrr.io/r/base/character.html) to
  a character string if possible. If a character vector of length 2 or
  more is supplied, the first element is used with a warning. Missing
  values are allowed except for `regexpr`, `gregexpr` and `regexec`.

- fixed:

  logical. If `TRUE`, `pattern` is a string to be matched as is.
  Overrides all conflicting arguments.

- trim:

  if `TRUE`,
  [`gtable_trim()`](https://gtable.r-lib.org/dev/reference/gtable_trim.md)
  will be used to trim off any empty cells.

- invert:

  Should the filtering be inverted so that cells matching `pattern` is
  removed instead of kept.

## Value

A gtable only containing the matching grobs, potentially stripped of
empty columns and rows

## See also

Other gtable manipulation:
[`gtable_add_cols()`](https://gtable.r-lib.org/dev/reference/gtable_add_cols.md),
[`gtable_add_grob()`](https://gtable.r-lib.org/dev/reference/gtable_add_grob.md),
[`gtable_add_padding()`](https://gtable.r-lib.org/dev/reference/gtable_add_padding.md),
[`gtable_add_rows()`](https://gtable.r-lib.org/dev/reference/gtable_add_rows.md),
[`gtable_add_space`](https://gtable.r-lib.org/dev/reference/gtable_add_space.md)

## Examples

``` r
library(grid)
gt <- gtable(unit(rep(5, 3), c("cm")), unit(5, "cm"))
rect <- rectGrob(gp = gpar(fill = "black"))
circ <- circleGrob(gp = gpar(fill = "red"))

gt <- gtable_add_grob(gt, rect, 1, 1, name = "rect")
gt <- gtable_add_grob(gt, circ, 1, 3, name = "circ")

plot(gtable_filter(gt, "rect"))

plot(gtable_filter(gt, "rect", trim = FALSE))

plot(gtable_filter(gt, "circ"))

plot(gtable_filter(gt, "circ", trim = FALSE))

```
