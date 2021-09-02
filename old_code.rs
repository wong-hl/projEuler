use std::ops::{Add, Div, Mul};

extern crate num;
use num::cast::ToPrimitive;
use num::PrimInt;

fn sum_first_n_natural_numbers<T>(n: T) -> T
where
    T: Add<Output = T> + Mul<Output = T> + Div<Output = T> + PrimInt,
{
    let two = num::cast(2).unwrap();
    n * (n + T::one()) / two
}

fn number_of_summations<T>(n: T) -> T
where
    T: Mul<Output = T> + Div<Output = T> + PrimInt + std::fmt::Debug,
{
    if n == num::cast(2).unwrap() {
        return T::one();
    }

    let is_even: bool = n & num::one() == num::zero();
    let two: T = num::cast(2).unwrap();
    let half_n = n / two;

    //     println!("{} {:?}", is_even, half_n);

    if is_even {
        two * sum_first_n_natural_numbers(half_n) - half_n
    } else {
        two * sum_first_n_natural_numbers(half_n)
    }
}
