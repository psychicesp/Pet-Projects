import multiprocessing
from random import randint as rand
import platform
import time
import pandas as pd
import os
import pickle

# Configuration
TOTAL_RUNS = 10_000_000
FILE_NAME = 'death_saves_log.csv'

def d6(): return rand(1, 6)
def d20(): return rand(1, 20)

def simulate_chunk(char_type, iterations):
    """Worker function for individual cores."""
    survived = 0
    bounced = 0
    for _ in range(iterations):
        saves, fails = 0, 0
        while True:
            roll_20 = d20()
            # Logic for Monk
            if char_type == 'monk':
                if roll_20 == 20: 
                    survived += 1; bounced += 1; break
                elif roll_20 == 1: fails += 2
                elif (roll_20 + 6) > 9: saves += 1
                else: fails += 1
            # Logic for Brute
            elif char_type == 'brute':
                roll_6 = d6()
                if (roll_20 + roll_6) >= 20:
                    survived += 1; bounced += 1; break
                elif roll_20 == 1: fails += 2
                elif (roll_20 + roll_6) > 9: saves += 1
                else: fails += 1
            # Logic for Feller
            elif char_type == 'feller':
                if roll_20 == 20:
                    survived += 1; bounced += 1; break
                elif roll_20 == 1: fails += 2
                elif roll_20 > 9: saves += 1
                else: fails += 1

            if saves >= 3: survived += 1; break
            elif fails >= 3: break
    return (survived, bounced)

def run_simulation(num):
    cpu_cores = multiprocessing.cpu_count() -2
    chunk_size = num // cpu_cores
    tasks = []
    for char in ['monk', 'brute', 'feller']:
        for _ in range(cpu_cores):
            tasks.append((char, chunk_size))

    print(f"Starting simulation: {num:,} runs per class across {cpu_cores} cores.")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        results = pool.starmap(simulate_chunk, tasks)

    run_time = time.time() - start_time
    
    # Process the results into a flat dictionary
    stats = {'monk': [0,0], 'brute': [0,0], 'feller': [0,0]}
    for i, res in enumerate(results):
        char_name = ['monk', 'brute', 'feller'][i // cpu_cores]
        stats[char_name][0] += res[0] # Survived
        stats[char_name][1] += res[1] # Bounced

    # Prepare Data for CSV
    df_output = {
        'date_run': [time.ctime(start_time)],
        'Monk_Survived': [stats['monk'][0]],
        'Monk_Bounced': [stats['monk'][1]],
        'Feller_Survived': [stats['feller'][0]],
        'Feller_Bounced': [stats['feller'][1]],
        'Brute_Survived': [stats['brute'][0]],
        'Brute_Bounced': [stats['brute'][1]],
        'simulator_type': ["AI All Core -2"],
        'run_time_seconds': [round(run_time, 8)],
        'computer_name': [platform.node()],
        'processor': [platform.processor()],
        'score': [round((num / run_time) / 10000, 8)],
        'operating_system': [f"{platform.system()} {platform.release()}"],
        'Number_of_Runs': [num]
    }

    # Handle CSV Reading/Appending
    if os.path.exists(FILE_NAME):
        df_existing = pd.read_csv(FILE_NAME)
        next_id = df_existing['run_id'].max() + 1 if not df_existing.empty else 1
    else:
        df_existing = pd.DataFrame()
        next_id = 1

    df_new = pd.DataFrame(df_output)
    df_new['run_id'] = next_id
    
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_csv(FILE_NAME, index=False)

    print(f"Results logged to {FILE_NAME}. Total runtime: {round(run_time, 2)}s")

if __name__ == '__main__':
    # Running 5 iterations as requested in your original script
    for i in range(5):
        run_simulation(TOTAL_RUNS)