import pytest
from grid_r2py import Unit, RectGrob, CircleGrob, NullGrob
from gtable_r2py.layouts import (
    gtable_col, gtable_row, gtable_matrix,
    gtable_row_spacer, gtable_col_spacer,
)
from gtable_r2py.gtable import is_gtable


class TestGtableCol:
    def test_basic(self):
        grobs = [RectGrob(name="a"), CircleGrob(name="b")]
        gt = gtable_col("col", grobs)
        assert is_gtable(gt)
        assert gt.nrow == 2
        assert gt.ncol == 1
        assert len(gt) == 2
        assert gt.layout.t == [1, 2]
        assert gt.layout.l == [1, 1]

    def test_with_explicit_heights(self):
        grobs = [RectGrob(name="a"), RectGrob(name="b")]
        gt = gtable_col("col", grobs, heights=Unit([2, 3], "cm"))
        assert gt.nrow == 2

    def test_with_z(self):
        grobs = [RectGrob(name="a"), RectGrob(name="b")]
        gt = gtable_col("col", grobs, z=[10, 20])
        assert gt.layout.z == [10, 20]


class TestGtableRow:
    def test_basic(self):
        grobs = [RectGrob(name="a"), CircleGrob(name="b")]
        gt = gtable_row("row", grobs)
        assert gt.nrow == 1
        assert gt.ncol == 2
        assert len(gt) == 2
        assert gt.layout.l == [1, 2]
        assert gt.layout.t == [1, 1]


class TestGtableMatrix:
    def test_basic(self):
        grobs = [
            [RectGrob(name="a"), CircleGrob(name="b")],
            [NullGrob(name="c"), RectGrob(name="d")],
        ]
        gt = gtable_matrix(
            "mat", grobs,
            widths=Unit([1, 1], "null"),
            heights=Unit([1, 1], "null"),
        )
        assert gt.nrow == 2
        assert gt.ncol == 2
        assert len(gt) == 4
        assert gt.layout.t == [1, 1, 2, 2]
        assert gt.layout.l == [1, 2, 1, 2]

    def test_with_z(self):
        grobs = [
            [RectGrob(name="a"), RectGrob(name="b")],
            [RectGrob(name="c"), RectGrob(name="d")],
        ]
        z = [[3, 1], [2, 4]]
        gt = gtable_matrix(
            "mat", grobs,
            widths=Unit([1, 1], "null"),
            heights=Unit([1, 1], "null"),
            z=z,
        )
        assert gt.layout.z == [3, 1, 2, 4]


class TestSpacers:
    def test_row_spacer(self):
        gt = gtable_row_spacer(Unit([1, 2, 3], "cm"))
        assert gt.ncol == 3
        assert gt.nrow == 0
        assert len(gt) == 0

    def test_col_spacer(self):
        gt = gtable_col_spacer(Unit([1, 2], "cm"))
        assert gt.nrow == 2
        assert gt.ncol == 0
        assert len(gt) == 0


class TestLayoutErrors:
    def test_gtable_col_z_length_mismatch(self):
        grobs = [RectGrob(name="a"), RectGrob(name="b")]
        with pytest.raises(ValueError, match="same length"):
            gtable_col("test", grobs, z=[1.0])

    def test_gtable_row_z_length_mismatch(self):
        grobs = [RectGrob(name="a"), RectGrob(name="b")]
        with pytest.raises(ValueError, match="same length"):
            gtable_row("test", grobs, z=[1.0, 2.0, 3.0])

    def test_gtable_matrix_width_mismatch(self):
        grobs = [[RectGrob(name="a"), RectGrob(name="b")]]
        with pytest.raises(ValueError, match="widths"):
            gtable_matrix("test", grobs, widths=Unit([1], "cm"), heights=Unit([1], "cm"))

    def test_gtable_matrix_height_mismatch(self):
        grobs = [[RectGrob(name="a")]]
        with pytest.raises(ValueError, match="heights"):
            gtable_matrix("test", grobs, widths=Unit([1], "cm"), heights=Unit([1, 2], "cm"))
