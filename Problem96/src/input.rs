use std::fs;
use std::path::Path;

fn path_to_file(file_name: String) -> &Path {
    let out_path: &Path = Path::new(&file_name);

    if out_path.exists() {
        &out_path
    } else {
        panic!("{} file does not exits", file_name);
    }
}

