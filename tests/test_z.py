import pytest
from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob
from gtable_r2py.z import z_normalise, z_arrange_gtables
from grid_r2py import Unit, RectGrob


class TestZNormalise:
    def test_empty_layout(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        result = z_normalise(gt)
        assert result is gt

    def test_normalise(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, z=10)
        gtable_add_grob(gt, RectGrob(name="b"), t=2, l=1, z=5)
        gtable_add_grob(gt, RectGrob(name="c"), t=3, l=1, z=20)
        z_normalise(gt)
        assert gt.layout.z == [2, 1, 3]

    def test_ties(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="a"), t=1, l=1, z=5)
        gtable_add_grob(gt, RectGrob(name="b"), t=2, l=1, z=5)
        z_normalise(gt)
        # First occurrence wins
        assert gt.layout.z[0] < gt.layout.z[1]


class TestZArrangeGtables:
    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            z_arrange_gtables([GTable()], [1, 2])

    def test_arrange(self):
        a = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        b = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        gtable_add_grob(a, RectGrob(name="a"), t=1, l=1, z=5)
        gtable_add_grob(b, RectGrob(name="b"), t=1, l=1, z=3)
        result = z_arrange_gtables([a, b], [2, 1])
        # b should be normalised first (lower z priority), a after
        assert max(b.layout.z) < min(a.layout.z)

    def test_with_empty_gtable(self):
        a = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        b = GTable()  # empty
        gtable_add_grob(a, RectGrob(name="a"), t=1, l=1)
        result = z_arrange_gtables([a, b], [1, 2])
        assert len(result) == 2
