import pytest
from libxiangqi import Board, IllegalMove


def test_illegal_move_no_piece():
    """Test that moving from empty square raises IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(0, 1, 1, 1)


def test_illegal_move_wrong_turn():
    """Test that moving opponent's piece raises IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(4, 6, 4, 5)


def test_illegal_move_invalid_position():
    """Test that invalid positions raise IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(10, 10, 5, 5)


def test_illegal_move_capture_own():
    """Test that capturing own piece raises IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(0, 0, 1, 0)


def test_illegal_move_same_position():
    """Test that moving to same position raises IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(4, 3, 4, 3)


def test_illegal_move_blocked_path():
    """Test that moving through blocking pieces raises IllegalMove"""
    g = Board()
    with pytest.raises(IllegalMove):
        g.make_move(0, 0, 0, 5)


def test_illegal_move_piece_specific():
    """Test that invalid piece-specific moves raise IllegalMove"""
    g = Board()
    # General can't move diagonally
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)
    with pytest.raises(IllegalMove):
        g.make_move(4, 0, 5, 1)
