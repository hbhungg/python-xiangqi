import pytest
from libxiangqi import Game, IllegalMove


def test_red_cannon_move_without_jump():
    """Test cannon can move without jumping when not capturing"""
    g = Game()
    # Cannon at (1,2) can move to (1,4) if path is clear
    # First move soldier out of way
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Now move cannon
    g.make_move(1, 2, 1, 4)


def test_black_cannon_move_without_jump():
    """Test black cannon can move without jumping"""
    g = Game()
    # Red move
    g.make_move(0, 3, 0, 4)

    # Black cannon moves
    g.make_move(1, 7, 1, 5)


def test_cannon_move_horizontally():
    """Test cannon can move horizontally"""
    g = Game()
    # Move soldier
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Move cannon horizontally
    g.make_move(1, 2, 0, 2)


def test_cannon_capture_with_screen():
    """Test cannon must jump over exactly one piece to capture"""
    g = Game()
    # Move pieces to set up a capture
    # Cannon at (1,2), soldier at (4,3), want to capture black soldier at (4,6)
    g.make_move(1, 2, 4, 2)
    g.make_move(0, 6, 0, 5)

    # Now cannon at (4,2), there's a red soldier at (4,3), and black soldier at (4,6)
    # Cannon should be able to capture the black soldier
    g.make_move(4, 2, 4, 6)


def test_cannon_cannot_capture_without_screen():
    """Test cannon cannot capture without a screen piece"""
    g = Game()
    # Move cannon
    g.make_move(1, 2, 1, 4)
    g.make_move(1, 7, 1, 5)

    # Try to capture without screen
    with pytest.raises(IllegalMove):
        g.make_move(1, 4, 1, 5)


def test_cannon_cannot_move_with_blocking_piece():
    """Test cannon cannot move through pieces when not capturing"""
    g = Game()
    # Cannon at (1,2) cannot move to (1,4) because soldier at (0,3) or (2,3)... wait
    # Actually, let me check the board layout. Cannon is at (1,2), soldiers are at ranks 3 and 6

    # Try to move cannon through soldier - should fail
    with pytest.raises(IllegalMove):
        g.make_move(1, 2, 1, 4)


def test_cannon_cannot_capture_with_two_screens():
    """Test cannon cannot capture if there are 2+ pieces in between"""
    g = Game()
    # Set up: cannon, soldier1, soldier2, enemy
    g.make_move(1, 2, 4, 2)
    g.make_move(4, 6, 4, 5)

    # Now: cannon at (4,2), red soldier at (4,3), black soldier at (4,5)
    # Try to capture - should fail because only 1 screen is allowed
    with pytest.raises(IllegalMove):
        g.make_move(4, 2, 4, 5)


def test_cannon_cannot_move_diagonally():
    """Test cannon can only move in straight lines"""
    g = Game()
    # Try to move cannon diagonally
    with pytest.raises(IllegalMove):
        g.make_move(1, 2, 2, 3)


def test_cannon_horizontal_capture():
    """Test cannon can capture horizontally with a screen"""
    g = Game()
    # Move cannon to position for horizontal capture
    g.make_move(1, 2, 1, 4)
    g.make_move(1, 7, 1, 5)

    # Move cannon horizontally
    g.make_move(1, 4, 3, 4)
    g.make_move(1, 5, 3, 5)

    # Now red cannon at (3,4), red soldier at (4,3)... need to position for horizontal capture
    # Move soldier to be screen
    g.make_move(4, 3, 4, 4)
    g.make_move(3, 5, 4, 5)

    # Now capture
    g.make_move(3, 4, 6, 4)


def test_cannon_cannot_jump_to_empty():
    """Test cannon cannot jump over piece to move to empty square"""
    g = Game()
    # Move soldier
    g.make_move(0, 3, 0, 4)
    g.make_move(0, 6, 0, 5)

    # Move cannon next to soldier
    g.make_move(1, 2, 1, 3)
    g.make_move(1, 7, 1, 6)

    # Try to jump over soldier to empty square
    with pytest.raises(IllegalMove):
        g.make_move(1, 3, 1, 5)
