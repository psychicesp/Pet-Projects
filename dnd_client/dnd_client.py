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
    'speed':{},
    'hit_dice_type':{},
    'hit_dice':{}

}
for file in files:
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
        print(score[6])
        if '(' in score[2]:
            ac = score[2].split('(')[0].replace(' ','')
            ac_source = score[2].split('(')[1].replace(')','').strip(' ')
            if 'mage armor' in ac_source and ac_source.split(' ')[0].strip(' ').isnumeric():
                ac = int(ac_source.split(' ')[0].strip(' '))
                ac_source = "mage armor"
        else:
            ac = score[2].replace(' ','')
            try:
                ac = int(ac)
            except:
                ac = pd.NA
            ac_source = pd.NA
        hit_dice = score[4].split('(')[1].split('d')[0]
        hit_dice_type = score[4].split('(')[1].split('d')[1].split(' ')[0]
        hit_dice_type = 'd'+ hit_dice_type.strip('(').strip(')')
        speed = score[6].replace('div','').replace('.','')
        print(f"""    ac = {ac}
    ac_source = {ac_source}
    hit_dice = {hit_dice}
    hit_dice_type = {hit_dice_type}
    speed = {speed}""")
    except:
        score = 'error'
        ac = pd.NA
        ac_source = pd.NA
        hit_dice = pd.NA
        hit_dice_type = pd.NA
        speed = pd.NA
        print(f"Could not parse {creature}")
    attrs['ac'][creature] = ac
    attrs['ac_source'][creature] = ac_source
    attrs['speed'][creature] = speed
    attrs['hit_dice'][creature] = hit_dice
    attrs['hit_dice_type'][creature] = hit_dice_type
#%%
df = pd.read_csv('monsters.csv')

def armorer(x):
    if x.Name in attrs['ac'].keys():
        return attrs['ac'][x.Name]
    else:
        return pd.NA
def armoring(x):
    if x.Name in attrs['ac_source'].keys():
        return attrs['ac_source'][x.Name]
    else:
        return pd.NA
def speeder(x):
    if x.Name in attrs['speed'].keys():
        return attrs['speed'][x.Name]
    else:
        return pd.NA
def hitter(x):
    if x.Name in attrs['hit_dice'].keys():
        return attrs['hit_dice'][x.Name]
    else:
        return pd.NA
def hitting(x):
    if x.Name in attrs['hit_dice_type'].keys():
        return attrs['hit_dice_type'][x.Name]
    else:
        return pd.NA

df['AC'] = df.apply(armorer, axis = 1)
df['Armor'] = df.apply(armoring, axis = 1)
df['HitDice#'] = df.apply(hitter, axis = 1)
df['HitDice'] = df.apply(hitting, axis = 1)
df['Speed'] = df.apply(speeder, axis = 1)
# %%

