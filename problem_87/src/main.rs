use crate::primes::prime_numbers_upto;

pub mod primes;
pub mod solver;

fn main() {
    let upper_limit: u32 = 50;
    let prime_limits = solver::PrimeBaseLimits::new(upper_limit);
    println!("{:?}", prime_limits);
    let prime_numbers = prime_numbers_upto(prime_limits.get_square() + 1);
    println!("{:?}", prime_numbers);
}
