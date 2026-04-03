import math
import pytest
from grid_r2py import Unit, RectGrob, NullGrob
from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob, gtable_add_rows, gtable_add_cols


class TestAddGrob:
    def test_single_grob(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=1)
        assert len(gt) == 1
        assert gt.layout.t == [1]
        assert gt.layout.l == [1]
        assert gt.layout.b == [1]
        assert gt.layout.r == [1]

    def test_spanning_grob(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=1, b=3, r=2)
        assert gt.layout.t == [1]
        assert gt.layout.b == [3]
        assert gt.layout.r == [2]

    def test_multiple_grobs(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1], "cm"))
        r1 = RectGrob(name="r1")
        r2 = RectGrob(name="r2")
        gtable_add_grob(gt, [r1, r2], t=[1, 2], l=[1, 2])
        assert len(gt) == 2

    def test_z_inf_increments(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1], "cm"))
        r1 = RectGrob(name="r1")
        r2 = RectGrob(name="r2")
        gtable_add_grob(gt, r1, t=1, l=1, z=math.inf)
        gtable_add_grob(gt, r2, t=2, l=1, z=math.inf)
        assert gt.layout.z[1] > gt.layout.z[0]

    def test_z_neg_inf(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1], "cm"))
        r1 = RectGrob(name="r1")
        r2 = RectGrob(name="r2")
        gtable_add_grob(gt, r1, t=1, l=1, z=5)
        gtable_add_grob(gt, r2, t=2, l=1, z=-math.inf)
        assert gt.layout.z[1] < gt.layout.z[0]

    def test_negative_index(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=-1, l=-1)
        assert gt.layout.t == [3]
        assert gt.layout.l == [2]

    def test_default_b_r(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=2)
        assert gt.layout.b == [1]
        assert gt.layout.r == [2]

    def test_chaining(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gt.add_grob(RectGrob(name="r"), t=1, l=1)
        assert result is gt


class TestAddRows:
    def test_add_at_bottom(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1], "cm"))
        gtable_add_rows(gt, Unit([2], "cm"))
        assert gt.nrow == 3

    def test_add_at_top(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=1)
        gtable_add_rows(gt, Unit([2], "cm"), pos=0)
        assert gt.nrow == 3
        # Existing grob should shift down
        assert gt.layout.t == [2]
        assert gt.layout.b == [2]

    def test_add_in_middle_spans(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1, 1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=1, b=3)
        gtable_add_rows(gt, Unit([1], "cm"), pos=1)
        # Grob spans 1-3, new row at pos 1 means grob now spans 1-4
        assert gt.layout.t == [1]
        assert gt.layout.b == [4]

    def test_chaining(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gt.add_rows(Unit([1], "cm"))
        assert result is gt


class TestAddCols:
    def test_add_at_right(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1], "cm"))
        gtable_add_cols(gt, Unit([2], "cm"))
        assert gt.ncol == 3

    def test_add_at_left(self):
        gt = GTable(widths=Unit([1, 1], "cm"), heights=Unit([1], "cm"))
        rect = RectGrob(name="r")
        gtable_add_grob(gt, rect, t=1, l=1)
        gtable_add_cols(gt, Unit([2], "cm"), pos=0)
        assert gt.ncol == 3
        assert gt.layout.l == [2]
        assert gt.layout.r == [2]

    def test_chaining(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = gt.add_cols(Unit([1], "cm"))
        assert result is gt
