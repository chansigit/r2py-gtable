import pytest
from grid_r2py import Unit, RectGrob
from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob
from gtable_r2py.modify import (
    gtable_trim, gtable_filter,
    gtable_add_padding, gtable_add_row_space, gtable_add_col_space,
)


class TestTrim:
    def test_trim_empty(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        result = gtable_trim(gt)
        assert result.nrow == 0
        assert result.ncol == 0

    def test_trim_center(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="r"), t=2, l=2)
        result = gtable_trim(gt)
        assert result.nrow == 1
        assert result.ncol == 1
        assert len(result) == 1
        assert result.layout.t == [1]
        assert result.layout.l == [1]

    def test_trim_spanning(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="r"), t=1, l=2, b=3, r=3)
        result = gtable_trim(gt)
        assert result.nrow == 3
        assert result.ncol == 2


class TestFilter:
    def test_filter_by_name(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="rect"), t=1, l=1, name="rect")
        gtable_add_grob(gt, RectGrob(name="circ"), t=1, l=3, name="circ")
        result = gtable_filter(gt, "rect")
        assert len(result) == 1
        assert result.layout.name == ["rect"]

    def test_filter_regex(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, name="panel-1")
        gtable_add_grob(gt, RectGrob(name="b"), t=1, l=2, name="panel-2")
        result = gtable_filter(gt, r"panel-\d+")
        assert len(result) == 2

    def test_filter_invert(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, name="keep")
        gtable_add_grob(gt, RectGrob(name="b"), t=1, l=2, name="remove")
        result = gtable_filter(gt, "remove", invert=True)
        assert len(result) == 1
        assert result.layout.name == ["keep"]

    def test_filter_fixed(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, name="a.b")
        result = gtable_filter(gt, "a.b", fixed=True)
        assert len(result) == 1

    def test_filter_no_trim(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=2, name="mid")
        result = gtable_filter(gt, "mid", trim=False)
        assert result.ncol == 3


class TestPadding:
    def test_padding(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gtable_add_padding(gt, Unit(0.5, "cm"))
        assert result.nrow == 3
        assert result.ncol == 3

    def test_padding_vector(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gtable_add_padding(gt, Unit([1, 2, 3, 4], "cm"))
        assert result.nrow == 3
        assert result.ncol == 3


class TestRowSpace:
    def test_row_space_single(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1, 1], "cm"))
        result = gtable_add_row_space(gt, Unit(0.5, "cm"))
        assert result.nrow == 5

    def test_row_space_no_rows(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gtable_add_row_space(gt, Unit(0.5, "cm"))
        assert result.nrow == 1


class TestColSpace:
    def test_col_space_single(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1], "cm"))
        result = gtable_add_col_space(gt, Unit(0.5, "cm"))
        assert result.ncol == 5

    def test_col_space_vector(self):
        gt = GTable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1], "cm"))
        result = gtable_add_col_space(gt, Unit([0.5, 1.0], "cm"))
        assert result.ncol == 5


class TestMethodChaining:
    def test_trim_returns_new(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="r"), t=1, l=1)
        result = gt.trim()
        assert result.nrow == 1

    def test_filter_returns_new(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, name="a")
        gtable_add_grob(gt, RectGrob(name="b"), t=1, l=2, name="b")
        result = gt.filter("a")
        assert len(result) == 1
