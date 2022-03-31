fn main() {
    let sieve = primes_up_to(9);
    println!("{:?}", &sieve);
}

fn sieve_of_eratosthenes(max_value: u64) -> Vec<bool> {
    let max_val: usize = max_value as usize;
    let mut is_prime: Vec<bool> = vec![true; max_val - 2];
    let sqrt_n: usize = (max_value as f64).sqrt().ceil() as usize;

    (2..sqrt_n).for_each(|index: usize| {
        if let Some(true) = is_prime.get(index - 2) {
            let max_k: usize = (max_val - index * index - 1) / index;
            (0..=max_k).for_each(|k: usize| is_prime[index * index + k * index - 2] = false);
        }
    });

    is_prime
}

fn primes_up_to(max_value: u64) -> Vec<usize> {
    sieve_of_eratosthenes(max_value)
        .iter()
        .enumerate()
        .filter_map(|(index, is_prime)| if *is_prime { Some(index + 2) } else { None })
        .collect()
}
