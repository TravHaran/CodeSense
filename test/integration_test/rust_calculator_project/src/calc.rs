use itertools::Itertools;
use std::ops::{Div, Sub};

pub struct Calc;

impl Calc {
    pub fn add(arr: Vec<f64>) -> f64 {
        arr.iter().sum::<f64>()
    }

    pub fn sub(arr: Vec<f64>) -> f64 {
        arr.iter().map(|&x| x as f64).fold1(Sub::sub).unwrap_or(0.0)
    }

    pub fn mul(arr: Vec<f64>) -> f64 {
        arr.iter().product()
    }

    pub fn div(arr: Vec<f64>) -> f64 {
        arr.iter().map(|&x| x as f64).fold1(Div::div).unwrap_or(0.0)
    }
}

#[test]
fn test_all_operations() {
    // addition
    assert_eq!(Calc::add([2.0, 4.0, 6.0].to_vec()), 12.0);
    assert_eq!(Calc::add([-6.0, 5.0, 10.0].to_vec()), 9.0);

    // subtraction
    assert_eq!(Calc::sub([10.0, 4.0, 6.0].to_vec()), 0.0);
    assert_eq!(Calc::sub([100.0, 10.0, 19.0].to_vec()), 71.0);

    // multiplication
    assert_eq!(Calc::mul([10.0, 10.0, 2.0].to_vec()), 200.0);
    assert_eq!(Calc::mul([-3.0, 2.0].to_vec()), -6.0);

    // division
    assert_eq!(Calc::div([54.0, 2.0, 3.0].to_vec()), 9.0);
    assert_eq!(Calc::div([4.0, 2.0, 5.0].to_vec()), 0.4);
}
