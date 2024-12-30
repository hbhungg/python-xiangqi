from enum import Enum, auto
from queue import Queue
from typing import Optional
from dataclasses import dataclass, field


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
  return piece_type.name[0].lower() if piece_type != PieceType.CHARIOT else "r"


def piece_name(piece_type: PieceType) -> str:
  return piece_type.name.lower()


class Color(Enum):
  RED = True
  BLACK = False


# fmt: off
class Square(Enum):
  A1 = 0;  A2 = 1;  A3 = 2;  A4 = 3;  A5 = 4;  A6 = 5;  A7 = 6;  A8 = 7;  A9 = 8;  A10 = 9  # noqa: E702
  B1 = 10; B2 = 11; B3 = 12; B4 = 13; B5 = 14; B6 = 15; B7 = 16; B8 = 17; B9 = 18; B10 = 19 # noqa: E702
  C1 = 20; C2 = 21; C3 = 22; C4 = 23; C5 = 24; C6 = 25; C7 = 26; C8 = 27; C9 = 28; C10 = 29 # noqa: E702
  D1 = 30; D2 = 31; D3 = 32; D4 = 33; D5 = 34; D6 = 35; D7 = 36; D8 = 37; D9 = 38; D10 = 39 # noqa: E702
  E1 = 40; E2 = 41; E3 = 42; E4 = 43; E5 = 44; E6 = 45; E7 = 46; E8 = 47; E9 = 48; E10 = 49 # noqa: E702
  F1 = 50; F2 = 51; F3 = 52; F4 = 53; F5 = 54; F6 = 55; F7 = 56; F8 = 57; F9 = 58; F10 = 59 # noqa: E702
  G1 = 60; G2 = 61; G3 = 62; G4 = 63; G5 = 64; G6 = 65; G7 = 66; G8 = 67; G9 = 68; G10 = 69 # noqa: E702
  H1 = 70; H2 = 71; H3 = 72; H4 = 73; H5 = 74; H6 = 75; H7 = 76; H8 = 77; H9 = 78; H10 = 79 # noqa: E702
  I1 = 80; I2 = 81; I3 = 82; I4 = 83; I5 = 84; I6 = 85; I7 = 86; I8 = 87; I9 = 88; I10 = 89 # noqa: E702
# fmt: on


STARTING_POSITION = {
  Color.RED: {
    PieceType.SOLDIER: 0b000000000_000000000_000000000_000000000_000000000_000000000_101010101_000000000_000000000_000000000,
    PieceType.CANNON: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010_000000000_000000000,
    PieceType.GENERAL: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000010000,
    PieceType.ADVISOR: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000101000,
    PieceType.ELEPHANT: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_001000100,
    PieceType.HORSE: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010,
    PieceType.CHARIOT: 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_100000001,
  },
  Color.BLACK: {
    PieceType.SOLDIER: 0b000000000_000000000_000000000_101010101_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.CANNON: 0b000000000_000000000_010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.GENERAL: 0b000010000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.ADVISOR: 0b000101000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.ELEPHANT: 0b001000100_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.HORSE: 0b010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
    PieceType.CHARIOT: 0b100000001_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  },
  "MISC": {
    "VERTICAL": 0b100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000,
    "HORIZONTAL": 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_111111111,
  },
}


@dataclass
class Piece:
  piece_type: PieceType
  color: Color
  bit: int = field(init=False)

  def __post_init__(self):
    self.bit = STARTING_POSITION[self.color][self.piece_type]

  def __repr__(self):
    s = piece_symbol(self.piece_type)
    return s.upper() if self.color == Color.RED else s.lower()


@dataclass
class Move:
  from_square: Square
  to_square: Square


class Board:
  def __init__(self):
    self.red_pieces: list[Piece] = [Piece(piece_type=pt, color=Color.RED) for pt in PieceType]
    self.black_pieces: list[Piece] = [Piece(piece_type=pt, color=Color.BLACK) for pt in PieceType]
    self.all_pieces = self.red_pieces + self.black_pieces
    self.moves: Queue[Move] = Queue(maxsize=0)
    self.turn = Color.RED

  def at(self, square: Square) -> Optional[Piece]:
    mask = self.mask(square)
    for piece in self.all_pieces:
      if piece.bit & mask:
        return piece
    return None

  @staticmethod
  def mask(square: Square) -> int:
    return 1 << square.value

  def push(self, move: Move):
    piece_at = self.at(move.from_square)
    fm = self.mask(move.from_square)
    tm = self.mask(move.to_square)
    print(bin(piece_at.bit), bin(fm), bin(tm))
    piece_at.bit = piece_at.bit ^ fm
    print(bin(piece_at.bit), bin(fm), bin(tm))
    piece_at.bit = piece_at.bit | tm
    print(bin(piece_at.bit), bin(fm), bin(tm))
    self.moves.put(move)

  def pop(self):
    return self.moves.get()

  def __repr__(self):
    ret = ""
    for i in range(RANKS):
      row = " ".join(str(s) if (s := self.at(square=Square(i * FILES + j))) is not None else "." for j in range(FILES))
      ret = f"{row}\n{ret}"
    return ret
