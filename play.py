from xiangqi import Board, Move, Square

if __name__ == "__main__":
  b = Board()
  b.push(Move(Square.A1, Square.B1))
  print(b)
