
#%%
import multiprocessing
from random import randint as rand
import platform
import time
import pandas as pd
#%%
simulator_type= "Multiprocessing"
computer_name = platform.node()
processor = platform.processor()
if platform.system() == 'Linux':
    distribution = platform.linux_distribution()
    operating_system = f"{platform.system} {platform.release}({distribution}) version #{platform.version}"
else:
    operating_system = f"{platform.system} {platform.release} version #{platform.version}"
# making dice rolls more concise, will need six-sided and 20 sided dice
def d6():
    roll = rand(1,6)
    return roll
def d20():
    roll = rand(1,20)
    return roll
# These dictionaries hold stats for each unit.  Code was refactored this way 
# because I cannot reuse variable names when using multiprocessing and 
# I prefered it to making a dozen unique variables

monk= {
    'saves':0,
    'fails':0,
    'd20':0,
    'in_progress':True,
    'survive': 0,
    'bounce': 0
}
brute= {
    'saves':0,
    'fails':0,
    'd20':0,
    'd6'
    'in_progress':True,
    'survive': 0,
    'bounce': 0
}
feller= {
    'saves':0,
    'fails':0,
    'd20':0,
    'in_progress':True,
    'survive': 0,
    'bounce': 0
}
# The following are the Monks death saving throws.  It bounces back when rolling a 20 and adds proficiency to the total 
# but the proficiency does not count towards a "Nat 20"
def monk_throws(n):
    for i in range(n):
        monk['in_progress'] = True
        monk['saves'] = 0
        monk['fails'] = 0
        while monk['in_progress'] == True:
            monk['d20'] = d20()
            if monk['d20'] == 20:
                monk['survive'] += 1
                monk['bounce'] += 1
                monk['in_progress'] = False
                break
            elif monk['d20'] == 1:
                monk['fails'] += 2
            elif (monk['d20'] + 6) > 9:
                monk['saves'] += 1
            else:
                monk['fails'] += 1
            if monk['saves'] >= 3:
                monk['survive'] += 1
                monk['in_progress'] = False
                break
            elif monk['fails'] >= 3:
                monk['in_progress'] = False
                break
    print("The 18th+ level Monk survived " + str(round(100*(monk['survive']/n),2)) + "% of the time and bounced right back " + str(round(100*(monk['bounce']/n),2)) + "% of the time.")
#The following are the Brutes death saving throws.  They roll a d6 to go with the d20, if they and up to 20 it counts as a Nat 20
def brute_throws(n):
    for i in range(n):
        brute['saves'] = 0
        brute['fails'] = 0
        brute['in_progress'] = True
        while brute['in_progress'] == True:
            brute['d20'] = d20()
            brute['d6'] = d6()
            if brute['d20'] + brute['d6'] >= 20:
                brute['survive'] += 1
                brute['bounce'] += 1
                brute['in_progress'] = False
                break
            elif brute['d20'] == 1:
                brute['fails'] += 2
            elif (brute['d20'] + brute['d6']) > 9:
                brute['saves'] += 1
            else:
                brute['fails'] += 1
            if brute['saves'] >= 3:
                brute['survive'] += 1
                brute['in_progress'] = False
                break
            elif brute['fails'] >= 3:
                brute['in_progress'] = False
                break
    print("The 6th+ level Brute survived " + str(round(100*(brute['survive']/n),2)) + "% of the time and bounced right back " + str(round(100*(brute['bounce']/n),2)) + "% of the time.")
#The following are the fellers series of death saving throws
def feller_throws(n):
    for i in range(n):
        feller['saves'] = 0
        feller['fails'] = 0
        feller['in_progress'] = True
        while feller['in_progress'] == True:
            feller['d20'] = d20()
            if feller['d20'] == 20:
                feller['survive'] += 1
                feller['bounce'] += 1
                feller['in_progress'] = False
                break
            elif feller['d20'] == 1:
                feller['fails'] += 2
            elif feller['d20'] > 9:
                feller['saves'] += 1
            else:
                feller['fails'] += 1
            if feller['saves'] >= 3:
                feller['survive'] += 1
                feller['in_progress'] = False
                break
            elif feller['fails'] >= 3:
                feller['in_progress'] = False
                break
    print("The regular feller survived " + str(round(100*(feller['survive']/n),2)) + "% of the time and would bounce back " + str(round(100*(feller['bounce']/n),2)) + "% of the time.")
def thing():
    print('yup')
def throw_saves(num):
    if __name__ == '__main__':
        p1 = multiprocessing.Process(target = monk_throws, args=(num,))
        p2 = multiprocessing.Process(target = brute_throws, args=(num,))
        p3 = multiprocessing.Process(target = feller_throws, args=(num,))

        start_time = time.time() 
        p1.start()
        p2.start()
        p3.start()
        print("Each unit will be brought to 0 HP " + str(num) + " times")

        p1.join()
        p2.join()
        p3.join()
        run_time = time.time()-start_time
        print(f'The program ran in {round(run_time, 2)} seconds')
    
throw_saves(10000000)


        

            




# %%
