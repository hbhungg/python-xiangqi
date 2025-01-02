from xiangqi import Color, Move, Piece, PieceType, Square, Board


def test_board_print():
  starting_board = """
r h e a g a e h r
. . . . . . . . .
. c . . . . . c .
s . s . s . s . s
. . . . . . . . .
. . . . . . . . .
S . S . S . S . S
. C . . . . . C .
. . . . . . . . .
R H E A G A E H R
"""
  b = Board()
  assert str(b).strip() == starting_board.strip()


def test_move():
  board_state = """
r h e a g a e h r
. . . . . . . . .
. c . . . . . c .
s . s . s . s . s
. . . . . . . . .
. . . . . . . . .
S . S . S . S . S
. C . . . . . C .
R . . . . . . . .
. H E A G A E H R
"""
  b = Board()
  b.push(Move(Square.A1, Square.A2))
  assert b.piece_at(Square.A2) == Piece(PieceType.CHARIOT, Color.RED)
  assert str(b).strip() == board_state.strip()


def test_color_at():
  b = Board()
  assert b.color_at(Square.A1) == Color.RED
  assert b.color_at(Square.A10) == Color.BLACK
  assert b.color_at(Square.A5) is None


def test_piece_at():
  b = Board()
  assert b.piece_at(Square.A1) == Piece(PieceType.CHARIOT, Color.RED)
  assert b.piece_at(Square.B1) == Piece(PieceType.HORSE, Color.RED)
  assert b.piece_at(Square.A10) == Piece(PieceType.CHARIOT, Color.BLACK)
  assert b.piece_at(Square.A5) is None
