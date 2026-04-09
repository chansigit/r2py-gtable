import pytest
from grid_r2py import Unit, Gpar, Viewport, NullGrob, RectGrob
from gtable_r2py.gtable import GTable, is_gtable, as_gtable
from gtable_r2py.layout_table import LayoutTable


class TestGTableConstruction:
    def test_empty(self):
        gt = GTable()
        assert gt.nrow == 0
        assert gt.ncol == 0
        assert len(gt) == 0
        assert gt.name == "layout"
        assert gt.respect is False

    def test_with_dimensions(self):
        gt = GTable(
            widths=Unit([1, 2, 3], "cm"),
            heights=Unit([5], "cm"),
        )
        assert gt.nrow == 1
        assert gt.ncol == 3
        assert len(gt) == 0

    def test_with_name(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"), name="panel")
        assert gt.name == "panel"

    def test_with_rownames_colnames(self):
        gt = GTable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([1, 2], "cm"),
            rownames=["r1", "r2"],
            colnames=["c1", "c2"],
        )
        assert gt.rownames == ["r1", "r2"]
        assert gt.colnames == ["c1", "c2"]

    def test_with_vp(self):
        vp = Viewport(width=Unit(10, "cm"), height=Unit(5, "cm"))
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"), vp=vp)
        assert gt.vp is not None


class TestGTableProperties:
    def test_dim(self):
        gt = GTable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2, 3], "cm"))
        assert gt.dim() == (3, 2)

    def test_total_width(self):
        gt = GTable(widths=Unit([1, 2, 3], "cm"), heights=Unit([1], "cm"))
        w = gt.total_width()
        assert isinstance(w, Unit)

    def test_total_height(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 2], "cm"))
        h = gt.total_height()
        assert isinstance(h, Unit)


class TestGTableRepr:
    def test_repr_empty(self):
        gt = GTable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2, 3], "cm"))
        s = repr(gt)
        assert "3" in s and "2" in s
        assert "layout" in s
        assert "0 grobs" in s


class TestGTableTranspose:
    def test_transpose_swaps(self):
        gt = GTable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([3, 4, 5], "cm"),
        )
        gt.transpose()
        assert gt.nrow == 2
        assert gt.ncol == 3


class TestIsGtable:
    def test_true(self):
        gt = GTable()
        assert is_gtable(gt) is True

    def test_false(self):
        assert is_gtable("hello") is False
        assert is_gtable(None) is False


class TestAsGtable:
    def test_from_gtable(self):
        gt = GTable()
        assert as_gtable(gt) is gt

    def test_from_grob(self):
        grob = RectGrob(name="r")
        result = as_gtable(grob)
        assert is_gtable(result)
        assert result.nrow == 1
        assert result.ncol == 1
        assert len(result) == 1

    def test_invalid(self):
        with pytest.raises(TypeError):
            as_gtable("not a grob")


class TestPublicAPI:
    def test_all_exports_importable(self):
        import gtable_r2py
        for name in gtable_r2py.__all__:
            assert hasattr(gtable_r2py, name), f"missing export: {name}"

    def test_gtable_function(self):
        from gtable_r2py import gtable, is_gtable
        from grid_r2py import Unit
        gt = gtable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        assert is_gtable(gt)


class TestGTableErrors:
    def test_getitem_requires_tuple(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        with pytest.raises(TypeError, match="requires \\[rows, cols\\]"):
            gt[0]

    def test_getitem_requires_two_elements(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        with pytest.raises(TypeError, match="requires \\[rows, cols\\]"):
            gt[0, 0, 0]

    def test_resolve_index_invalid_type(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        with pytest.raises(TypeError, match="invalid index type"):
            gt[{1}, 0]

    def test_resolve_index_name_without_names(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        with pytest.raises(KeyError, match="no names"):
            gt["missing", 0]
