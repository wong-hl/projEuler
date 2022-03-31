fn main() {
    let mut previous: u32 = 1;
    let mut current: u32 = 2;
    let mut total: u32 = 2;

    while current < 4000000 - previous {
        let next: u32 = previous + current;

        if next & 1 == 0 {
            total += next;
        }

        previous = current;
        current = next;
    }

    println!("Sum of even fibonacci numbers: {}", total)
}
