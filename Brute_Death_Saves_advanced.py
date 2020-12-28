
#%%
import multiprocessing
from random import randint as rand
import platform
import time
import pandas as pd
num_times=10000000
file_name = 'death_saves_log.csv'
#%%

# making dice rolls more concise, will need six-sided and 20-sided dice
def d6():
    roll = rand(1,6)
    return roll
def d20():
    roll = rand(1,20)
    return roll
if "monk" not in globals():
    monk = {
    'saves':0,
    'fails':0,
    'd20':0,
    'in_progress':True,
    'survive': 0,
    'bounce': 0
    }
    brute = {
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
    global monk_s
    global monk_b
    monk_s = monk['survive']
    monk_b = monk['bounce']
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
    global brute_s
    global brute_b
    brute_s = brute['survive']
    brute_b = brute['bounce']
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
    global feller_s
    global feller_b
    feller_s = feller['survive']
    feller_b = feller['bounce']
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
    
throw_saves(num_times)

file_name = 'death_saves_log.csv'
df_output = {}
try:
    df_output['Monk_Survived']= [monk_s]
    df_output['Monk_Bounced']= [monk_b]
    df_output['Feller_Survived']= [feller_s]
    df_output['Feller_Bounced']= [feller_b]
    df_output['Brute_Survived']= [brute_s]
    df_output['Brute_Bounced']= [brute_b]
except:
    pass
df_output['simulator_type']= ["Multi Thread"]
df_output['computer_name'] = [platform.node()]
df_output['processor'] = [platform.processor()]
if 'Linux' in platform.system():
    distribution = platform.linux_distribution()
    df_output['operating_system'] = [f"{platform.system()} {platform.release()}({distribution}) version #{platform.version()}"]
else:
    df_output['operating_system'] = [f"{platform.system()} {platform.release()} version {platform.version()}"]
df_output['Number_of_Runs'] = [num_times]
df = pd.read_csv(file_name)
df_output['run_id'] = df['run_id'].max()+1
new_line = pd.DataFrame(df_output)
df = pd.concat([df, new_line])
try:
    print(monk_s)
    if (num_times >= 100000) and (monk_s>1000):
        df.set_index('run_id').to_csv(file_name)
except:
    pass      

            




# %%
