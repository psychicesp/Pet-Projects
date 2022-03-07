#%%
# from matplotlib import pyplot as plt
import numpy as np
from statistics import mode
import os

punctuation = ['.', '!', '?']

# Infers original formatting rules given a novel as a list of lines
def analyze_novel(novel):
    line_lengths = np.array([len(line) for line in novel])
    # Trimming off outliers will make for a more consistent result.
        # Many lines have a length of 1, I don't want these large counts competing for mode
    lower_limit = 10
    line_lengths = line_lengths[line_lengths > lower_limit]
    upper_limit = mode(line_lengths)*1.2
    line_lengths = line_lengths[line_lengths < upper_limit]
    # line_lengths = [x for x in line_lengths if x < upper_outlier and x > lower_outlier]
    upper_quantile = np.quantile(line_lengths, 0.78)
    # print(upper_quantile)
    # plt.hist(line_lengths, bins = 50)
    # plt.show()
    return upper_quantile

# Determine if a line is over
def is_end(last_line, this_line, line_limit):
    trimmed_line = last_line.strip('"').strip("'")
    last_char = trimmed_line.split(' ')[-1]
    long_line = ' '.join(last_line.split(' ')+[this_line.split(' ')[0]])
    if last_char in punctuation and long_line < line_limit:
        return True
    else:
        return False

# Get a list of lines given file path
def novel_get(txt_file):
    with open(txt_file, 'r', encoding = 'utf-8') as book:
        novel = book.readlines()
    return novel

# Break down lines into chapter object
def chapter_get(novel):
    pass

# Break down the 'text' part of a chapter object into a list of paragraphs, rather than a list of lines
def paragraph_get(novel):
    line_limit = analyze_novel(novel)
    p_list = []
    p = novel[0]
    for n, line in enumerate(novel):
        if is_end(novel[n-1], line, line_limit):
            p_list.append(p)
            p= '\n'
        else:
            p = p+line
        p_list.append(p)
    return p_list
# Re-pack list of paragraphs into a list of lines, using the given max line length
def line_get(paragraph, line_length = 150):
    pass

# Parses a text file into a list of chapter objects, chapter text broken down into paragraphs
def parse_novel(txt_file):
    pass

# Parses a text file and outputs a new text file with adjusted max line-length
def reindent_novel(txt_file, line_length = 150):
    novel = novel_get(txt_file)


paragraphs = paragraph_get(novel_get('txts/[4]Harry Potter and the Goblet of Fire.txt'))

# %%
