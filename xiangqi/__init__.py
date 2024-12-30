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
  A1 = 0;  B1 = 1;  C1 = 2;  D1 = 3;  E1 = 4;  F1 = 5;  G1 = 6;  H1 = 7;  I1 = 8  # noqa: E702
  A2 = 9;  B2 = 10; C2 = 11; D2 = 12; E2 = 13; F2 = 14; G2 = 15; H2 = 16; I2 = 17  # noqa: E702
  A3 = 18; B3 = 19; C3 = 20; D3 = 21; E3 = 22; F3 = 23; G3 = 24; H3 = 25; I3 = 26  # noqa: E702
  A4 = 27; B4 = 28; C4 = 29; D4 = 30; E4 = 31; F4 = 32; G4 = 33; H4 = 34; I4 = 35  # noqa: E702
  A5 = 36; B5 = 37; C5 = 38; D5 = 39; E5 = 40; F5 = 41; G5 = 42; H5 = 43; I5 = 44  # noqa: E702
  A6 = 45; B6 = 46; C6 = 47; D6 = 48; E6 = 49; F6 = 50; G6 = 51; H6 = 52; I6 = 53  # noqa: E702
  A7 = 54; B7 = 55; C7 = 56; D7 = 57; E7 = 58; F7 = 59; G7 = 60; H7 = 61; I7 = 62  # noqa: E702
  A8 = 63; B8 = 64; C8 = 65; D8 = 66; E8 = 67; F8 = 68; G8 = 69; H8 = 70; I8 = 71  # noqa: E702
  A9 = 72; B9 = 73; C9 = 74; D9 = 75; E9 = 76; F9 = 77; G9 = 78; H9 = 79; I9 = 80  # noqa: E702
  A10 = 81; B10 = 82; C10 = 83; D10 = 84; E10 = 85; F10 = 86; G10 = 87; H10 = 88; I10 = 89  # noqa: E702
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
    # FIXME: This might be wrong
    # Or, my (understanding) of mapping between square and the actual bit is wrong (prob)
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
