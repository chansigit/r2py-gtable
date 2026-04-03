import pytest
from grid_r2py import Unit, RectGrob
from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob
from gtable_r2py.combine import gtable_rbind, gtable_cbind


def _make_gt(nrow, ncol, name="test"):
    return GTable(
        widths=Unit([1] * ncol, "cm"),
        heights=Unit([1] * nrow, "cm"),
        name=name,
    )


class TestRbind:
    def test_basic(self):
        a = _make_gt(2, 3)
        b = _make_gt(1, 3)
        result = gtable_rbind(a, b)
        assert result.nrow == 3
        assert result.ncol == 3

    def test_grobs_preserved(self):
        a = _make_gt(1, 1)
        b = _make_gt(1, 1)
        gtable_add_grob(a, RectGrob(name="ra"), t=1, l=1)
        gtable_add_grob(b, RectGrob(name="rb"), t=1, l=1)
        result = gtable_rbind(a, b)
        assert len(result) == 2
        assert result.layout.t == [1, 2]

    def test_size_max(self):
        a = GTable(widths=Unit([1, 2], "cm"), heights=Unit([1], "cm"))
        b = GTable(widths=Unit([3, 1], "cm"), heights=Unit([1], "cm"))
        result = gtable_rbind(a, b, size="max")
        assert result.nrow == 2

    def test_size_first(self):
        a = GTable(widths=Unit([1, 2], "cm"), heights=Unit([1], "cm"))
        b = GTable(widths=Unit([3, 1], "cm"), heights=Unit([1], "cm"))
        result = gtable_rbind(a, b, size="first")
        assert result.nrow == 2

    def test_mismatched_cols_raises(self):
        a = _make_gt(1, 2)
        b = _make_gt(1, 3)
        with pytest.raises(ValueError):
            gtable_rbind(a, b)

    def test_three_tables(self):
        a = _make_gt(1, 2)
        b = _make_gt(1, 2)
        c = _make_gt(1, 2)
        result = gtable_rbind(a, b, c)
        assert result.nrow == 3


class TestCbind:
    def test_basic(self):
        a = _make_gt(3, 2)
        b = _make_gt(3, 1)
        result = gtable_cbind(a, b)
        assert result.nrow == 3
        assert result.ncol == 3

    def test_grobs_preserved(self):
        a = _make_gt(1, 1)
        b = _make_gt(1, 1)
        gtable_add_grob(a, RectGrob(name="ra"), t=1, l=1)
        gtable_add_grob(b, RectGrob(name="rb"), t=1, l=1)
        result = gtable_cbind(a, b)
        assert len(result) == 2
        assert result.layout.l == [1, 2]

    def test_mismatched_rows_raises(self):
        a = _make_gt(2, 1)
        b = _make_gt(3, 1)
        with pytest.raises(ValueError):
            gtable_cbind(a, b)

    def test_size_min(self):
        a = GTable(widths=Unit([1], "cm"), heights=Unit([1, 2], "cm"))
        b = GTable(widths=Unit([1], "cm"), heights=Unit([3, 1], "cm"))
        result = gtable_cbind(a, b, size="min")
        assert result.ncol == 2


class TestRbindWithZ:
    def test_z_ordering(self):
        a = _make_gt(1, 1)
        b = _make_gt(1, 1)
        gtable_add_grob(a, RectGrob(name="ra"), t=1, l=1, z=5)
        gtable_add_grob(b, RectGrob(name="rb"), t=1, l=1, z=3)
        result = gtable_rbind(a, b, z=[2, 1])
        assert result.layout.z[1] < result.layout.z[0]


class TestEmptyBinds:
    def test_rbind_empty_first(self):
        a = GTable(widths=Unit([1], "cm"), heights=Unit([], "cm"))
        b = _make_gt(2, 1)
        result = gtable_rbind(a, b)
        assert result.nrow == 2

    def test_cbind_empty_first(self):
        a = GTable(widths=Unit([], "cm"), heights=Unit([1], "cm"))
        b = _make_gt(1, 2)
        result = gtable_cbind(a, b)
        assert result.ncol == 2
