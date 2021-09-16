use num::{FromPrimitive, ToPrimitive};

fn seive<T>(n: T) -> Vec<bool>
where
    T: ToPrimitive,
{
    if let Some(max_val) = n.to_usize() {
        // Initialise aray of boolean values from 2 to n (shifted in implementation)
        // i.e. index 0 = 2, index 1 = 3, ... etc
        let mut out = vec![true; max_val - 2];

        // Max iteration number = sqrt(n)
        let n_sqrt: usize = ((max_val as f64).sqrt() + 1.0) as usize;

        // For i = 2, ..., sqrt(n)
        (2..n_sqrt).for_each(|index| {
            // if that index is true
            if let Some(true) = out.get(index - 2) {
                // Iterate over j = i^2, i^2 + i, ..., n
                let max_k: usize = (max_val - index * index - 1) / index;
                (0..=max_k).for_each(|k| out[index * index + k * index - 2] = false);
            }
        });
        out
    } else {
        panic!("Unable to convert to usize")
    }
}

pub fn prime_numbers_upto<T: ToPrimitive + FromPrimitive>(maximum_num: T) -> Vec<T> {
    seive(maximum_num)
        .iter()
        .enumerate()
        .filter_map(|(index, is_prime)| -> Option<T> {
            if *is_prime {
                T::from_usize(index + 2)
            } else {
                None
            }
        })
        .collect()
}
