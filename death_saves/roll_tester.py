#%%
import numpy as np
from numpy.random import randint as rand
from matplotlib import pyplot as plt
import inflect

inflect = inflect.engine().number_to_words

def d20(size):
    return rand(1,20, size = size)

def advantage(size):
    a1 = d20(size)
    a2 = d20(size)
    return np.maximum(a1,a2)


def disadvantage(size):
    a1 = d20(size)
    a2 = d20(size)
    return np.minimum(a1,a2)

bins = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

for x in range(10):
    arr = d20(10**x)
    plt.hist(arr, bins = bins)
    plt.xticks(bins, bins)
    plt.title(inflect(10**x))
    plt.show()
# %%
