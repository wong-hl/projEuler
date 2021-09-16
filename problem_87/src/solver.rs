// use num::Integer;
use num::integer::Roots;

#[derive(Debug)]
struct PrimeBaseLimits<T>
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
    fn new(upper_limit: T) -> Self {
        let square = upper_limit.nth_root(2);
        let cube = upper_limit.nth_root(3);
        let fourth = upper_limit.nth_root(4);
        Self {
            square,
            cube,
            fourth,
        }
    }
}
