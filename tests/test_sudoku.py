"""Test sudoku functions and class functions"""
import sudoku as s

def test_helper_functions():
    pass

def test_init_incomplete_board():
    """
    Tests the ListGrid class method that uses from_matrix() to build the board
    """
    l = s.ListGrid.init_incomplete()
    t = s.ListGrid(s.flatten(s.test_incomplete))
    assert l == t
    assert hash(l) == hash(t)

def test_incomplete_board():
    """
    Tests the ListGrid class method that uses from_matrix() to build the board
    """
    l = s.ListGrid.init_complete()
    t = s.ListGrid(s.flatten(s.test_complete))
    assert l == t
    assert hash(l) == hash(t)

def test_incorrect_board():
    """
    Tests the ListGrid class method that uses from_matrxi() to build the board
    Expecting an error to be raised of type ValueError
    """
    l = s.ListGrid.init_incorrect()

def test_manual_input_rows():
    pass

def test_manual_input_single_no_delim():
    pass

def test_manual_input_single_with_delim():
    pass