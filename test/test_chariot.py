import pytest
from libxiangqi import Game, IllegalMove

def test_red_chariot_move():
  g = Game()
  g.make_move(0, 0, 0, 3)


