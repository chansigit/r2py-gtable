"""End-to-end integration tests exercising full gtable workflows."""

import math
import pytest
from grid_r2py import Unit, RectGrob, CircleGrob, NullGrob

from gtable_r2py import (
    GTable, gtable, gtable_col, gtable_row, gtable_matrix,
    gtable_add_grob, gtable_add_rows, gtable_add_cols,
    gtable_rbind, gtable_cbind,
    gtable_trim, gtable_filter, gtable_add_padding,
    gtable_add_row_space, gtable_add_col_space,
    gtable_row_spacer, gtable_col_spacer,
    is_gtable, as_gtable,
    gtable_make_context, gtable_make_content,
    gtable_width_details, gtable_height_details,
)


class TestBuildAndManipulate:
    def test_ggplot_like_workflow(self):
        """Simulate a simplified ggplot2-style panel assembly."""
        # 1. Create panel area
        panel = gtable_matrix(
            "panel",
            grobs=[[RectGrob(name="plot_bg")]],
            widths=Unit([1], "null"),
            heights=Unit([1], "null"),
        )
        assert panel.dim() == (1, 1)

        # 2. Add axis grobs
        gtable_add_cols(panel, Unit([1], "cm"), pos=0)   # y-axis space left
        gtable_add_rows(panel, Unit([1], "cm"), pos=-1)  # x-axis space bottom
        gtable_add_grob(panel, RectGrob(name="yaxis"), t=1, l=1, name="yaxis")
        gtable_add_grob(panel, RectGrob(name="xaxis"), t=2, l=2, name="xaxis")
        assert panel.dim() == (2, 2)
        assert len(panel) == 3

        # 3. Add title row
        gtable_add_rows(panel, Unit([0.5], "cm"), pos=0)
        gtable_add_grob(panel, RectGrob(name="title"), t=1, l=1, b=1, r=2, name="title")
        assert panel.dim() == (3, 2)

        # 4. Add padding
        gtable_add_padding(panel, Unit(0.2, "cm"))
        assert panel.dim() == (5, 4)

        # 5. Prepare for rendering
        gtable_make_context(panel)
        gtable_make_content(panel)
        assert len(panel.children) == 4

    def test_chaining_workflow(self):
        """Test method chaining API."""
        gt = GTable(
            widths=Unit([1, 1], "cm"),
            heights=Unit([1, 1], "cm"),
        )
        gt.add_grob(RectGrob(name="r"), t=1, l=1) \
          .add_rows(Unit([0.5], "cm")) \
          .add_cols(Unit([0.5], "cm"))
        assert gt.nrow == 3
        assert gt.ncol == 3
        assert len(gt) == 1


class TestCombineWorkflow:
    def test_rbind_cbind(self):
        """Build a 2x2 grid of panels using rbind/cbind."""
        panels = []
        for i in range(4):
            p = gtable(
                widths=Unit([1], "null"),
                heights=Unit([1], "null"),
            )
            gtable_add_grob(p, RectGrob(name=f"p{i}"), t=1, l=1, name=f"panel-{i}")
            panels.append(p)

        top = gtable_cbind(panels[0], panels[1])
        bottom = gtable_cbind(panels[2], panels[3])
        grid = gtable_rbind(top, bottom)

        assert grid.dim() == (2, 2)
        assert len(grid) == 4


class TestFilterAndTrim:
    def test_extract_panels(self):
        """Filter to keep only panel grobs, then trim."""
        gt = gtable(widths=Unit([1, 1, 1], "cm"), heights=Unit([1, 1, 1], "cm"))
        gtable_add_grob(gt, RectGrob(name="bg"), t=1, l=1, b=3, r=3, name="background")
        gtable_add_grob(gt, RectGrob(name="p"), t=2, l=2, name="panel-1")
        gtable_add_grob(gt, RectGrob(name="a"), t=3, l=3, name="axis-x")

        panels = gtable_filter(gt, "panel")
        assert len(panels) == 1
        assert panels.layout.name == ["panel-1"]


class TestAsGtable:
    def test_roundtrip(self):
        gt = gtable(widths=Unit([1], "cm"), heights=Unit([1], "cm"))
        assert as_gtable(gt) is gt

    def test_grob_wrapping(self):
        grob = RectGrob(name="test")
        gt = as_gtable(grob)
        assert is_gtable(gt)
        assert len(gt) == 1


class TestSpacers:
    def test_spacer_in_rbind(self):
        """Use spacers to add gaps between panels.

        gtable_row_spacer creates a zero-column GTable with row heights,
        which is treated as a zero-height row spacer in rbind (skipped).
        To insert a visible gap row between panels, use a 1-row GTable with
        the desired height instead.
        """
        p1 = gtable(widths=Unit([1], "null"), heights=Unit([1], "null"))
        gtable_add_grob(p1, RectGrob(name="p1"), t=1, l=1)
        p2 = gtable(widths=Unit([1], "null"), heights=Unit([1], "null"))
        gtable_add_grob(p2, RectGrob(name="p2"), t=1, l=1)

        # Create a proper row-gap spacer: 1 row, 1 col, no grobs
        spacer = GTable(widths=Unit([1], "null"), heights=Unit([0.5], "cm"))
        result = gtable_rbind(p1, spacer, p2)
        assert result.nrow == 3
        assert len(result) == 2  # spacer has no grobs

    def test_col_spacer_structure(self):
        """gtable_col_spacer produces a zero-column table with row heights."""
        spacer = gtable_col_spacer(Unit(0.5, "cm"))
        assert spacer.nrow == 1
        assert spacer.ncol == 0

    def test_row_spacer_structure(self):
        """gtable_row_spacer produces a zero-row table with column widths."""
        spacer = gtable_row_spacer(Unit(0.5, "cm"))
        assert spacer.nrow == 0
        assert spacer.ncol == 1


class TestSubsetting:
    def test_matrix_subsetting(self):
        """Test [rows, cols] subsetting."""
        gt = gtable_matrix(
            "test",
            grobs=[
                [RectGrob(name="a"), RectGrob(name="b")],
                [RectGrob(name="c"), RectGrob(name="d")],
            ],
            widths=Unit([1, 1], "cm"),
            heights=Unit([1, 1], "cm"),
        )
        # Get top-left cell
        sub = gt[0:1, 0:1]
        assert sub.nrow == 1
        assert sub.ncol == 1
        assert len(sub) == 1

    def test_named_subsetting(self):
        """Test subsetting by names."""
        gt = GTable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([1, 2], "cm"),
            rownames=["top", "bottom"],
            colnames=["left", "right"],
        )
        gtable_add_grob(gt, RectGrob(name="r"), t=1, l=2, name="r")
        sub = gt["top", "right"]
        assert sub.nrow == 1
        assert sub.ncol == 1
        assert len(sub) == 1
