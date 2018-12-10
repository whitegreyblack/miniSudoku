"""Test sudoku functions and class functions"""
from sudoku import string_2_list

def test_string_2_list():
    assert string_2_list("a b c") == ['a', 'b', 'c']

