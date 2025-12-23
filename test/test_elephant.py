import pytest
from libxiangqi import Game, IllegalMove


def test_red_elephant_move_diagonal():
    """Test red elephant can move two steps diagonally"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Move elephant diagonally
    g.make_move(2, 0, 4, 2)


def test_black_elephant_move_diagonal():
    """Test black elephant can move two steps diagonally"""
    g = Game()
    # Red move
    g.make_move(4, 3, 4, 4)

    # Black elephant moves diagonally
    g.make_move(2, 9, 4, 7)


def test_elephant_blocked_by_piece():
    """Test elephant cannot jump over pieces (elephant eye blocked)"""
    g = Game()
    # Soldier is at (4,3), blocking elephant at (2,0) from moving to (4,2)
    # because the midpoint (3,1) needs to be checked, but (4,3) blocks the path indirectly

    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Move elephant
    g.make_move(2, 0, 4, 2)
    g.make_move(0, 6, 0, 5)

    # Move soldier to block elephant
    g.make_move(4, 4, 4, 5)
    g.make_move(0, 5, 0, 4)

    # Move elephant back
    g.make_move(4, 2, 2, 0)
    g.make_move(0, 4, 0, 3)

    # Move soldier to elephant eye position
    g.make_move(2, 3, 3, 3)
    g.make_move(0, 3, 0, 2)
    g.make_move(3, 3, 3, 4)
    g.make_move(0, 2, 0, 1)
    g.make_move(3, 4, 3, 5)
    g.make_move(0, 1, 0, 0)
    g.make_move(3, 5, 3, 6)
    g.make_move(8, 6, 8, 5)
    g.make_move(3, 6, 3, 7)
    g.make_move(8, 5, 8, 4)
    g.make_move(3, 7, 4, 7)
    g.make_move(8, 4, 8, 3)
    g.make_move(4, 7, 5, 7)
    g.make_move(8, 3, 8, 2)
    g.make_move(5, 7, 6, 7)
    g.make_move(8, 2, 8, 1)
    g.make_move(6, 7, 7, 7)
    g.make_move(8, 1, 8, 0)
    g.make_move(7, 7, 8, 7)
    g.make_move(6, 9, 7, 7)
    g.make_move(8, 7, 8, 8)
    g.make_move(7, 7, 8, 5)
    g.make_move(8, 8, 7, 8)
    g.make_move(8, 5, 7, 3)
    g.make_move(7, 8, 6, 8)
    g.make_move(7, 3, 6, 1)
    g.make_move(6, 8, 5, 8)

    # Now put a piece at (3,1) to block the elephant eye
    g.make_move(4, 0, 3, 1)
    g.make_move(5, 8, 4, 8)

    # Try to move elephant - should be blocked
    with pytest.raises(IllegalMove):
        g.make_move(2, 0, 4, 2)


def test_red_elephant_cannot_cross_river():
    """Test red elephant cannot cross the river (rank > 4)"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Move elephant to edge of river
    g.make_move(2, 0, 4, 2)
    g.make_move(0, 6, 0, 5)
    g.make_move(4, 2, 2, 4)
    g.make_move(0, 5, 0, 4)

    # Try to cross river
    with pytest.raises(IllegalMove):
        g.make_move(2, 4, 4, 6)


def test_black_elephant_cannot_cross_river():
    """Test black elephant cannot cross the river (rank < 5)"""
    g = Game()
    # Red move
    g.make_move(4, 3, 4, 4)

    # Black elephant to edge of river
    g.make_move(2, 9, 4, 7)
    g.make_move(0, 3, 0, 4)
    g.make_move(4, 7, 2, 5)
    g.make_move(0, 4, 0, 5)

    # Try to cross river
    with pytest.raises(IllegalMove):
        g.make_move(2, 5, 4, 3)


def test_elephant_cannot_move_one_step():
    """Test elephant must move exactly 2 diagonal steps"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Try to move elephant one step
    with pytest.raises(IllegalMove):
        g.make_move(2, 0, 3, 1)


def test_elephant_cannot_move_orthogonally():
    """Test elephant cannot move in straight lines"""
    g = Game()
    # Move soldier
    g.make_move(4, 3, 4, 4)
    g.make_move(4, 6, 4, 5)

    # Try to move elephant orthogonally
    with pytest.raises(IllegalMove):
        g.make_move(2, 0, 2, 2)
