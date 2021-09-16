use crate::{primes::prime_numbers_upto, solver::prime_power_triples_solutions};

pub mod primes;
pub mod solver;

fn main() {
    let upper_limit: u32 = 50000000;
    let prime_limits = solver::PrimeBaseLimits::new(upper_limit);
    // println!("{:?}", prime_limits);
    let prime_numbers = prime_numbers_upto(prime_limits.get_square() + 1);
    // println!("{:?}", prime_numbers);
    let soln = prime_power_triples_solutions(prime_limits, prime_numbers, upper_limit);
    // println!("{:?}", soln);
    println!("Num solutions: {}", soln.len());
}
