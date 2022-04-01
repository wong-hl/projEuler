fn main() {
    // let target_value: u64 = 13195;
    let target_value: u64 = 600851475143;
    let sieve: Vec<usize> = find_primes_up_to(square_root(target_value) as u64);
    println!("{:?}", &sieve);
    let largest_prime: Option<usize> =
        find_largest_prime_factor(&sieve, target_value as usize);
    println!(
        "Largest prime factor of {} is {}",
        target_value,
        largest_prime.unwrap()
    );
}

fn square_root(value: u64) -> f64 {
    (value as f64).sqrt().ceil()
}

fn sieve_of_eratosthenes(max_value: u64) -> Vec<bool> {
    let max_val: usize = max_value as usize;
    let mut is_prime: Vec<bool> = vec![true; max_val - 2];
    let sqrt_n: usize = square_root(max_value) as usize;

    (2..sqrt_n).for_each(|index: usize| {
        if let Some(true) = is_prime.get(index - 2) {
            let max_k: usize = (max_val - index * index - 1) / index;
            (0..=max_k).for_each(|k: usize| {
                is_prime[index * index + k * index - 2] = false
            });
        }
    });

    is_prime
}

fn find_primes_up_to(max_value: u64) -> Vec<usize> {
    sieve_of_eratosthenes(max_value)
        .iter()
        .enumerate()
        .filter_map(
            |(index, is_prime)| if *is_prime { Some(index + 2) } else { None },
        )
        .collect()
}

fn find_largest_prime_factor(
    primes: &[usize],
    target_value: usize,
) -> Option<usize> {
    let prime_factor: Option<&usize> = primes
        .iter()
        .rev()
        .find(|prime| target_value % **prime == 0);
    if let Some(largest_prime_factor) = prime_factor {
        Some(*largest_prime_factor)
    } else {
        None
    }
}
