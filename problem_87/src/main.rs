use crate::primes::prime_numbers_upto;

pub mod primes;

fn main() {
    let prime_numbers = prime_numbers_upto(100);
    println!("{:?}", prime_numbers);
}
