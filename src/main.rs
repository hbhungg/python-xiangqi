use libxiangqi::Game;

fn main() {
  let mut game = Game::new();
  loop {
    game.print_board();
    let legal_moves = game.get_legal_moves();
    println!("Legal moves: {legal_moves:?}");
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    let n: Vec<u8> = input.split_whitespace().map(|s| s.parse().unwrap()).collect();
    if let Err(err) = game.make_move(n[0], n[1], n[2], n[3]) {
      println!("Move error: {err}");
    };
  }
}
