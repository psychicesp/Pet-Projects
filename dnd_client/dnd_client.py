#%%
from splinter import Browser
from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
from pprint import pprint

# url = 'https://www.aidedd.org/dnd-filters/monsters.php'
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)
# browser.visit(url)
# dnd_soup = BS(browser.html, 'html.parser')
# browser.quit()
# dnd_soup = dnd_soup.find_all("tbody")[0]
# name_links = {}
# for bit in dnd_soup.find_all("a",href=True):
#     name_links[bit.text] = bit['href']

# pprint(name_links)
# %%
def url_finder(x):
    x=x.lower().split(' ')
    if len(x)>1:
        x = '-'.join(x)
    else:
        x=x[0]
    return f"https://www.aidedd.org/dnd/monstres.php?vo={x}"
df = pd.read_csv('monsters.csv')

df['URL']=df['Name'].apply(url_finder)

# %%
