#%%
from numpy import nan
from splinter import Browser
from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
import time
from pprint import pprint
import random
import shutil
import os

# %%
url = "https://5e.tools/items.html#abacus_phb"

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
time.sleep(5)
dnd_soup = BS(browser.html, 'html.parser')

dnd_table = dnd_soup.find_all("a", {"class":"lst--border lst__row-inner"})
hrefs = [x['href'] for x in dnd_table]
print(type(hrefs[0]))
#%%
url = "https://5e.tools/items.html"
c = 0
for href in hrefs[365:]:
    c += 1
    name = href.split("#")[1].split("_")[0].replace('%20','_').replace('*','x')
    new_url = url+href
    print(name)
    browser.visit(new_url)
    if c < 2:    
        time.sleep(5)
    else:
        time.sleep(2)
    dnd_soup = BS(browser.html, 'html.parser')
    dnd_soup = dnd_soup.find("table", {"class": "stats"})
    with open(f"html_pages/items/{name}.html", "w") as temp:
        pprint(dnd_soup.encode('utf8'), stream = temp)
    print("     ", "finished")
browser.quit()
#%%

#%%
