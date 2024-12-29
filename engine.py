RANKS = 10
FILES = 9

def bitboard_to_string(bitboard: int):
  ret = ""
  for rank in range(RANKS-1, -1, -1):
    row = ' '.join([f'{(bitboard >> (rank * FILES + file)) & 1}' for file in range(FILES-1, -1, -1)])
    ret += f"{row}\n"
  return ret


class Piece:
  VERTICAL = 0b100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000_100000000
  HORIZONTAL = 0b000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_000000000_111111111

  def __init__(self, bit: int):
    self.bit = bit

  def __repr__(self):
    return bitboard_to_string(self.bit)

if __name__ == "__main__":
  a = Piece(bit=Piece.HORIZONTAL)
  print(a)
  print()
  b = Piece(bit=Piece.VERTICAL)
  print(b)

