import pytest
from libxiangqi import Game, IllegalMove

def test_red_soldier_move():
  g = Game()
  g.make_move(4, 3, 4, 4)

def test_black_soldier_move():
  g = Game()
  g.make_move(4, 3, 4, 4)
  g.make_move(4, 6, 4, 5)

def test_red_soldier_no_move_sideway_before_river():
  g = Game()
  g.make_move(4, 3, 4, 4)
  g.make_move(4, 6, 4, 5)
  with pytest.raises(IllegalMove):
    g.make_move(2, 3, 3, 3)
