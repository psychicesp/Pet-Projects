#%%
from splinter import Browser
from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
import time
from pprint import pprint
import random

# url = 'https://www.aidedd.org/dnd-filters/monsters.php'
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)
# browser.quit()
# dnd_soup = dnd_soup.find_all("tbody")[0]
# name_links = {}
# for bit in dnd_soup.find_all("a",href=True):
#     name_links[bit.text] = bit['href']

# pprint(name_links)
# def url_finder(x):
#     x=x.lower().split(' ')
#     if len(x)>1:
#         x = '-'.join(x)
#     else:
#         x=x[0]
#     return f"https://www.aidedd.org/dnd/monstres.php?vo={x}"
df = pd.read_csv('monsters.csv')

# df['URL']=df['Name'].apply(url_finder)

def html_writer(x):
    nameo=x.lower()
    nameo = nameo.split(' ')
    if len(nameo)>1:
        nameo = '-'.join(nameo)
    else:
        nameo=nameo[0]
    url = f"https://www.aidedd.org/dnd/monstres.php?vo={nameo}"
    nameo=x.replace('/', ' OR ')
    print(f"Getting {x}")
    file_name = f"html_pages/{nameo}.html"
    response = req.get(url)
    rest = random.random() 
    rest = rest * random.randint(2,3)
    rest += 1
    print(f"    Resting for {round(rest,2)} seconds")
    time.sleep(rest)
    with open(file_name, 'w', encoding='utf-8') as stuff:
        stuff.write(response.text)
    print(f"Failed to write {x}")

names = df['Name'].to_list()

for name in names:
    html_writer(name)

# %%
