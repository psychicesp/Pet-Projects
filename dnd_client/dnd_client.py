#%%
from splinter import Browser
from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
import time
from pprint import pprint
import random
#%%
url = 'https://www.aidedd.org/dnd-filters/spells.php'
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
# dnd_soup = BS(browser.html, 'html.parser')
# browser.quit()
# dnd_soup = dnd_soup.find_all("tbody")[0]
# name_links = {}
# for bit in dnd_soup.find_all("a",href=True):
#     name_links[bit.text] = bit['href']

df = pd.read_html(browser.html)
browser.quit()
# df['URL']=df['Name'].apply(url_finder)
# %%
df = pd.read_csv('spells.csv')
def html_writer(x):
    nameo=x.lower().replace("'",'-').replace(' ','-')
    url = f"https://www.aidedd.org/dnd/sorts.php?vo={nameo}"
    nameo=x.replace('/', ' OR ')
    print(f"Getting {x}")
    file_name = f"html_pages/spells/{nameo}.html"
    response = req.get(url)
    rest = random.random() 
    rest = rest * random.randint(2,3)
    rest += 1
    print(f"    Resting for {round(rest,2)} seconds")
    time.sleep(rest)
    with open(file_name, 'w', encoding='utf-8') as stuff:
        stuff.write(response.text)

names = df['Name'].to_list()
for name in names:
    html_writer(name)

# %%
