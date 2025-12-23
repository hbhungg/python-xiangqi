use pyo3::create_exception;
use pyo3::prelude::*;

create_exception!(libxiangqi, IllegalMove, pyo3::exceptions::PyException);

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
pub enum Side {
  Red,
  Black,
}

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct Piece {
  piece_type: PieceType,
  side: Side,
}

impl Piece {
  pub fn new(piece_type: PieceType, side: Side) -> Self {
    Piece { piece_type, side }
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

    let color_flag = match self.side {
      Side::Red => 0,
      Side::Black => 0b00010000,
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

    let side = if is_black { Side::Black } else { Side::Red };
    Some(Piece { piece_type, side })
  }
}

const OUT_OF_BOUNDS: u8 = 255;
const EMPTY: u8 = 0;
const RANK_SZ: u8 = 10; // Height
const FILE_SZ: u8 = 9; // Width

#[pyclass]
pub struct Game {
  board: [u8; 144],
  turn: Side,
}

pub fn pos_to_idx(file: u8, rank: u8) -> Option<usize> {
  if file >= FILE_SZ || rank >= RANK_SZ {
    return None;
  }
  Some(((rank + 1) * 12 + (file + 1)) as usize)
}

// Helper to check if position is in palace
fn in_palace(file: u8, rank: u8, side: Side) -> bool {
  if file < 3 || file > 5 {
    return false;
  }
  match side {
    Side::Red => rank <= 2,
    Side::Black => rank >= 7,
  }
}

// Helper to check if position has crossed river
fn crossed_river(rank: u8, side: Side) -> bool {
  match side {
    Side::Red => rank > 4,
    Side::Black => rank < 5,
  }
}

#[pymethods]
impl Game {
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

    let mut game = Game { board, turn: Side::Red };

    // Red pieces (rank 0-4)
    game.set_piece(0, 0, PieceType::Chariot, Side::Red);
    game.set_piece(1, 0, PieceType::Horse, Side::Red);
    game.set_piece(2, 0, PieceType::Elephant, Side::Red);
    game.set_piece(3, 0, PieceType::Advisor, Side::Red);
    game.set_piece(4, 0, PieceType::General, Side::Red);
    game.set_piece(5, 0, PieceType::Advisor, Side::Red);
    game.set_piece(6, 0, PieceType::Elephant, Side::Red);
    game.set_piece(7, 0, PieceType::Horse, Side::Red);
    game.set_piece(8, 0, PieceType::Chariot, Side::Red);

    game.set_piece(1, 2, PieceType::Cannon, Side::Red);
    game.set_piece(7, 2, PieceType::Cannon, Side::Red);

    game.set_piece(0, 3, PieceType::Soldier, Side::Red);
    game.set_piece(2, 3, PieceType::Soldier, Side::Red);
    game.set_piece(4, 3, PieceType::Soldier, Side::Red);
    game.set_piece(6, 3, PieceType::Soldier, Side::Red);
    game.set_piece(8, 3, PieceType::Soldier, Side::Red);

    // Black pieces (rank 5-9)
    game.set_piece(0, 9, PieceType::Chariot, Side::Black);
    game.set_piece(1, 9, PieceType::Horse, Side::Black);
    game.set_piece(2, 9, PieceType::Elephant, Side::Black);
    game.set_piece(3, 9, PieceType::Advisor, Side::Black);
    game.set_piece(4, 9, PieceType::General, Side::Black);
    game.set_piece(5, 9, PieceType::Advisor, Side::Black);
    game.set_piece(6, 9, PieceType::Elephant, Side::Black);
    game.set_piece(7, 9, PieceType::Horse, Side::Black);
    game.set_piece(8, 9, PieceType::Chariot, Side::Black);

    game.set_piece(1, 7, PieceType::Cannon, Side::Black);
    game.set_piece(7, 7, PieceType::Cannon, Side::Black);

    game.set_piece(0, 6, PieceType::Soldier, Side::Black);
    game.set_piece(2, 6, PieceType::Soldier, Side::Black);
    game.set_piece(4, 6, PieceType::Soldier, Side::Black);
    game.set_piece(6, 6, PieceType::Soldier, Side::Black);
    game.set_piece(8, 6, PieceType::Soldier, Side::Black);

    game
  }

  pub fn set_piece(&mut self, file: u8, rank: u8, piece_type: PieceType, side: Side) -> Option<()> {
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
  fn is_valid_general_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Side) -> bool {
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
  fn is_valid_advisor_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Side) -> bool {
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
  fn is_valid_elephant_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Side) -> bool {
    // Cannot cross river
    match side {
      Side::Red => {
        if to_rank > 4 {
          return false;
        }
      },
      Side::Black => {
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
  fn is_valid_soldier_move(&self, from_file: u8, from_rank: u8, to_file: u8, to_rank: u8, side: Side) -> bool {
    let file_diff = (from_file as i8 - to_file as i8).abs();
    let rank_diff = from_rank as i8 - to_rank as i8;

    let has_crossed = crossed_river(from_rank, side);

    match side {
      Side::Red => {
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
      Side::Black => {
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
          if piece.side != self.turn {
            continue;
          }

          for to_rank in 0..RANK_SZ {
            for to_file in 0..FILE_SZ {
              // Check destination
              if let Some(dest) = self.get_piece(to_file, to_rank) {
                if dest.side == piece.side {
                  continue;
                }
              }

              let is_capture = self.get_piece(to_file, to_rank).is_some();

              let is_valid = match piece.piece_type {
                PieceType::General => self.is_valid_general_move(from_file, from_rank, to_file, to_rank, piece.side),
                PieceType::Advisor => self.is_valid_advisor_move(from_file, from_rank, to_file, to_rank, piece.side),
                PieceType::Elephant => self.is_valid_elephant_move(from_file, from_rank, to_file, to_rank, piece.side),
                PieceType::Horse => self.is_valid_horse_move(from_file, from_rank, to_file, to_rank),
                PieceType::Chariot => self.is_valid_chariot_move(from_file, from_rank, to_file, to_rank),
                PieceType::Cannon => self.is_valid_cannon_move(from_file, from_rank, to_file, to_rank, is_capture),
                PieceType::Soldier => self.is_valid_soldier_move(from_file, from_rank, to_file, to_rank, piece.side),
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
    if piece.side != self.turn {
      return Err(IllegalMove::new_err("Not turn"));
    }

    // Check destination
    let dest_piece = self.get_piece(to_file, to_rank);
    let is_capture = dest_piece.is_some();

    // Can't capture own piece
    if let Some(dest) = dest_piece {
      if dest.side == piece.side {
        return Err(IllegalMove::new_err("Cannot capture own piece"));
      }
    }

    // Validate move based on piece type
    let is_valid = match piece.piece_type {
      PieceType::General => self.is_valid_general_move(from_file, from_rank, to_file, to_rank, piece.side),
      PieceType::Advisor => self.is_valid_advisor_move(from_file, from_rank, to_file, to_rank, piece.side),
      PieceType::Elephant => self.is_valid_elephant_move(from_file, from_rank, to_file, to_rank, piece.side),
      PieceType::Horse => self.is_valid_horse_move(from_file, from_rank, to_file, to_rank),
      PieceType::Chariot => self.is_valid_chariot_move(from_file, from_rank, to_file, to_rank),
      PieceType::Cannon => self.is_valid_cannon_move(from_file, from_rank, to_file, to_rank, is_capture),
      PieceType::Soldier => self.is_valid_soldier_move(from_file, from_rank, to_file, to_rank, piece.side),
    };

    if !is_valid {
      return Err(IllegalMove::new_err(format!("Invalid move for {:?}", piece.piece_type)));
    }

    // Execute the move
    self.board[to_idx] = self.board[from_idx];
    self.board[from_idx] = EMPTY;

    // Switch turns
    self.turn = match self.turn {
      Side::Red => Side::Black,
      Side::Black => Side::Red,
    };

    Ok(())
  }

  pub fn print_board(&self) {
    println!("\nCurrent turn: {:?}", self.turn);
    // Print from rank 9 down to 0 (so rank 0 is at bottom)
    for rank in (0..RANK_SZ).rev() {
      print!("{} ", rank);

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
            match piece.side {
              Side::Red => base,
              Side::Black => base.to_lowercase().next().unwrap(),
            }
          } else {
            '?'
          };
          print!("{} ", symbol);
        } else {
          print!("X ");
        }
      }
      println!();
    }

    // Print file numbers at bottom
    print!("  ");
    for file in 0..FILE_SZ {
      print!("{} ", file);
    }
    println!();
  }
}

#[pymodule]
#[pyo3(name = "_libxiangqi")]
fn _libxiangqi(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_class::<Game>()?;
  m.add("IllegalMove", m.py().get_type::<IllegalMove>())?;
  Ok(())
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn test_soldier_moves() {
    let mut game = Game::new();

    // Red soldier can move forward
    assert!(game.make_move(4, 3, 4, 4).is_ok());

    // Black soldier can move forward
    assert!(game.make_move(4, 6, 4, 5).is_ok());

    // Red soldier can't move sideways before crossing river
    assert!(game.make_move(2, 3, 3, 3).is_err());
  }

  #[test]
  fn test_chariot_moves() {
    let mut game = Game::new();

    // Move soldier out of the way
    game.make_move(0, 3, 0, 4).unwrap();
    game.make_move(0, 6, 0, 5).unwrap();

    // Chariot can now move forward
    assert!(game.make_move(0, 0, 0, 3).is_ok());
  }
}
