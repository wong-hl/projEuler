use std::{collections::HashMap, fs::File, io::prelude::*, path::Path};
use ndarray::Array2;


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

fn process_input(file_name: String, num_puzzles: usize) -> Result<HashMap<u8, Array2<u8>>, String> {
    let file_contents = read_from_file(file_name);

    let sorted_input = HashMap::with_capacity(num_puzzles);

    Ok(sorted_input)
}

#[test]
fn path_to_file_works() {
    if let Ok(output) = read_from_file(String::from("p096_sudoku.txt")) {
        assert!(!output.is_empty());
    }
}