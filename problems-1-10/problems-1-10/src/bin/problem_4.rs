fn main() {
    if let Some((x, y)) = six_digit_palindrome() {
        println!("x = {}, y = {}", x, y);
        println!("Palindromic number: {}", (1000 - x) * (1000 - y));
    }
}

fn six_digit_palindrome() -> Option<(u32, u32)> {
    let mut counter: u32 = 0;
    for z in 0..10 {
        let n: u32 = 1001 - 99 * z;
        for i in 2..n {
            counter += 1;
            if n % i == 0 {
                let x: u32 = i - 1;
                let y: u32 = n / i - 1;
                let xy: u32 = x * y;
                let first_three: u32 = 1000 - (x + y);

                if first_three % 10 == xy / 100
                    && (first_three / 10) % 10 == (xy / 10) % 10
                    && first_three / 100 == xy % 10
                {
                    println!("No. values tested: {}", counter);
                    return Some((x, y));
                }
            }
        }
    }
    None
}
