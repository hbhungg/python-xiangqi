import pytest
from libxiangqi import Game, IllegalMove


def test_red_chariot_move_vertical():
    """Test red chariot can move vertically when path is clear"""
    g = Game()
    # Move soldier out of the way first
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Now chariot can move to where soldier was
    g.make_move(0, 0, 0, 3)


def test_black_chariot_move_vertical():
    """Test black chariot can move vertically"""
    g = Game()
    # Red move
    g.make_move(0, 3, 0, 4)

    # Move black soldier, then chariot
    g.make_move(0, 6, 0, 5)
    g.make_move(0, 4, 0, 5)
    g.make_move(0, 9, 0, 6)


def test_chariot_move_horizontal():
    """Test chariot can move horizontally"""
    g = Game()
    # Move soldier out
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Move chariot up
    g.make_move(0, 0, 0, 2)
    g.make_move(0, 5, 0, 4)

    # Move chariot horizontally
    g.make_move(0, 2, 3, 2)


def test_chariot_blocked_by_own_piece():
    """Test chariot cannot move through own pieces"""
    g = Game()
    # Chariot at (0,0) blocked by soldier at (0,3)
    with pytest.raises(IllegalMove):
        g.make_move(0, 0, 0, 4)


def test_chariot_blocked_by_enemy_piece():
    """Test chariot cannot jump over enemy pieces"""
    g = Game()
    # Move pieces to set up blocking
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)
    g.make_move(0, 0, 0, 3)
    g.make_move(0, 9, 0, 6)

    # Chariot at (0,3) blocked by black soldier at (0,5)
    with pytest.raises(IllegalMove):
        g.make_move(0, 3, 0, 6)


def test_chariot_can_capture():
    """Test chariot can capture enemy pieces"""
    g = Game()
    # Set up capture
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)
    g.make_move(0, 0, 0, 3)
    g.make_move(8, 6, 8, 5)

    # Chariot captures black soldier
    g.make_move(0, 3, 0, 5)


def test_chariot_cannot_capture_own_piece():
    """Test chariot cannot capture its own pieces"""
    g = Game()
    # Try to move chariot onto own soldier
    with pytest.raises(IllegalMove):
        g.make_move(0, 0, 0, 3)


def test_chariot_cannot_move_diagonally():
    """Test chariot can only move in straight lines"""
    g = Game()
    # Move soldier
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Try diagonal move
    with pytest.raises(IllegalMove):
        g.make_move(0, 0, 1, 1)


def test_chariot_long_distance_move():
    """Test chariot can move multiple squares at once"""
    g = Game()
    # Clear path
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Move chariot multiple squares
    g.make_move(0, 0, 0, 2)
    g.make_move(0, 5, 0, 4)
    g.make_move(0, 2, 5, 2)


def test_chariot_horizontal_blocked():
    """Test chariot blocked when moving horizontally"""
    g = Game()
    # Move chariot up
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)
    g.make_move(0, 0, 0, 1)
    g.make_move(0, 5, 0, 4)

    # Try to move through horse
    with pytest.raises(IllegalMove):
        g.make_move(0, 1, 2, 1)


def test_chariot_can_move_full_board():
    """Test chariot can traverse the entire board if clear"""
    g = Game()
    # Move soldier
    g.make_move(0, 3, 0, 4)
    g.make_move(8, 6, 8, 5)

    # Move chariot far
    g.make_move(0, 0, 0, 2)
    g.make_move(8, 5, 8, 4)
    g.make_move(0, 2, 7, 2)


