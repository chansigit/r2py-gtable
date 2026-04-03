import pytest
from gtable_r2py.layout_table import LayoutTable, LayoutRow


class TestLayoutRow:
    def test_fields(self):
        row = LayoutRow(t=1, l=2, b=3, r=4, z=1.0, clip="on", name="rect")
        assert row.t == 1
        assert row.l == 2
        assert row.b == 3
        assert row.r == 4
        assert row.z == 1.0
        assert row.clip == "on"
        assert row.name == "rect"


class TestLayoutTableCreation:
    def test_empty(self):
        lt = LayoutTable()
        assert len(lt) == 0
        assert lt.t == []
        assert lt.name == []

    def test_from_columns(self):
        lt = LayoutTable(
            t=[1, 2], l=[1, 1], b=[1, 2], r=[1, 1],
            z=[1.0, 2.0], clip=["on", "on"], name=["a", "b"]
        )
        assert len(lt) == 2
        assert lt.t == [1, 2]


class TestLayoutTableAppend:
    def test_append_one(self):
        lt = LayoutTable()
        lt.append(t=1, l=1, b=1, r=1, z=1.0, clip="on", name="a")
        assert len(lt) == 1
        assert lt.name == ["a"]

    def test_append_multiple(self):
        lt = LayoutTable()
        lt.append(t=1, l=1, b=1, r=1, z=1.0, clip="on", name="a")
        lt.append(t=2, l=2, b=2, r=2, z=2.0, clip="off", name="b")
        assert len(lt) == 2
        assert lt.z == [1.0, 2.0]


class TestLayoutTableExtend:
    def test_extend(self):
        lt1 = LayoutTable(t=[1], l=[1], b=[1], r=[1], z=[1.0], clip=["on"], name=["a"])
        lt2 = LayoutTable(t=[2], l=[2], b=[2], r=[2], z=[2.0], clip=["off"], name=["b"])
        lt1.extend(lt2)
        assert len(lt1) == 2
        assert lt1.name == ["a", "b"]


class TestLayoutTableIndexing:
    def test_int_index(self):
        lt = LayoutTable(
            t=[1, 2], l=[3, 4], b=[1, 2], r=[3, 4],
            z=[1.0, 2.0], clip=["on", "off"], name=["a", "b"]
        )
        row = lt[0]
        assert isinstance(row, LayoutRow)
        assert row.t == 1
        assert row.name == "a"

    def test_bool_mask(self):
        lt = LayoutTable(
            t=[1, 2, 3], l=[1, 1, 1], b=[1, 2, 3], r=[1, 1, 1],
            z=[1.0, 2.0, 3.0], clip=["on", "on", "on"], name=["a", "b", "c"]
        )
        filtered = lt[[True, False, True]]
        assert isinstance(filtered, LayoutTable)
        assert len(filtered) == 2
        assert filtered.name == ["a", "c"]

    def test_slice(self):
        lt = LayoutTable(
            t=[1, 2, 3], l=[1, 1, 1], b=[1, 2, 3], r=[1, 1, 1],
            z=[1.0, 2.0, 3.0], clip=["on", "on", "on"], name=["a", "b", "c"]
        )
        sliced = lt[1:3]
        assert isinstance(sliced, LayoutTable)
        assert len(sliced) == 2
        assert sliced.name == ["b", "c"]


class TestLayoutTableFilter:
    def test_filter(self):
        lt = LayoutTable(
            t=[1, 2, 3], l=[1, 1, 1], b=[1, 2, 3], r=[1, 1, 1],
            z=[1.0, 2.0, 3.0], clip=["on", "on", "on"], name=["a", "b", "c"]
        )
        filtered = lt.filter([True, False, True])
        assert len(filtered) == 2
        assert filtered.t == [1, 3]


class TestLayoutTableShift:
    def test_shift_rows(self):
        lt = LayoutTable(
            t=[1, 2, 3], l=[1, 1, 1], b=[1, 3, 3], r=[1, 1, 1],
            z=[1.0, 2.0, 3.0], clip=["on", "on", "on"], name=["a", "b", "c"]
        )
        lt.shift_rows(offset=2, after=1)
        assert lt.t == [1, 4, 5]
        assert lt.b == [1, 5, 5]

    def test_shift_cols(self):
        lt = LayoutTable(
            t=[1, 1, 1], l=[1, 2, 3], b=[1, 1, 1], r=[1, 2, 3],
            z=[1.0, 2.0, 3.0], clip=["on", "on", "on"], name=["a", "b", "c"]
        )
        lt.shift_cols(offset=1, after=1)
        assert lt.l == [1, 3, 4]
        assert lt.r == [1, 3, 4]


class TestLayoutTableCopy:
    def test_copy_independent(self):
        lt = LayoutTable(t=[1], l=[1], b=[1], r=[1], z=[1.0], clip=["on"], name=["a"])
        lt2 = lt.copy()
        lt2.append(t=2, l=2, b=2, r=2, z=2.0, clip="off", name="b")
        assert len(lt) == 1
        assert len(lt2) == 2
