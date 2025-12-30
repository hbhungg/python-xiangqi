use pyo3::create_exception;
use pyo3::prelude::*;

create_exception!(libxiangqi, IllegalMove, pyo3::exceptions::PyException);

const OUT_OF_BOUNDS: u8 = 255;
const EMPTY: u8 = 0;
const RANK_SZ: u8 = 10; // Height
const FILE_SZ: u8 = 9; // Width

#[pyclass]
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum PieceType {
  General,
  Advisor,
  Elephant,
  Horse,
  Chariot,
  Cannon,
  Soldier,
}

#[pyclass]
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Color {
  Red,
  Black,
}

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct Piece {
  piece_type: PieceType,
  color: Color,
}

#[pyclass]
#[derive(Debug, PartialEq, Eq)]
pub enum Square {
  A1 = 0,
  B1 = 1,
  C1 = 2,
  D1 = 3,
  E1 = 4,
  F1 = 5,
  G1 = 6,
  H1 = 7,
  I1 = 8,
  A2 = 9,
  B2 = 10,
  C2 = 11,
  D2 = 12,
  E2 = 13,
  F2 = 14,
  G2 = 15,
  H2 = 16,
  I2 = 17,
  A3 = 18,
  B3 = 19,
  C3 = 20,
  D3 = 21,
  E3 = 22,
  F3 = 23,
  G3 = 24,
  H3 = 25,
  I3 = 26,
  A4 = 27,
  B4 = 28,
  C4 = 29,
  D4 = 30,
  E4 = 31,
  F4 = 32,
  G4 = 33,
  H4 = 34,
  I4 = 35,
  A5 = 36,
  B5 = 37,
  C5 = 38,
  D5 = 39,
  E5 = 40,
  F5 = 41,
  G5 = 42,
  H5 = 43,
  I5 = 44,
  A6 = 45,
  B6 = 46,
  C6 = 47,
  D6 = 48,
  E6 = 49,
  F6 = 50,
  G6 = 51,
  H6 = 52,
  I6 = 53,
  A7 = 54,
  B7 = 55,
  C7 = 56,
  D7 = 57,
  E7 = 58,
  F7 = 59,
  G7 = 60,
  H7 = 61,
  I7 = 62,
  A8 = 63,
  B8 = 64,
  C8 = 65,
  D8 = 66,
  E8 = 67,
  F8 = 68,
  G8 = 69,
  H8 = 70,
  I8 = 71,
  A9 = 72,
  B9 = 73,
  C9 = 74,
  D9 = 75,
  E9 = 76,
  F9 = 77,
  G9 = 78,
  H9 = 79,
  I9 = 80,
  A10 = 81,
  B10 = 82,
  C10 = 83,
  D10 = 84,
  E10 = 85,
  F10 = 86,
  G10 = 87,
  H10 = 88,
  I10 = 89,
}

#[pyclass]
#[derive(Debug, PartialEq, Eq)]
pub struct Move {
  from_square: Square,
  to_square: Square,
}

impl Piece {
  pub fn new(piece_type: PieceType, side: Color) -> Self {
    Piece {
      piece_type,
      color: side,
    }
  }

  fn to_u8(self) -> u8 {
    let piece_val = match self.piece_type {
      PieceType::General => 1,
      PieceType::Advisor => 2,
      PieceType::Elephant => 3,
      PieceType::Horse => 4,
      PieceType::Chariot => 5,
      PieceType::Cannon => 6,
      PieceType::Soldier => 7,
    };

    let color_flag = match self.color {
      Color::Red => 0,
      Color::Black => 0b00010000,
    };

    piece_val | color_flag
  }

  fn from_u8(val: u8) -> Option<Self> {
    if val == EMPTY || val == OUT_OF_BOUNDS {
      return None;
    }

    let piece_type = val & 0b00001111;
    let is_black = (val & 0b00010000) != 0;

    let piece_type = match piece_type {
      1 => PieceType::General,
      2 => PieceType::Advisor,
      3 => PieceType::Elephant,
      4 => PieceType::Horse,
      5 => PieceType::Chariot,
      6 => PieceType::Cannon,
      7 => PieceType::Soldier,
      _ => return None,
    };

    let side = if is_black { Color::Black } else { Color::Red };
    Some(Piece {
      piece_type,
      color: side,
    })
  }
}

#[pyclass]
pub struct Board {
  board: [u8; 144],
  turn: Color,
}

pub fn pos_to_idx(file: u8, rank: u8) -> Option<usize> {
  if file >= FILE_SZ || rank >= RANK_SZ {
    return None;
  }
  Some(((rank + 1) * 12 + (file + 1)) as usize)
}

// Helper to check if position is in palace
fn in_palace(file: u8, rank: u8, side: Color) -> bool {
  if file < 3 || file > 5 {
    return false;
  }
  match side {
    Color::Red => rank <= 2,
    Color::Black => rank >= 7,
  }
}

// Helper to check if position has crossed river
fn crossed_river(rank: u8, side: Color) -> bool {
  match side {
    Color::Red => rank > 4,
    Color::Black => rank < 5,
  }
}

#[pymethods]
impl Board {
  #[new]
  pub fn new() -> Self {
    let mut board = [OUT_OF_BOUNDS; 144];

    // Clear board
    for rank in 0..RANK_SZ {
      for file in 0..FILE_SZ {
        let idx = pos_to_idx(file, rank).unwrap();
        board[idx] = EMPTY;
      }
    }

    let mut game = Board {
      board,
      turn: Color::Red,
    };

    // Red pieces (rank 0-4)
    game.set_piece(0, 0, PieceType::Chariot, Color::Red);
    game.set_piece(1, 0, PieceType::Horse, Color::Red);
    game.set_piece(2, 0, PieceType::Elephant, Color::Red);
    game.set_piece(3, 0, PieceType::Advisor, Color::Red);
    game.set_piece(4, 0, PieceType::General, Color::Red);
    game.set_piece(5, 0, PieceType::Advisor, Color::Red);
    game.set_piece(6, 0, PieceType::Elephant, Color::Red);
    game.set_piece(7, 0, PieceType::Horse, Color::Red);
    game.set_piece(8, 0, PieceType::Chariot, Color::Red);

    game.set_piece(1, 2, PieceType::Cannon, Color::Red);
    game.set_piece(7, 2, PieceType::Cannon, Color::Red);

    game.set_piece(0, 3, PieceType::Soldier, Color::Red);
    game.set_piece(2, 3, PieceType::Soldier, Color::Red);
    game.set_piece(4, 3, PieceType::Soldier, Color::Red);
    game.set_piece(6, 3, PieceType::Soldier, Color::Red);
    game.set_piece(8, 3, PieceType::Soldier, Color::Red);

    // Black pieces (rank 5-9)
    game.set_piece(0, 9, PieceType::Chariot, Color::Black);
    game.set_piece(1, 9, PieceType::Horse, Color::Black);
    game.set_piece(2, 9, PieceType::Elephant, Color::Black);
    game.set_piece(3, 9, PieceType::Advisor, Color::Black);
    game.set_piece(4, 9, PieceType::General, Color::Black);
    game.set_piece(5, 9, PieceType::Advisor, Color::Black);
    game.set_piece(6, 9, PieceType::Elephant, Color::Black);
    game.set_piece(7, 9, PieceType::Horse, Color::Black);
    game.set_piece(8, 9, PieceType::Chariot, Color::Black);

    game.set_piece(1, 7, PieceType::Cannon, Color::Black);
    game.set_piece(7, 7, PieceType::Cannon, Color::Black);

    game.set_piece(0, 6, PieceType::Soldier, Color::Black);
    game.set_piece(2, 6, PieceType::Soldier, Color::Black);
    game.set_piece(4, 6, PieceType::Soldier, Color::Black);
    game.set_piece(6, 6, PieceType::Soldier, Color::Black);
    game.set_piece(8, 6, PieceType::Soldier, Color::Black);

    game
  }

  pub fn set_piece(&mut self, file: u8, rank: u8, piece_type: PieceType, side: Color) -> Option<()> {
    let idx = pos_to_idx(file, rank)?;
    self.board[idx] = Piece::new(piece_type, side).to_u8();
    Some(())
  }

  pub fn get_piece(&self, file: u8, rank: u8) -> Option<Piece> {
    let idx = pos_to_idx(file, rank)?;
    Piece::from_u8(self.board[idx])
  }

  fn get_at_idx(&self, idx: usize) -> u8 {
    self.board[idx]
  }

  // Check if a move is valid for General
  fn is_valid_general_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Color) -> bool {
    // Must stay in palace
    if !in_palace(to_file, to_rank, side) {
      return false;
    }

    // Can only move one step orthogonally
    let file_diff = (from_file as i8 - to_file as i8).abs();
    let rank_diff = (from_rank as i8 - to_rank as i8).abs();

    (file_diff == 1 && rank_diff == 0) || (file_diff == 0 && rank_diff == 1)
  }

  // Check if a move is valid for Advisor
  fn is_valid_advisor_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Color) -> bool {
    // Must stay in palace
    if !in_palace(to_file, to_rank, side) {
      return false;
    }

    // Can only move one step diagonally
    let file_diff = (from_file as i8 - to_file as i8).abs();
    let rank_diff = (from_rank as i8 - to_rank as i8).abs();

    file_diff == 1 && rank_diff == 1
  }

  // Check if a move is valid for Elephant
  fn is_valid_elephant_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Color) -> bool {
    // Cannot cross river
    match side {
      Color::Red => {
        if to_rank > 4 {
          return false;
        }
      },
      Color::Black => {
        if to_rank < 5 {
          return false;
        }
      },
    }

    // Must move exactly 2 steps diagonally
    let file_diff = from_file as i8 - to_file as i8;
    let rank_diff = from_rank as i8 - to_rank as i8;

    if file_diff.abs() != 2 || rank_diff.abs() != 2 {
      return false;
    }

    // Check if blocked (elephant eye)
    let mid_file = ((from_file as i8 + to_file as i8) / 2) as u8;
    let mid_rank = ((from_rank as i8 + to_rank as i8) / 2) as u8;
    let mid_idx = pos_to_idx(mid_file, mid_rank).unwrap();

    self.board[mid_idx] == EMPTY
  }

  // Check if a move is valid for Horse
  fn is_valid_horse_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8) -> bool {
    let file_diff = (from_file as i8 - to_file as i8).abs();
    let rank_diff = (from_rank as i8 - to_rank as i8).abs();

    // Must move in L-shape (1-2 or 2-1)
    if !((file_diff == 1 && rank_diff == 2) || (file_diff == 2 && rank_diff == 1)) {
      return false;
    }

    // Check if blocked (horse leg)
    let (block_file, block_rank) = if file_diff == 2 {
      // Moving horizontally more, check horizontal block
      (((from_file as i8 + to_file as i8) / 2) as u8, from_rank)
    } else {
      // Moving vertically more, check vertical block
      (from_file, ((from_rank as i8 + to_rank as i8) / 2) as u8)
    };

    let block_idx = pos_to_idx(block_file, block_rank).unwrap();
    self.board[block_idx] == EMPTY
  }

  // Check if a move is valid for Chariot (Rook)
  fn is_valid_chariot_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8) -> bool {
    // Must move in straight line
    if from_file != to_file && from_rank != to_rank {
      return false;
    }

    // Check path is clear
    if from_file == to_file {
      // Moving vertically
      let (start, end) = if from_rank < to_rank {
        (from_rank + 1, to_rank)
      } else {
        (to_rank + 1, from_rank)
      };

      for rank in start..end {
        let idx = pos_to_idx(from_file, rank).unwrap();
        if self.board[idx] != EMPTY {
          return false;
        }
      }
    } else {
      // Moving horizontally
      let (start, end) = if from_file < to_file {
        (from_file + 1, to_file)
      } else {
        (to_file + 1, from_file)
      };

      for file in start..end {
        let idx = pos_to_idx(file, from_rank).unwrap();
        if self.board[idx] != EMPTY {
          return false;
        }
      }
    }

    true
  }

  // Check if a move is valid for Cannon
  fn is_valid_cannon_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, is_capture: bool) -> bool {
    // Must move in straight line
    if from_file != to_file && from_rank != to_rank {
      return false;
    }

    // Count pieces in between
    let mut pieces_between = 0;

    if from_file == to_file {
      // Moving vertically
      let (start, end) = if from_rank < to_rank {
        (from_rank + 1, to_rank)
      } else {
        (to_rank + 1, from_rank)
      };

      for rank in start..end {
        let idx = pos_to_idx(from_file, rank).unwrap();
        if self.board[idx] != EMPTY {
          pieces_between += 1;
        }
      }
    } else {
      // Moving horizontally
      let (start, end) = if from_file < to_file {
        (from_file + 1, to_file)
      } else {
        (to_file + 1, from_file)
      };

      for file in start..end {
        let idx = pos_to_idx(file, from_rank).unwrap();
        if self.board[idx] != EMPTY {
          pieces_between += 1;
        }
      }
    }

    // If capturing, must have exactly 1 piece between (the screen)
    // If not capturing, must have 0 pieces between
    if is_capture {
      pieces_between == 1
    } else {
      pieces_between == 0
    }
  }

  // Check if a move is valid for Soldier
  fn is_valid_soldier_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Color) -> bool {
    let file_diff = (from_file as i8 - to_file as i8).abs();
    let rank_diff = from_rank as i8 - to_rank as i8;

    let has_crossed = crossed_river(from_rank, side);

    match side {
      Color::Red => {
        // Red moves up (increasing rank)
        if rank_diff == -1 && file_diff == 0 {
          // Forward move always allowed
          true
        } else if has_crossed && rank_diff == 0 && file_diff == 1 {
          // Sideways move only after crossing river
          true
        } else {
          false
        }
      },
      Color::Black => {
        // Black moves down (decreasing rank)
        if rank_diff == 1 && file_diff == 0 {
          // Forward move always allowed
          true
        } else if has_crossed && rank_diff == 0 && file_diff == 1 {
          // Sideways move only after crossing river
          true
        } else {
          false
        }
      },
    }
  }

  pub fn get_legal_moves(&self) -> Vec<(u8, u8, u8, u8)> {
    let mut moves = Vec::new();

    for from_rank in 0..RANK_SZ {
      for from_file in 0..FILE_SZ {
        if let Some(piece) = self.get_piece(from_file, from_rank) {
          if piece.color != self.turn {
            continue;
          }

          for to_rank in 0..RANK_SZ {
            for to_file in 0..FILE_SZ {
              // Check destination
              if let Some(dest) = self.get_piece(to_file, to_rank) {
                if dest.color == piece.color {
                  continue;
                }
              }

              let is_capture = self.get_piece(to_file, to_rank).is_some();

              let is_valid = match piece.piece_type {
                PieceType::General => self.is_valid_general_move(from_file, from_rank, to_file, to_rank, piece.color),
                PieceType::Advisor => self.is_valid_advisor_move(from_file, from_rank, to_file, to_rank, piece.color),
                PieceType::Elephant => self.is_valid_elephant_move(from_file, from_rank, to_file, to_rank, piece.color),
                PieceType::Horse => self.is_valid_horse_move(from_file, from_rank, to_file, to_rank),
                PieceType::Chariot => self.is_valid_chariot_move(from_file, from_rank, to_file, to_rank),
                PieceType::Cannon => self.is_valid_cannon_move(from_file, from_rank, to_file, to_rank, is_capture),
                PieceType::Soldier => self.is_valid_soldier_move(from_file, from_rank, to_file, to_rank, piece.color),
              };

              if is_valid {
                moves.push((from_file, from_rank, to_file, to_rank));
              }
            }
          }
        }
      }
    }

    moves
  }

  // Main function to validate and execute a move
  pub fn make_move(&mut self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8) -> PyResult<()> {
    // Check positions are valid
    // let from_idx = pos_to_idx(from_file, from_rank).ok_or("Invalid from position")?;
    // let to_idx = pos_to_idx(to_file, to_rank).ok_or("Invalid to position")?;
    let from_idx = pos_to_idx(from_file, from_rank)
      .ok_or_else(|| IllegalMove::new_err(format!("Invalid from position ({from_file}, {from_rank})")))?;

    let to_idx = pos_to_idx(to_file, to_rank)
      .ok_or_else(|| IllegalMove::new_err(format!("Invalid to position ({to_file}, {to_rank})")))?;

    // Check there's a piece at source
    let piece = self
      .get_piece(from_file, from_rank)
      .ok_or_else(|| IllegalMove::new_err(format!("({from_file}, {from_rank}) has no piece")))?;

    // Check it's the correct player's turn
    if piece.color != self.turn {
      return Err(IllegalMove::new_err("Not turn"));
    }

    // Check destination
    let dest_piece = self.get_piece(to_file, to_rank);
    let is_capture = dest_piece.is_some();

    // Can't capture own piece
    if let Some(dest) = dest_piece {
      if dest.color == piece.color {
        return Err(IllegalMove::new_err("Cannot capture own piece"));
      }
    }

    // Validate move based on piece type
    let is_valid = match piece.piece_type {
      PieceType::General => self.is_valid_general_move(from_file, from_rank, to_file, to_rank, piece.color),
      PieceType::Advisor => self.is_valid_advisor_move(from_file, from_rank, to_file, to_rank, piece.color),
      PieceType::Elephant => self.is_valid_elephant_move(from_file, from_rank, to_file, to_rank, piece.color),
      PieceType::Horse => self.is_valid_horse_move(from_file, from_rank, to_file, to_rank),
      PieceType::Chariot => self.is_valid_chariot_move(from_file, from_rank, to_file, to_rank),
      PieceType::Cannon => self.is_valid_cannon_move(from_file, from_rank, to_file, to_rank, is_capture),
      PieceType::Soldier => self.is_valid_soldier_move(from_file, from_rank, to_file, to_rank, piece.color),
    };

    if !is_valid {
      return Err(IllegalMove::new_err(format!("Invalid move for {:?}", piece.piece_type)));
    }

    // Execute the move
    self.board[to_idx] = self.board[from_idx];
    self.board[from_idx] = EMPTY;

    // Switch turns
    self.turn = match self.turn {
      Color::Red => Color::Black,
      Color::Black => Color::Red,
    };

    Ok(())
  }

  pub fn ascii(&self) -> String {
    let mut output = String::new();
    for rank in (0..RANK_SZ).rev() {
      for file in 0..FILE_SZ {
        if let Some(idx) = pos_to_idx(file, rank) {
          let piece_val = self.board[idx];
          let symbol = if piece_val == EMPTY {
            '.'
          } else if piece_val == OUT_OF_BOUNDS {
            'X'
          } else if let Some(piece) = Piece::from_u8(piece_val) {
            let base = match piece.piece_type {
              PieceType::General => 'G',
              PieceType::Advisor => 'A',
              PieceType::Elephant => 'E',
              PieceType::Horse => 'H',
              PieceType::Chariot => 'R',
              PieceType::Cannon => 'C',
              PieceType::Soldier => 'S',
            };
            match piece.color {
              Color::Red => base,
              Color::Black => base.to_lowercase().next().unwrap(),
            }
          } else {
            '?'
          };
          output.push(symbol);
          output.push(' ');
        } else {
          output.push_str("X ");
        }
      }
      output.push('\n');
    }
    output.push('\n');

    output
  }

  pub fn turn(&self) -> bool {
    match self.turn {
      Color::Red => true,
      Color::Black => false,
    }
  }
}

#[pymodule]
#[pyo3(name = "_libxiangqi")]
fn _libxiangqi(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_class::<Board>()?;
  m.add("IllegalMove", m.py().get_type::<IllegalMove>())?;
  Ok(())
}
