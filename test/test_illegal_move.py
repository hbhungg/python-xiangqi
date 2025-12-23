import pytest

from libxiangqi import Game, IllegalMove

def test_illegal_move_raise():
  g = Game()
  with pytest.raises(IllegalMove):
    g.make_move(0, 1, 1, 1)
