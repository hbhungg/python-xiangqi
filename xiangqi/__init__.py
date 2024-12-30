from enum import Enum, auto
from typing import Optional


RANKS = 10
FILES = 9
RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]


class PieceType(Enum):
  SOLDIER = auto()
  CANNON = auto()
  GENERAL = auto()
  ADVISOR = auto()
  ELEPHANT = auto()
  HORSE = auto()
  CHARIOT = auto()


def piece_symbol(piece_type: PieceType) -> str:
  return piece_type.name[0].lower()


def piece_name(piece_type: PieceType) -> str:
  return piece_type.name.lower()


class Color(Enum):
  RED = True
  BLACK = False


class Square(Enum):
  A0 = 0
  A1 = 1
  A2 = 2
  A3 = 3
  A4 = 4
  A5 = 5
  A6 = 6
  A7 = 7
  A8 = 8
  A9 = 9
  B0 = 10
  B1 = 11
  B2 = 12
  B3 = 13
  B4 = 14
  B5 = 15
  B6 = 16
  B7 = 17
  B8 = 18
  B9 = 19
  C0 = 20
  C1 = 21
  C2 = 22
  C3 = 23
  C4 = 24
  C5 = 25
  C6 = 26
  C7 = 27
  C8 = 28
  C9 = 29
  D0 = 30
  D1 = 31
  D2 = 32
  D3 = 33
  D4 = 34
  D5 = 35
  D6 = 36
  D7 = 37
  D8 = 38
  D9 = 39
  E0 = 40
  E1 = 41
  E2 = 42
  E3 = 43
  E4 = 44
  E5 = 45
  E6 = 46
  E7 = 47
  E8 = 48
  E9 = 49
  F0 = 50
  F1 = 51
  F2 = 52
  F3 = 53
  F4 = 54
  F5 = 55
  F6 = 56
  F7 = 57
  F8 = 58
  F9 = 59
  G0 = 60
  G1 = 61
  G2 = 62
  G3 = 63
  G4 = 64
  G5 = 65
  G6 = 66
  G7 = 67
  G8 = 68
  G9 = 69
  H0 = 70
  H1 = 71
  H2 = 72
  H3 = 73
  H4 = 74
  H5 = 75
  H6 = 76
  H7 = 77
  H8 = 78
  H9 = 79
  I0 = 80
  I1 = 81
  I2 = 82
  I3 = 83
  I4 = 84
  I5 = 85
  I6 = 86
  I7 = 87
  I8 = 88
  I9 = 89


# TODO: This need refractor
STARTING_POSITION = {
  "RED_SOLDIER": 0b000000000_000000000_000000000_000000000_000000000_000000000_101010101_000000000_000000000_000000000,
  "RED_CANNON": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010_000000000_000000000,
  "RED_GENERAL": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000010000,
  "RED_ADVISOR": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000101000,
  "RED_ELEPHANT": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_001000100,
  "RED_HORSE": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010,
  "RED_CHARIOT": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_100000001,
  "BLACK_SOLDIER": 0b000000000_000000000_000000000_101010101_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_CANNON": 0b000000000_000000000_010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_GENERAL": 0b000010000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_ADVISOR": 0b000101000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_ELEPHANT": 0b001000100_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_HORSE": 0b010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_CHARIOT": 0b100000001_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
}


class Piece:
  VERTICAL = 0b100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000
  HORIZONTAL = 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_111111111
  NAME: str

  def __init__(self, side: Color):
    piece_name = self.__class__.NAME
    self.side = side
    # TODO: This need refractor
    self.bit = STARTING_POSITION[f"RED_{piece_name}"] if side == Color.RED else STARTING_POSITION[f"BLACK_{piece_name}"]

  def __repr__(self):
    return self.NAME[0].upper() if self.side == Color.RED else self.NAME[0].lower()


class Soldier(Piece):
  NAME = "SOLDIER"


class Cannon(Piece):
  NAME = "CANNON"


class General(Piece):
  NAME = "GENERAL"


class Advisor(Piece):
  NAME = "ADVISOR"


class Elephant(Piece):
  NAME = "ELEPHANT"


class Horse(Piece):
  NAME = "HORSE"


class Chariot(Piece):
  NAME = "CHARIOT"


class Board:
  def __init__(self):
    piece_types = [Soldier, Cannon, General, Advisor, Elephant, Horse, Chariot]
    self.red_pieces: list[Piece] = [piece(side=Color.RED) for piece in piece_types]
    self.black_pieces: list[Piece] = [piece(side=Color.BLACK) for piece in piece_types]
    self.all_pieces = self.red_pieces + self.black_pieces
    self.turn = Color.RED

  @staticmethod
  def parse_move(move: str):
    r, c = move[0], move[1]
    r = "ABCDEFGHI".index(r.upper())
    c = int(c)
    return r, c

  def at(self, start: tuple[int, int]) -> Optional[Piece]:
    mask = 1 << (start[0] * FILES + start[1])
    for piece in self.all_pieces:
      if piece.bit & mask:
        return piece
    return None

  def __repr__(self):
    ret = ""
    for i in range(RANKS):
      row = " ".join(str(s) if (s := self.at(start=(i, j))) is not None else "." for j in range(FILES))
      ret = f"{row}\n{ret}"
    return ret
