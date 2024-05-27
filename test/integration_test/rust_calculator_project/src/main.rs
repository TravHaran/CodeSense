mod calc;
use calc::Calc;
use std::io;

fn main() {
    println!("Welcome to the a basic calculator built with Rust.");

    loop {
        println!("Please enter an equation or \"q\" to quit: ");

        let mut input = String::new();
        io::stdin()
            .read_line(&mut input)
            .expect("Failed to read input");

        if input.trim() == "q" {
            println!("Thanks for using this program.");
            break;
        }

        let valid_operators = vec!["+", "-", "*", "/"];

        for operator in valid_operators {
            match input.find(operator) {
                Some(_) => {
                    let parts: Vec<&str> = input.split(operator).collect();

                    if parts.len() < 2 {
                        panic!("Invalid equation.");
                    }

                    let mut number_array = vec![];
                    let mut counter = 0;

                    while counter != parts.len() {
                        let val: f64 = parts[counter].trim().parse().ok().expect("Enter a number.");
                        number_array.push(val);
                        counter += 1;
                    }

                    match operator {
                        "+" => println!("{}", Calc::add(number_array)),
                        "-" => println!("{}", Calc::sub(number_array)),
                        "*" => println!("{}", Calc::mul(number_array)),
                        "/" => println!("{}", Calc::div(number_array)),
                        _ => println!("Only addition, subtraction, multiplication and division are supported.")
                    }
                }

                None => {
                    continue;
                }
            }
        }
    }
}
