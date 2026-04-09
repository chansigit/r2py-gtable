import pytest
from grid_r2py import Unit, RectGrob, Viewport, Layout, GTree
from grid_r2py.vp_collections import VpStack
from gtable_r2py.gtable import GTable
from gtable_r2py.add import gtable_add_grob
from gtable_r2py.grid_integration import (
    gtable_make_context, gtable_make_content,
    gtable_width_details, gtable_height_details,
)


class TestMakeContext:
    def test_creates_layout_viewport(self):
        gt = GTable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([3], "cm"),
            name="test",
        )
        result = gtable_make_context(gt)
        assert result is gt
        assert gt.vp is not None
        assert gt.vp.layout is not None
        assert gt.vp.layout.nrow == 1
        assert gt.vp.layout.ncol == 2

    def test_stacks_existing_vp(self):
        outer_vp = Viewport(width=Unit(10, "cm"), height=Unit(10, "cm"), name="outer")
        gt = GTable(
            widths=Unit([1], "cm"),
            heights=Unit([1], "cm"),
            name="test",
            vp=outer_vp,
        )
        gtable_make_context(gt)
        # Should produce a VpStack with [outer_vp, layout_vp]
        assert isinstance(gt.vp, VpStack)
        assert len(gt.vp) == 2
        assert gt.vp[0] is outer_vp
        assert gt.vp[1].layout is not None
        assert gt.vp[1].layout.nrow == 1
        assert gt.vp[1].layout.ncol == 1

    def test_idempotent_no_vp(self):
        """Calling make_context twice without user vp should not nest."""
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"), name="test")
        gtable_make_context(gt)
        gtable_make_context(gt)
        # Should still be a plain Viewport, not nested
        assert not isinstance(gt.vp, VpStack)
        assert gt.vp.layout is not None

    def test_idempotent_with_vp(self):
        """Calling make_context twice with user vp should not double-nest."""
        outer_vp = Viewport(name="outer")
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"), name="test", vp=outer_vp)
        gtable_make_context(gt)
        gtable_make_context(gt)
        # Should still be a VpStack of exactly 2, not 3+
        assert isinstance(gt.vp, VpStack)
        assert len(gt.vp) == 2
        assert gt.vp[0] is outer_vp


class TestMakeContent:
    def test_sets_children(self):
        gt = GTable(
            widths=Unit([1, 1], "cm"),
            heights=Unit([1, 1], "cm"),
        )
        r1 = RectGrob(name="r1")
        r2 = RectGrob(name="r2")
        gtable_add_grob(gt, r1, t=1, l=1, name="r1")
        gtable_add_grob(gt, r2, t=2, l=2, name="r2", z=1)
        result = gtable_make_content(gt)
        assert result is gt
        assert len(gt.children) == 2

    def test_z_order(self):
        gt = GTable(
            widths=Unit([1], "cm"),
            heights=Unit([1, 1], "cm"),
        )
        r1 = RectGrob(name="r1")
        r2 = RectGrob(name="r2")
        gtable_add_grob(gt, r1, t=1, l=1, name="first", z=10)
        gtable_add_grob(gt, r2, t=2, l=1, name="second", z=1)
        gtable_make_content(gt)
        # Children should be ordered by z: r2 (z=1) before r1 (z=10)
        assert gt.children[0].name == "second.2-1-2-1"
        assert gt.children[1].name == "first.1-1-1-1"

    def test_empty_gtable(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        gtable_make_content(gt)
        assert len(gt.children) == 0


class TestDimensionDetails:
    def test_width(self):
        gt = GTable(widths=Unit([1, 2, 3], "cm"), heights=Unit([1], "cm"))
        w = gtable_width_details(gt)
        assert isinstance(w, Unit)

    def test_height(self):
        gt = GTable(widths=Unit([1], "cm"), heights=Unit([1, 2], "cm"))
        h = gtable_height_details(gt)
        assert isinstance(h, Unit)
