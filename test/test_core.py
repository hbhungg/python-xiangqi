from xiangqi import Board

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
  b = Board()
  assert str(b).strip() == starting_board.strip()