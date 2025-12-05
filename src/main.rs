use libxiangqi::Game;

fn main() {
  let mut game = Game::new();
  loop {
    game.print_board();
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    let n: Vec<u8> = input.split_whitespace().map(|s| s.parse().unwrap()).collect();
    game.make_move(n[0], n[1], n[2], n[3]).unwrap();
  }
}