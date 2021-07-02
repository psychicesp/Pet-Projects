#%%
import pandas as pd

mon = pd.read_csv('monsters.csv')
mon.to_csv('monsters.csv')

def challenge_cleaner(x):
    if '/' in x:
        x = 1/int(x.split('/')[1])
    else:
        x = float(x)
    return x

mon['Challenge'] = mon['Challenge'].apply(challenge_cleaner)
# %%
