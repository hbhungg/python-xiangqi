from collections import namedtuple
from enum import Enum
from typing import Optional


RANKS = 10
FILES = 9

# TODO: This need refractor
STARTING_POSITION = {
  "RED_SOLDIER"    : 0b000000000_000000000_000000000_000000000_000000000_000000000_101010101_000000000_000000000_000000000,
  "RED_CANNON"     : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010_000000000_000000000,
  "RED_GENERAL"    : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000010000,
  "RED_ADVISOR"    : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000101000,
  "RED_ELEPHANT"   : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_001000100,
  "RED_HORSE"      : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_010000010,
  "RED_CHARIOT"    : 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_100000001,

  "BLACK_SOLDIER"  : 0b000000000_000000000_000000000_101010101_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_CANNON"   : 0b000000000_000000000_010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_GENERAL"  : 0b000010000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_ADVISOR"  : 0b000101000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_ELEPHANT" : 0b001000100_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_HORSE"    : 0b010000010_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
  "BLACK_CHARIOT"  : 0b100000001_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000,
}

class Side(Enum):
  RED=True
  BLACK=False

class Piece:
  VERTICAL = 0b100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000
  HORIZONTAL = 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_111111111
  NAME: str

  def __init__(self, side: Side):
    piece_name = self.__class__.NAME
    self.side = side
    # TODO: This need refractor
    self.bit = STARTING_POSITION[f"RED_{piece_name}"] if side == Side.RED else STARTING_POSITION[f"BLACK_{piece_name}"]
  
  def __repr__(self):
    return self.NAME[0].upper() if self.side == Side.RED else self.NAME[0].lower()
  # def __repr__(self):
  #   return bitboard_to_string(self.bit)

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
    self.red_pieces: list[Piece] = [piece(side=Side.RED) for piece in piece_types]
    self.black_pieces: list[Piece] = [piece(side=Side.BLACK) for piece in piece_types]
    self.all_pieces = self.red_pieces + self.black_pieces
    self.turn = Side.RED
  
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
