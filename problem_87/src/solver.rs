use std::{
    collections::HashSet,
    hash::Hash,
    ops::{Add, Mul},
};

use num::integer::Roots;

#[derive(Debug)]
pub struct PrimeBaseLimits<T>
where
    T: Roots,
{
    square: T,
    cube: T,
    fourth: T,
}

impl<T> PrimeBaseLimits<T>
where
    T: Roots,
{
    pub fn new(upper_limit: T) -> Self {
        let square = upper_limit.nth_root(2);
        let cube = upper_limit.nth_root(3);
        let fourth = upper_limit.nth_root(4);
        Self {
            square,
            cube,
            fourth,
        }
    }

    /// Get a reference to the prime base limits's square.
    pub fn get_square(&self) -> &T {
        &self.square
    }

    /// Get a reference to the prime base limits's fourth.
    pub fn get_fourth(&self) -> &T {
        &self.fourth
    }

    /// Get a reference to the prime base limits's cube.
    pub fn get_cube(&self) -> &T {
        &self.cube
    }
}

fn compute_triple<T>(prime_square: T, prime_cube: T, prime_fourth: T) -> T
where
    T: Mul<Output = T> + Add<Output = T> + Copy,
{
    prime_square * prime_square
        + prime_cube * prime_cube * prime_cube
        + prime_fourth * prime_fourth * prime_fourth * prime_fourth
}

pub fn prime_power_triples_solutions<T>(
    limits: PrimeBaseLimits<T>,
    valid_primes: Vec<T>,
) -> HashSet<T>
where
    T: Roots + Hash + Copy,
{
    let mut solutions: HashSet<T> = HashSet::with_capacity(valid_primes.len() * valid_primes.len());
    for prime_fourth in valid_primes.iter().filter(|val| val > &limits.get_fourth()) {
        for prime_cube in valid_primes.iter().filter(|val| val > &limits.get_cube()) {
            for prime_square in valid_primes.iter().filter(|val| val > &limits.get_square()) {
                solutions.insert(compute_triple(*prime_square, *prime_cube, *prime_fourth));
            }
        }
    }
    solutions
}
