import pytest
from libxiangqi import Game, IllegalMove


def test_red_horse_move_l_shape():
    """Test red horse can move in L-shape (2 forward, 1 sideways)"""
    g = Game()
    # Horse at (1,0) can move to (2,2)
    g.make_move(1, 0, 2, 2)


def test_black_horse_move_l_shape():
    """Test black horse can move in L-shape"""
    g = Game()
    # Red move
    g.make_move(1, 0, 2, 2)

    # Black horse moves
    g.make_move(1, 9, 2, 7)


def test_horse_all_l_directions():
    """Test horse can move in all 8 L-shape directions"""
    g = Game()
    # Move horse to open area
    g.make_move(1, 0, 2, 2)
    g.make_move(1, 9, 2, 7)

    # Test various L-moves
    g.make_move(2, 2, 3, 4)
    g.make_move(2, 7, 3, 5)
    g.make_move(3, 4, 2, 2)
    g.make_move(3, 5, 2, 7)
    g.make_move(2, 2, 1, 4)


def test_horse_blocked_by_piece():
    """Test horse cannot jump when leg is blocked"""
    g = Game()
    # Horse at (1,0) is blocked by elephant at (2,0) from moving to (3,1)
    # The blocking piece is in the direction of the longer movement

    # Try to move horse but it's blocked by elephant
    with pytest.raises(IllegalMove):
        g.make_move(1, 0, 3, 1)


def test_horse_not_blocked_diagonal():
    """Test horse is not blocked by diagonal pieces"""
    g = Game()
    # Horse at (1,0), cannon at (1,2), horse should be able to move to (2,2)
    g.make_move(1, 0, 2, 2)


def test_horse_blocked_horizontally():
    """Test horse blocked when moving horizontally more"""
    g = Game()
    # Move soldier out
    g.make_move(2, 3, 2, 4)
    g.make_move(2, 6, 2, 5)

    # Move horse to open area
    g.make_move(1, 0, 2, 2)
    g.make_move(1, 9, 2, 7)
    g.make_move(2, 2, 2, 3)
    g.make_move(2, 7, 2, 6)

    # Move piece to blocking position
    g.make_move(0, 0, 0, 2)
    g.make_move(0, 9, 0, 7)
    g.make_move(0, 2, 1, 2)
    g.make_move(0, 7, 1, 7)

    # Try to move horse - should be blocked at (1,3)
    with pytest.raises(IllegalMove):
        g.make_move(2, 3, 0, 2)


def test_horse_blocked_vertically():
    """Test horse blocked when moving vertically more"""
    g = Game()
    # Move soldier out
    g.make_move(2, 3, 2, 4)
    g.make_move(1, 6, 1, 5)

    # Move horse
    g.make_move(1, 0, 2, 2)
    g.make_move(1, 9, 2, 7)
    g.make_move(2, 2, 1, 4)
    g.make_move(2, 7, 1, 5)

    # Horse at (1,4) trying to move to (2,6) would be blocked at (1,5) where black soldier is
    with pytest.raises(IllegalMove):
        g.make_move(1, 4, 2, 6)


def test_horse_cannot_move_straight():
    """Test horse cannot move in straight lines"""
    g = Game()
    # Move soldier
    g.make_move(1, 3, 1, 4)
    g.make_move(1, 6, 1, 5)

    # Try to move horse straight
    with pytest.raises(IllegalMove):
        g.make_move(1, 0, 1, 2)


def test_horse_cannot_move_diagonally():
    """Test horse cannot move diagonally"""
    g = Game()
    # Try to move horse diagonally
    with pytest.raises(IllegalMove):
        g.make_move(1, 0, 2, 1)


def test_horse_cannot_move_one_square():
    """Test horse cannot move just one square"""
    g = Game()
    # Try to move horse one square
    with pytest.raises(IllegalMove):
        g.make_move(1, 0, 1, 1)
