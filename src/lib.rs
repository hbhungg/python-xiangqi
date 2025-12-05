use std::{error, marker::PhantomData};

use pyo3::{prelude::*, types::PyInt};

#[pyclass]
#[derive(Clone, Copy, Debug)]
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
pub enum Side { Red, Black }
pub struct Piece { piece_type: PieceType, side: Side }
impl Piece {
  pub fn new(piece_type: PieceType, side: Side) -> Self { Piece{piece_type, side} }
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
    if val == EMPTY || val == OUT_OF_BOUNDS { return None; }
    
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
pub struct Game { board: [u8; 144], turn: Side }

pub fn pos_to_idx(file: u8, rank: u8) -> Option<usize> {
  if file >= FILE_SZ || rank >= RANK_SZ { return None; }
  Some(((rank + 1) * 12 + (file + 1)) as usize)
}


// #[pymethods]
impl Game {
  // #[new]
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
    game.set_piece(0, 0, PieceType::Chariot, Side::Red);
    game.set_piece(1, 0, PieceType::Horse, Side::Red);
    game.set_piece(2, 0, PieceType::Elephant, Side::Red);
    game.set_piece(3, 0, PieceType::Advisor, Side::Red);
    game.set_piece(4, 0, PieceType::General, Side::Red);
    game.set_piece(5, 0, PieceType::Advisor, Side::Red);
    game.set_piece(6, 0, PieceType::Elephant, Side::Red);
    game.set_piece(7, 0, PieceType::Horse, Side::Red);
    game.set_piece(8, 0, PieceType::Chariot, Side::Red);
    
    // Rank 2: Cannons
    game.set_piece(1, 2, PieceType::Cannon, Side::Red);
    game.set_piece(7, 2, PieceType::Cannon, Side::Red);
    
    // Rank 3: Soldiers
    game.set_piece(0, 3, PieceType::Soldier, Side::Red);
    game.set_piece(2, 3, PieceType::Soldier, Side::Red);
    game.set_piece(4, 3, PieceType::Soldier, Side::Red);
    game.set_piece(6, 3, PieceType::Soldier, Side::Red);
    game.set_piece(8, 3, PieceType::Soldier, Side::Red);
    
    // Black pieces (rank 5-9)
    // Rank 9: Chariots, Horses, Elephants, Advisors, General
    game.set_piece(0, 9, PieceType::Chariot, Side::Black);
    game.set_piece(1, 9, PieceType::Horse, Side::Black);
    game.set_piece(2, 9, PieceType::Elephant, Side::Black);
    game.set_piece(3, 9, PieceType::Advisor, Side::Black);
    game.set_piece(4, 9, PieceType::General, Side::Black);
    game.set_piece(5, 9, PieceType::Advisor, Side::Black);
    game.set_piece(6, 9, PieceType::Elephant, Side::Black);
    game.set_piece(7, 9, PieceType::Horse, Side::Black);
    game.set_piece(8, 9, PieceType::Chariot, Side::Black);
    
    // Rank 7: Cannons
    game.set_piece(1, 7, PieceType::Cannon, Side::Black);
    game.set_piece(7, 7, PieceType::Cannon, Side::Black);
    
    // Rank 6: Soldiers
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

  pub fn print_board(&self) {
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

#[pyfunction]
pub fn add(left: u64, right: u64) -> u64 {
  left + right
}

pub fn subtract(left: u64, right: u64) -> u64 {
  left - right
}

#[pymodule]
#[pyo3(name = "_libxiangqi")]
fn _libxiangqi(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(add, m)?)?;
  Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
