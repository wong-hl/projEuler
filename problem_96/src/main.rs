mod input;

fn main() {
    let sudoku_problems =
        input::process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();

    println!("{:?}", sudoku_problems);
}
