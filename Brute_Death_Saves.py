
#%%
from random import randint as rand
import platform
import time
import pandas as pd
# making dice rolls more concise, will need six-sided and 20 sided dice
def d6():
    roll = rand(1,6)
    return roll
def d20():
    roll = rand(1,20)
    return roll
def deathSaveComparisson (n):
    start_time = time.time() 
# These are counters representing both possible positive outcomes from a series of Death Saving Throws. 
# The lowercase represents passing the series of death saves and the capital represents bouncing back with 1HP
    monk = 0
    Monk = 0
    brute = 0
    Brute = 0
    regular = 0
    Regular = 0
# The following are the Monks death saving throws.  It bounces back when rolling a 20 and adds proficiency to the total 
# but the proficiency does not count towards a "Nat 20
    for i in range(n):
        saves = 0
        fails = 0
        in_progress = True
        while in_progress == True:
            roll20 = d20()
            if roll20 == 20:
                monk += 1
                Monk += 1
                in_progress = False
                break
            elif roll20 == 1:
                fails += 2
            elif (roll20 + 6) > 9:
                saves += 1
            else:
                fails += 1
            if saves >= 3:
                monk += 1
                in_progress = False
                break
            elif fails >= 3:
                in_progress = False
                break
#The following are the Brutes death saving throws.  They roll a d6 to go with the d20, if they and up to 20 it counts as a Nat 20
    for i in range(n):
        saves = 0
        fails = 0
        in_progress = True
        while in_progress == True:
            roll20 = d20()
            roll6 = d6()
            if roll20 + roll6 >= 20:
                brute += 1
                Brute += 1
                in_progress = False
                break
            elif roll20 == 1:
                fails += 2
            elif (roll20 + roll6) > 9:
                saves += 1
            else:
                fails += 1
            if saves >= 3:
                brute += 1
                in_progress = False
                break
            elif fails >= 3:
                in_progress = False
                break
#The following are the regular series of death saving throws
    for i in range(n):
        saves = 0
        fails = 0
        in_progress = True
        while in_progress == True:
            roll20 = d20()
            if roll20 == 20:
                regular += 1
                Regular += 1
                in_progress = False
                break
            elif roll20 == 1:
                fails += 2
            elif roll20 > 9:
                saves += 1
            else:
                fails += 1
            if saves >= 3:
                regular += 1
                in_progress = False
                break
            elif fails >= 3:
                in_progress = False
                break
    run_time = time.time()-start_time
    print(f'The program ran in {round(run_time, 2)} seconds')
#The following will print the results as a percentage of times rolled
    print("Each unit was brought to 0 HP " + str(n) + " times")
    print("The 18th+ level Monk survived " + str(round(100*(monk/n),2)) + "% of the time and bounced right back " + str(round(100*(Monk/n),2)) + "% of the time.")
    print("The regular feller survived " + str(round(100*(regular/n),2)) + "% of the time and would bounce back " + str(round(100*(Regular/n),2)) + "% of the time.")
        print("The 6th+ level Brute survived " + str(round(100*(brute/n),2)) + "% of the time and bounced right back " + str(round(100*(Brute/n),2)) + "% of the time.")

num_times = int(input("How many iterations should we simulate?"))

deathSaveComparisson(num_times)


            




# %%
