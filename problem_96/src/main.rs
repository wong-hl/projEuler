
pub mod input;
mod sudoku;

fn main() {
    let sudoku_problems =
        input::process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();

    println!("{:?}", sudoku_problems.get(&1));

    if let Some(first_puzzle) =  sudoku_problems.get(&1) {
        let row_val = sudoku::get_row_values(0, first_puzzle);
        let col_val = sudoku::get_column_values(0, first_puzzle);
        let sec_val = sudoku::get_sector_values(0, first_puzzle);
        println!("{:?}, {:?} {:?}", row_val, col_val, sec_val);

        let test = sudoku::process_sudoku_vector(first_puzzle);
        println!("{:?}", test);
    } 
}
