// use num::Integer;
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
