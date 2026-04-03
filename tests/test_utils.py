import pytest
from grid_r2py import Unit, unit_c


class TestNegToPos:
    def test_positive_unchanged(self):
        from gtable_r2py.utils import neg_to_pos
        assert neg_to_pos(3, 5) == 3

    def test_zero_unchanged(self):
        from gtable_r2py.utils import neg_to_pos
        assert neg_to_pos(0, 5) == 0

    def test_minus_one_is_max(self):
        from gtable_r2py.utils import neg_to_pos
        assert neg_to_pos(-1, 5) == 5

    def test_minus_max_is_one(self):
        from gtable_r2py.utils import neg_to_pos
        assert neg_to_pos(-5, 5) == 1


class TestInsertUnit:
    def test_insert_at_beginning(self):
        from gtable_r2py.utils import insert_unit
        x = Unit([1, 2, 3], "cm")
        v = Unit([10], "cm")
        result = insert_unit(x, v, after=0)
        assert len(result) == 4
        assert result[0] == Unit(10, "cm")
        assert result[1] == Unit(1, "cm")

    def test_insert_at_end(self):
        from gtable_r2py.utils import insert_unit
        x = Unit([1, 2], "cm")
        v = Unit([10], "cm")
        result = insert_unit(x, v, after=2)
        assert len(result) == 3
        assert result[2] == Unit(10, "cm")

    def test_insert_in_middle(self):
        from gtable_r2py.utils import insert_unit
        x = Unit([1, 2, 3], "cm")
        v = Unit([10, 20], "cm")
        result = insert_unit(x, v, after=1)
        assert len(result) == 5
        assert result[0] == Unit(1, "cm")
        assert result[1] == Unit(10, "cm")
        assert result[2] == Unit(20, "cm")
        assert result[3] == Unit(2, "cm")

    def test_insert_into_empty(self):
        from gtable_r2py.utils import insert_unit
        x = Unit([], "cm")
        v = Unit([10], "cm")
        result = insert_unit(x, v, after=0)
        assert len(result) == 1

    def test_insert_empty_values(self):
        from gtable_r2py.utils import insert_unit
        x = Unit([1, 2], "cm")
        v = Unit([], "cm")
        result = insert_unit(x, v, after=1)
        assert len(result) == 2


class TestCompareUnit:
    def test_pmax(self):
        from gtable_r2py.utils import compare_unit
        from grid_r2py import unit_pmax
        x = Unit([1, 2, 3], "cm")
        y = Unit([3, 1, 2], "cm")
        result = compare_unit(x, y, unit_pmax)
        assert len(result) == 3

    def test_empty_x_returns_y(self):
        from gtable_r2py.utils import compare_unit
        from grid_r2py import unit_pmax
        x = Unit([], "cm")
        y = Unit([1, 2], "cm")
        result = compare_unit(x, y, unit_pmax)
        assert len(result) == 2

    def test_empty_y_returns_x(self):
        from gtable_r2py.utils import compare_unit
        from grid_r2py import unit_pmax
        x = Unit([1, 2], "cm")
        y = Unit([], "cm")
        result = compare_unit(x, y, unit_pmax)
        assert len(result) == 2


class TestLenSameOr1:
    def test_length_1(self):
        from gtable_r2py.utils import len_same_or_1
        assert len_same_or_1([42], 5) is True

    def test_same_length(self):
        from gtable_r2py.utils import len_same_or_1
        assert len_same_or_1([1, 2, 3], 3) is True

    def test_different_length(self):
        from gtable_r2py.utils import len_same_or_1
        assert len_same_or_1([1, 2], 3) is False
