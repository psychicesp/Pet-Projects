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
folder = 'html_pages/monsters'
files = os.listdir(folder)


# url = 'https://www.aidedd.org/dnd-filters/spells.php'



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


# for file in files:
#     print(f'Working on {file}')
#     location = f"{folder}/{file}"
#     file_name = f"html_pages/French/monsters/{file}"
#     try:
#         with open(location, 'r') as thingy:
#             stuff = thingy.read()
#     except:
#         with open(location, 'r', encoding='utf-8') as thingy:
#             stuff = thingy.read()
#     soup = BS(stuff,'html.parser')
#     try:
#         url = soup.find_all('link', {'rel':'alternate'})[0]['href']
#         response = req.get(url)
#         print(f"    Writing French {file}")
#         try:
#             with open(file_name, 'w', encoding='utf-8') as stuff:
#                 stuff.write(response.text)
#         except:
#             with open(file_name, 'w') as stuff:
#                 stuff.write(response.text)
#         print(f"         -----{file} Was A Success!!!-----")
#     except:
#         pass
#     rest = random.random() 
#     rest = rest * random.randint(1,2)
#     rest += 1
#     print(f"            Resting for {round(rest,2)} seconds")
#     time.sleep(rest)
 

    # %%
attrs = {
    'ac':{},
    'ac_source':{},
    'walk_speed':{},
    'fly_speed':{},
    'climb_speed':{},
    'hit_dice_type':{},
    'hit_dice_number':{}

}
for file in files[0:15]:
    location = f"{folder}/{file}"
    creature = file.split('.')[0]
    file_name = f"html_pages/monsters/{file}"
    try:
        with open(location, 'r') as thingy:
            stuff = thingy.read()
    except:
        with open(location, 'r', encoding='utf-8') as thingy:
            stuff = thingy.read()
    soup = BS(stuff,'html.parser')
    print(creature)
    try:
        score = soup.find_all('div', {'class':'red'})[0]
        score = str(score).split('<svg><polyline points=')[0]
        score = score.replace('<br>','').replace('<br/>','').replace('<','').replace('>','').replace('/','')
        score = score.split('strong')
        print(score)
        if '(' in score[2]:
            ac = score[2].split('(')[0].replace(' ','')
            ac_source = score[2].split('(')[1].replace(')','').strip(' ')
        else:
            ac = score[2].replace(' ','')
            try:
                ac = int(ac)
            except:
                ac = pd.NA
            ac_source = pd.NA
        print(ac,'\n' ,ac_source)
    except:
        score = 'error'
        print(f"Could not parse {creature}")
#%%

df = pd.read_csv('monsters.csv')

def strengthener(x):
    if x.Name in attrs['STR'].keys():
        return attrs['STR'][x.Name]
    else:
        return 0
def dexerciser(x):
    if x.Name in attrs['DEX'].keys():
        return attrs['DEX'][x.Name]
    else:
        return 0
def congratulater(x):
    if x.Name in attrs['CON'].keys():
        return attrs['CON'][x.Name]
    else:
        return 0
def teacher(x):
    if x.Name in attrs['INT'].keys():
        return attrs['INT'][x.Name]
    else:
        return 0
def guru(x):
    if x.Name in attrs['WIS'].keys():
        return attrs['WIS'][x.Name]
    else:
        return 0
def coach(x):
    if x.Name in attrs['CHA'].keys():
        return attrs['CHA'][x.Name]
    else:
        return 0

df['Str'] = df.apply(strengthener, axis = 1)
df['Dex'] = df.apply(dexerciser, axis = 1)
df['Con'] = df.apply(congratulater, axis = 1)
df['Int'] = df.apply(teacher, axis = 1)
df['Wis'] = df.apply(guru, axis = 1)
df['Cha'] = df.apply(coach, axis = 1)
# %%

