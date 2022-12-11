extern crate rayon;
extern crate rand;
extern crate csv;

use rand::Rng;
use rayon::prelude::*;
use std::env;
use std::fs::File;

fn d6() -> u32 {
    rand::thread_rng().gen_range(1, 7)
}

fn d20() -> u32 {
    rand::thread_rng().gen_range(1, 21)
}

fn death_save_comparison(n: u32) -> (u32, u32, u32, u32, u32, u32, u32, u32) {
    let (monk, brute, regular) = (0, 0, 0);
    let (monk_bounced, brute_bounced, regular_bounced) = (0, 0, 0);

    (0..n).into_par_iter().for_each(|_| {
        // Monk death saving throws
        let (mut saves, mut fails) = (0, 0);
        let mut in_progress = true;
        while in_progress {
            let roll20 = d20();
            if roll20 == 20 {
                monk += 1;
                monk_bounced += 1;
                in_progress = false;
            } else if roll20 == 1 {
                fails += 2;
            } else if (roll20 + 6) > 9 {
                saves += 1;
            } else {
                fails += 1;
            }
            if saves >= 3 {
                monk += 1;
                in_progress = false;
            } else if fails >= 3 {
                in_progress = false;
            }
        }

        // Brute death saving throws
        let (mut saves, mut fails) = (0, 0);
        let mut in_progress = true;
        while in_progress {
            let roll20 = d20();
            let roll6 = d6();
            if roll20 + roll6 >= 20 {
                brute += 1;
                brute_bounced += 1;
                in_progress = false;
            } else if roll20 == 1 {
                fails += 2;
            } else if (roll20 + roll6) > 9 {
                saves += 1;
            } else {
                fails += 1;
            }
            if saves >= 3 {
                brute += 1;
                in_progress = false;
            } else if fails >= 3 {
                in_progress = false;
            }
        }

        // Regular death saving throws
        let (mut saves, mut fails) = (0, 0);
        let mut in_progress = true;
        while in_progress {
            let roll20 = d20();
            if roll20 == 20 {
                regular += 1;
                regular_bounced += 1;
                in_progress = false;
            } else if roll20 == 1 {
                fails += 2;
            } else if roll20 > 9 {
                saves += 1;
            } else {
                fails += 1;
            }
            if saves >= 3 {
                regular += 1;
                in_progress = false;
            } else if fails >= 3 {
                in_progress = false;
            }
            }
            });
            (monk, monk_bounced, brute, brute_bounced, regular, regular_bounced)
        }

        fn main() {
        let args: Vec<String> = env::args().collect();
        if args.len() != 2 {
        eprintln!("Usage: death_save_simulator <num_times>");
        std::process::exit(1);
        }
        let num_times = args[1].parse::<u32>().unwrap();

let (monk, monk_bounced, brute, brute_bounced, regular, regular_bounced) = death_save_comparison(num_times);

let file_name = "death_saves_log.csv";
let mut writer = csv::Writer::from_path(file_name).unwrap();
writer.write_record(&["operating_system", "simulator_type", "computer_name", "processor", "number_of_runs", "run_time_seconds", "monk_survived", "monk_bounced", "feller_survived", "feller_bounced", "brute_survived", "brute_bounced", "date_run", "score"]).unwrap();
writer.write_record(&[
    &format!("{} {} version {}", platform::system(), platform::release(), platform::version()),
    "Single Thread",
    &platform::node(),
    &platform::processor(),
    &num_times,
    "TODO: calculate run time",
    &monk,
    &monk_bounced,
    &regular,
    &regular_bounced,
    &brute,
    &brute_bounced,
    "TODO: add date and time",
    "TODO: calculate score",
]).unwrap();
}