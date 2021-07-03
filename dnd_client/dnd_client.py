#%%
from splinter import Browser
from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
import time
from pprint import pprint
import random
import shutil
import os
folder = 'html_pages/Monsters'
files = os.listdir(folder)
#%%
url = 'https://www.aidedd.org/dnd-filters/spells.php'
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)
# browser.visit(url)
# dnd_soup = BS(browser.html, 'html.parser')
# browser.quit()
# dnd_soup = dnd_soup.find_all("tbody")[0]
# name_links = {}
# for bit in dnd_soup.find_all("a",href=True):
#     name_links[bit.text] = bit['href']

# df = pd.read_html(browser.html)
# browser.quit()
# df['URL']=df['Name'].apply(url_finder)

# df = pd.read_csv('spells.csv')
# def html_writer(x, url):
#     nameo=x.lower().replace("'",'-').replace(' ','-')
#     url = f"https://www.aidedd.org/dnd/sorts.php?vo={nameo}"
#     nameo=x.replace('/', ' OR ')
#     print(f"Getting {x}")
#     file_name = f"html_pages/spells/{nameo}.html"
#     response = req.get(url)

#     with open(file_name, 'w', encoding='utf-8') as stuff:
#         stuff.write(response.text)

# names = df['Name'].to_list()
# for name in names:
#     html_writer(name)

# %%
for file in files:
    print(f'Working on {file}')
    location = f"{folder}/{file}"
    file_name = f"html_pages/French/monsters/{file}"
    try:
        with open(location, 'r') as thingy:
            stuff = thingy.read()
    except:
        with open(location, 'r', encoding='utf-8') as thingy:
            stuff = thingy.read()
    soup = BS(stuff,'html.parser')
    try:
        url = soup.find_all('link', {'rel':'alternate'})[0]['href']
        response = req.get(url)
        print(f"    Writing French {file}")
        try:
            with open(file_name, 'w') as stuff:
                stuff.write(response.text)
        except:
            with open(file_name, 'w', encoding='utf-8') as stuff:
                stuff.write(response.text)
        print(f"         -----{file} Was A Success!!!-----")
    except:
        pass
    rest = random.random() 
    rest = rest * random.randint(2,3)
    rest += 1
    print(f"            Resting for {round(rest,2)} seconds")
    time.sleep(rest)
 

    # %%
