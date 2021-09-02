use std::{fs::File, io::prelude::*, path::Path};

fn read_from_file(file_name: String) -> String {
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
        Ok(_) => file_contents
    }

}

#[test]
fn path_to_file_works() {
    assert_eq!(false, read_from_file(String::from("p096_sudoku.txt")).is_empty());
}