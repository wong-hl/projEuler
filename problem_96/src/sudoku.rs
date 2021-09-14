use core::panic;
use std::cmp::PartialEq;
use std::collections::HashSet;
use std::convert::From;
use std::hash::Hash;
extern crate num;
use num::Integer;

pub fn get_row_values<T: Copy>(row_index: usize, sudoku_vec: &[T]) -> Vec<T> {
    let start_index = row_index * 9;
    let end_index = (row_index + 1) * 9;
    // sudoku_vec[start_index..end_index].to_vec()
    (start_index..end_index)
        .map(|index| -> T { *sudoku_vec.get(index).unwrap() })
        .collect::<Vec<T>>()
}

pub fn get_column_values<T: Copy>(column_index: usize, sudoku_vec: &[T]) -> Vec<T> {
    (0..9)
        .map(|row_number| *sudoku_vec.get(9 * row_number + column_index).unwrap())
        .collect::<Vec<T>>()
}

pub fn get_sector_values<T: Copy>(sector_num: usize, sudoku_vec: &[T]) -> Vec<T> {
    let start_index = (sector_num / 3) * 3 * 9 + (sector_num % 3) * 3;
    (0..9)
        .map(|local_index| {
            *sudoku_vec
                .get(start_index + local_index % 3 + (local_index / 3) * 9)
                .unwrap()
        })
        .collect()
}

#[derive(Debug, Clone)]
pub struct GridCell<T>
where
    T: Copy + PartialEq + Integer + Eq + Hash,
{
    solution: Option<T>,
    candidates: Option<HashSet<T>>,
    is_solved: bool,
}

impl<T> GridCell<T>
where
    T: Copy + PartialEq + Integer + Eq + Hash,
{
    fn new(solution: Option<T>, candidates: Option<HashSet<T>>) -> GridCell<T> {
        let is_solved = solution != None;

        if solution == None && candidates == None {
            panic!("Both solution and candidates are None")
        }

        GridCell {
            solution,
            candidates,
            is_solved,
        }
    }
}

fn find_candidate_solutions<T>(index: usize, puzzle: &[T]) -> Option<HashSet<T>>
where
    T: Copy + Eq + Hash + Integer,
    u8: Into<T>,
{
    let row_index = index / 9;
    let column_index = index % 9;
    let sector_num = (row_index / 3) * 3 + column_index / 3;

    // No need to remove value in this cell as it will be 0
    let row_vals: HashSet<T> = get_row_values(row_index, puzzle).into_iter().collect();
    let col_vals: HashSet<T> = get_column_values(column_index, puzzle)
        .into_iter()
        .collect();
    let sec_vals: HashSet<T> = get_sector_values(sector_num, puzzle).into_iter().collect();

    // Find union of all values related to cell
    let associated_vals: HashSet<T> = &(&row_vals | &col_vals) | &sec_vals;
    // Create set that contains 1 to 9
    let possible_vals: HashSet<T> = (1_u8..=9).map(|x| x.into()).into_iter().collect();

    let candidate_vals = &possible_vals - &(&possible_vals & &associated_vals);

    if candidate_vals.is_empty() {
        None
    } else {
        Some(candidate_vals)
    }
}

pub fn process_sudoku_vector<T>(puzzle: &[T]) -> Vec<GridCell<T>>
where
    T: Copy + PartialEq + Integer + Hash + Eq + From<u8>,
    u8: Into<u8>,
{
    puzzle
        .iter()
        .enumerate()
        .map(|(index, value)| -> GridCell<T> {
            if value != &T::zero() {
                GridCell::new(Some(*value), None)
            } else {
                match find_candidate_solutions(index, puzzle) {
                    Some(mut candidate_solutions) => {
                        if candidate_solutions.len() == 1 {
                            let solution = candidate_solutions.drain().next();
                            GridCell::new(solution, None)
                        } else {
                            GridCell::new(None, Some(candidate_solutions))
                        }
                    }
                    None => GridCell::new(None, None),
                }
            }
        })
        .collect::<Vec<GridCell<T>>>()
}

fn is_grid_solved<T>(sudoku_grid: &[GridCell<T>]) -> bool
where
    T: Copy + Integer + Hash,
{
    !sudoku_grid.iter().any(|cell| -> bool { !cell.is_solved })
}

mod tests {
    #[test]
    fn test_get_row_values() {
        use super::get_row_values;
        use crate::input::process_input;

        let puzzles =
            process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();
        if let Some(first_puzzle) = puzzles.get(&0) {
            let first_row = get_row_values(0, first_puzzle);
            assert_eq!(vec![0, 0, 3, 0, 2, 0, 6, 0, 0], first_row);
            let next_row = get_row_values(1, first_puzzle);
            assert_eq!(vec![9, 0, 0, 3, 0, 5, 0, 0, 1], next_row);
            let next_row = get_row_values(2, first_puzzle);
            assert_eq!(vec![0, 0, 1, 8, 0, 6, 4, 0, 0], next_row);
            let next_row = get_row_values(3, first_puzzle);
            assert_eq!(vec![0, 0, 8, 1, 0, 2, 9, 0, 0], next_row);
            let next_row = get_row_values(4, first_puzzle);
            assert_eq!(vec![7, 0, 0, 0, 0, 0, 0, 0, 8], next_row);
            let next_row = get_row_values(5, first_puzzle);
            assert_eq!(vec![0, 0, 6, 7, 0, 8, 2, 0, 0], next_row);
            let next_row = get_row_values(6, first_puzzle);
            assert_eq!(vec![0, 0, 2, 6, 0, 9, 5, 0, 0], next_row);
            let next_row = get_row_values(7, first_puzzle);
            assert_eq!(vec![8, 0, 0, 2, 0, 3, 0, 0, 9], next_row);
            let next_row = get_row_values(8, first_puzzle);
            assert_eq!(vec![0, 0, 5, 0, 1, 0, 3, 0, 0], next_row);
        }
    }

    #[test]
    fn test_get_col_values() {
        use super::get_column_values;
        use crate::input::process_input;

        let puzzles =
            process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();
        if let Some(first_puzzle) = puzzles.get(&0) {
            let first_row = get_column_values(0, first_puzzle);
            assert_eq!(vec![0, 9, 0, 0, 7, 0, 0, 8, 0], first_row);
            let next_row = get_column_values(1, first_puzzle);
            assert_eq!(vec![0, 0, 0, 0, 0, 0, 0, 0, 0], next_row);
            let next_row = get_column_values(2, first_puzzle);
            assert_eq!(vec![3, 0, 1, 8, 0, 6, 2, 0, 5], next_row);
            let next_row = get_column_values(3, first_puzzle);
            assert_eq!(vec![0, 3, 8, 1, 0, 7, 6, 2, 0], next_row);
            let next_row = get_column_values(4, first_puzzle);
            assert_eq!(vec![2, 0, 0, 0, 0, 0, 0, 0, 1], next_row);
            let next_row = get_column_values(5, first_puzzle);
            assert_eq!(vec![0, 5, 6, 2, 0, 8, 9, 3, 0], next_row);
            let next_row = get_column_values(6, first_puzzle);
            assert_eq!(vec![6, 0, 4, 9, 0, 2, 5, 0, 3], next_row);
            let next_row = get_column_values(7, first_puzzle);
            assert_eq!(vec![0, 0, 0, 0, 0, 0, 0, 0, 0], next_row);
            let next_row = get_column_values(8, first_puzzle);
            assert_eq!(vec![0, 1, 0, 0, 8, 0, 0, 9, 0], next_row);
        }
    }

    #[test]
    fn test_get_sec_values() {
        use super::get_sector_values;
        use crate::input::process_input;

        let puzzles =
            process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();
        if let Some(first_puzzle) = puzzles.get(&0) {
            let first_row = get_sector_values(0, first_puzzle);
            assert_eq!(vec![0, 0, 3, 9, 0, 0, 0, 0, 1], first_row);
            let next_row = get_sector_values(1, first_puzzle);
            assert_eq!(vec![0, 2, 0, 3, 0, 5, 8, 0, 6], next_row);
            let next_row = get_sector_values(2, first_puzzle);
            assert_eq!(vec![6, 0, 0, 0, 0, 1, 4, 0, 0], next_row);
            let next_row = get_sector_values(3, first_puzzle);
            assert_eq!(vec![0, 0, 8, 7, 0, 0, 0, 0, 6], next_row);
            let next_row = get_sector_values(4, first_puzzle);
            assert_eq!(vec![1, 0, 2, 0, 0, 0, 7, 0, 8], next_row);
            let next_row = get_sector_values(5, first_puzzle);
            assert_eq!(vec![9, 0, 0, 0, 0, 8, 2, 0, 0], next_row);
            let next_row = get_sector_values(6, first_puzzle);
            assert_eq!(vec![0, 0, 2, 8, 0, 0, 0, 0, 5], next_row);
            let next_row = get_sector_values(7, first_puzzle);
            assert_eq!(vec![6, 0, 9, 2, 0, 3, 0, 1, 0], next_row);
            let next_row = get_sector_values(8, first_puzzle);
            assert_eq!(vec![5, 0, 0, 0, 0, 9, 3, 0, 0], next_row);
        }
    }
}
