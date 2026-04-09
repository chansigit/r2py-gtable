# Changelog

## gtable (development version)

## gtable 0.3.6

CRAN release: 2024-10-25

- Added
  [`as.gtable()`](https://gtable.r-lib.org/dev/reference/as.gtable.md)
  S3 method ([\#97](https://github.com/r-lib/gtable/issues/97)).
- Add `clip` argument to
  [`gtable_col()`](https://gtable.r-lib.org/dev/reference/gtable_col.md)
  and
  [`gtable_row()`](https://gtable.r-lib.org/dev/reference/gtable_row.md)
  ([\#56](https://github.com/r-lib/gtable/issues/56))
- Indexing a gtable with `NA` will now insert a zero-dimension
  row/column at the position of the `NA`-index
  ([\#13](https://github.com/r-lib/gtable/issues/13))

## gtable 0.3.5

CRAN release: 2024-04-22

- Fixed partial matching issue when constructing viewport in
  [`gtable()`](https://gtable.r-lib.org/dev/reference/gtable.md)
  ([\#94](https://github.com/r-lib/gtable/issues/94))
- General upkeep

## gtable 0.3.4

CRAN release: 2023-08-21

- Fix package doc links

## gtable 0.3.3

CRAN release: 2023-03-21

- Specify minimum rlang version

## gtable 0.3.2

CRAN release: 2023-03-17

- General upkeep

## gtable 0.3.1

CRAN release: 2022-09-01

- Re-documented to fix HTML issues in `.Rd`.

- gtable has been re-licensed as MIT
  ([\#85](https://github.com/r-lib/gtable/issues/85)).

## gtable 0.3.0

CRAN release: 2019-03-25

- Made a range of internal changes to increase performance of gtable
  construction, these include:

  - Use more performant `data.frame` constructor .
  - Treat layout data.frame as list when indexing and modifying it.
  - Use length of `widths` and `heights` fields instead of
    [`ncol()`](https://rdrr.io/r/base/nrow.html) and
    [`nrow()`](https://rdrr.io/r/base/nrow.html) internally.
  - Substitute `stopifnot(...)` with `if(!...) stop()`.

- Better documentation, including a new README, a vignette on
  performance profiling and a pkgdown site.

- New logo

- It is now an error to index into a gtable with non-increasing indices.

- Dimnames are now inherited from the grobs data in
  [`gtable_col()`](https://gtable.r-lib.org/dev/reference/gtable_col.md),
  [`gtable_row()`](https://gtable.r-lib.org/dev/reference/gtable_row.md),
  and
  [`gtable_matrix()`](https://gtable.r-lib.org/dev/reference/gtable_matrix.md)

- `gtable_trim` now works with empty gtables

- `gtable_filter` now has an invert argument to remove grops matching a
  name.

## gtable 0.2.0

CRAN release: 2016-02-26

- Switch from
  [`preDrawDetails()`](https://rdrr.io/r/grid/drawDetails.html) and
  [`postDrawDetails()`](https://rdrr.io/r/grid/drawDetails.html) methods
  to [`makeContent()`](https://rdrr.io/r/grid/makeContent.html) and
  [`makeContext()`](https://rdrr.io/r/grid/makeContent.html) methods
  ([@pmur002](https://github.com/pmur002),
  [\#50](https://github.com/r-lib/gtable/issues/50)). This is a better
  approach facilitiated by changes in grid. Learn more at
  <https://journal.r-project.org/archive/2013-2/murrell.pdf>.

- Added a `NEWS.md` file to track changes to the package.

- Partial argument matches have been fixed.

- Import grid instead of depending on it.

## gtable 0.1.2

CRAN release: 2012-12-05

- `print.gtable` now prints the z order of the grobs, and it no longer
  sort the names by z order. Previously, the layout names were sorted by
  z order, but the grobs weren’t. This resulted in a mismatch between
  the names and the grobs. It’s better to not sort by z by default,
  since that doesn’t match how indexing works. The `zsort` option allows
  the output to be sorted by z.
