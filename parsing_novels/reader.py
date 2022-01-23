#%%
from matplotlib import pyplot as plt
import numpy as np

def txt_reindent(txt_file, line_length = 150):
    with open(txt_file, 'r') as book:
        novel = book.readlines()
        line_lengths = [len(line) for line in novel]
        print(len(novel))
        print(novel)
        plt.hist(line_lengths, bins = 25)

txt_reindent('txts/[4]Harry Potter and the Goblet of Fire.txt')
# %%
