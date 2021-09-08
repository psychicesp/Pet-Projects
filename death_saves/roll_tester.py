#%%
import numpy as np
from numpy.random import randint as rand
from matplotlib import pyplot as plt
import pandas as pd
from numba import njit
from timeit import timeit
import inflect

inflect = inflect.engine().number_to_words

setup = """
import numpy as np
from numpy.random import randint as rand
from matplotlib import pyplot as plt
import pandas as pd
from numba import njit
from timeit import timeit
import inflect

@njit
def njit_d20(size):
    return rand(1,20, size = size)


def d20(size):
    return rand(1,20, size = size)
"""

@njit
def d20(size):
    return rand(1,21, size = size)

@njit
def advantage(size):
    a1 = d20(size)
    a2 = d20(size)
    return np.maximum(a1,a2)

@njit
def disadvantage(size):
    a1 = d20(size)
    a2 = d20(size)
    return np.minimum(a1,a2)

bins = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#%%
for x in range(10):
    arr = d20(10**x)
    plt.hist(arr, bins = 20)
    plt.xticks(bins, bins)
    plt.title(inflect(10**x))
    plt.show()
# %%
df = pd.DataFrame()

df['target_roll'] = list(range(1,21))
df['van_success_%'] = (21 - df['target_roll']) * 5
df['adv_success_%'] = (((df['van_success_%']/100)*2)-((df['van_success_%']/100)**2))*100
df['dis_success_%'] = ((df['van_success_%']/100)**2)*100

num_times = round(10**9)

arr = d20(num_times)

def arr_trimmer(x):
    return round(((arr[arr>=x]).size/arr.size)*100, 2)

df['emperical_van_%'] = df['target_roll'].apply(arr_trimmer)

arr = advantage(num_times)
df['emperical_adv_%'] = df['target_roll'].apply(arr_trimmer)

arr = disadvantage(num_times)
df['emperical_dis_%'] = df['target_roll'].apply(arr_trimmer)

arr = 0
df
# %%
