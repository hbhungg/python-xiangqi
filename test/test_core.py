import xiangqi


def test_board_print():
  starting_board = """
c h e a g a e h c
. . . . . . . . .
. c . . . . . c .
s . s . s . s . s
. . . . . . . . .
. . . . . . . . .
S . S . S . S . S
. C . . . . . C .
. . . . . . . . .
C H E A G A E H C
"""
  b = xiangqi.Board()
  assert str(b).strip() == starting_board.strip()


def test_idk():
  from xiangqi import PieceType

  assert xiangqi.piece_symbol(PieceType.SOLDIER) == "s"
  assert xiangqi.piece_name(PieceType.SOLDIER) == "soldier"
