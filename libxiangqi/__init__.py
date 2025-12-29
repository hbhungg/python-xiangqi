from ._libxiangqi import Board as _Board
from ._libxiangqi import IllegalMove as IllegalMove

class Board:
  def __init__(self):
    self._b = _Board()
  
  def make_move(self, *x):
    self._b.make_move(*x)
  
  @property
  def turn(self):
    return self._b.turn()