
from random import randint as rand
# making dice rolls more concise
def d6():
    roll = rand(1,6)
    return roll
def d20():
    roll = rand(1,20)
    return roll
def deathSaveComparisson (n):
# These are counters, the lowercase represents passing the series of death saves and the capital represents bouncing back with 1HP
    monk = 0
    Monk = 0
    brute = 0
    Brute = 0
    regular = 0
    Regular = 0
# The following are the Monks death saving throws.  It bounces back when rolling a 20 and adds proficiency to the total 
# but the proficiency does not count towards a "Nat 20"
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
#The following are the Brutes death saving throws.  THey roll a d6 to go with the d20, if they and up to 20 it counts as a Nat 20
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
#The following will print the results as a percentage of times rolled
    print("Each unit was brought to 0 HP #" + str(n) + " times")
    print("The Monk survived " + str(100*(monk/n)) + "% of the time and bounced right back " + str(100*(Monk/n)) + "% of the time.")
    print("The Brute survived " + str(100*(brute/n)) + "% of the time and bounced right back " + str(100*(Brute/n)) + "% of the time.")
    print("The regular feller survived " + str(100*(regular/n)) + "% of the time and would bounce back " + str(100*(Regular/n)) + "% of the time.")

no_times = int(input("How many iterations should we simulate?"))

deathSaveComparisson(no_times)
        

            


