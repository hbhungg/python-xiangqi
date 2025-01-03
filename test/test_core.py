import pytest
from xiangqi import Color, IllegalMoveError, Move, Piece, PieceType, Square, Board


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


def test_illegal_move():
  b = Board()
  with pytest.raises(IllegalMoveError):
    b.push(Move(Square.A2, Square.A3))
  with pytest.raises(IllegalMoveError):
    b.push(Move(Square.A1, Square.A4))


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


def test_chariot_legal_moves():
  from pprint import pprint

  b = Board()
  print(b)
  m = list(b._generate_legal_moves(Square.A1))
  pprint(m)
  assert Move(Square.A1, Square.A1) not in m
  assert Move(Square.A1, Square.A4) not in m
  assert Move(Square.A1, Square.A2) in m
  assert Move(Square.A1, Square.A5) not in m


def test_cannon_legal_moves():
  from pprint import pprint

  b = Board()
  print(b)
  m = list(b._generate_legal_moves(Square.B3))
  pprint(m)
  assert Move(Square.B3, Square.C4) in m
  # assert Move(Square.A1, Square.A4) not in m
  # assert Move(Square.A1, Square.A2) in m


def test_soldier_legal_moves():
  from pprint import pprint

  b = Board()
  print(b)
  m = list(b._generate_legal_moves(Square.A4))
  pprint(m)
  # assert Move(Square.A1, Square.A4) not in m
  # assert Move(Square.A1, Square.A2) in m
