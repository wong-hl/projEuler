use std::{collections::HashMap, fs::File, io::prelude::*, path::Path};
use ndarray::{Array, Array2};


fn read_from_file(file_name: String) -> Result<String, String> {
    // https://doc.rust-lang.org/stable/rust-by-example/std_misc/file/open.html

    let input_path: &Path = Path::new(&file_name);
    let file_display = input_path.display();

    // Open the path in read-only mode, returns `io::Result<File>`
    let mut file: File = match File::open(&input_path) {
        Err(why) => panic!("couldn't open {}: {}", file_display, why),
        Ok(file) => file,
    };

    // Read the file contents into a string, returns `io::Result<usize>`
    let mut file_contents = String::new();
    match file.read_to_string(&mut file_contents) {
        Err(why) => panic!("couldn't read {}: {}", file_display, why),
        Ok(_) => Ok(file_contents),
    }

}

fn process_input(file_name: String, num_puzzles: usize, identifier: String) -> Result<HashMap<usize, Array2<u32>>, String> {
    let file_contents = read_from_file(file_name)?;

    let mut sorted_input: HashMap<usize, ndarray::ArrayBase<ndarray::OwnedRepr<u32>, ndarray::Dim<[usize; 2]>>> = HashMap::with_capacity(num_puzzles);

    let mut storage_vector: Vec<u32> = Vec::with_capacity(81);

    for (counter, line) in file_contents.lines().enumerate() {
        if counter == 0 {
            continue;
        } else if line.contains(identifier.as_str()) || line.contains("End") {
            let grid_num = counter/10;
            sorted_input.insert(grid_num, Array::from_shape_vec((9,9), storage_vector).expect("Unable to reshape to 9 by 9"));
            storage_vector = Vec::with_capacity(81);
        } else {
            line.chars().for_each(|ch| storage_vector.push(ch.to_digit(10).unwrap()));
        }

    }

    Ok(sorted_input)
}

#[test]
fn path_to_file_works() {
    if let Ok(output) = read_from_file(String::from("p096_sudoku.txt")) {
        assert!(!output.is_empty());
    }
}

#[test]
fn process_input_works() {
    let output = process_input(String::from("p096_sudoku.txt"), 50, String::from("Grid")).unwrap();
    println!("{:?}", output);
    assert!(!output.is_empty());

}