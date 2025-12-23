import pytest
from libxiangqi import Game, IllegalMove


def test_red_advisor_move_diagonal():
    """Test red advisor can move diagonally within palace"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Move advisor diagonally
    g.make_move(3, 0, 4, 1)


def test_black_advisor_move_diagonal():
    """Test black advisor can move diagonally within palace"""
    g = Game()
    # Red move
    g.make_move(4, 3, 4, 4)

    # Black advisor moves diagonally
    g.make_move(3, 9, 4, 8)


def test_advisor_cannot_move_orthogonally():
    """Test advisor cannot move in straight lines (only diagonal)"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Try to move advisor orthogonally
    with pytest.raises(IllegalMove):
        g.make_move(3, 0, 3, 1)


def test_advisor_cannot_leave_palace():
    """Test advisor must stay within palace"""
    g = Game()
    # Move pieces to set up
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Move advisor to corner of palace
    g.make_move(3, 0, 4, 1)
    g.make_move(0, 6, 0, 5)
    g.make_move(4, 1, 5, 2)
    g.make_move(0, 5, 0, 4)

    # Try to move advisor outside palace
    with pytest.raises(IllegalMove):
        g.make_move(5, 2, 6, 3)


def test_advisor_cannot_move_two_steps():
    """Test advisor can only move one diagonal step"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Try to move advisor two diagonal steps
    with pytest.raises(IllegalMove):
        g.make_move(3, 0, 5, 2)


def test_advisor_all_positions():
    """Test advisor can reach all valid palace positions"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Advisor from (3,0) to (4,1)
    g.make_move(3, 0, 4, 1)
    g.make_move(0, 6, 0, 5)

    # Advisor from (4,1) to (3,2)
    g.make_move(4, 1, 3, 2)
    g.make_move(0, 5, 0, 4)

    # Advisor from (3,2) to (4,1)
    g.make_move(3, 2, 4, 1)
