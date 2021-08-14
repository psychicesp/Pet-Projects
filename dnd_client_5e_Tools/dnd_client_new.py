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
import json

# %%
# url = "https://5e.tools/items.html#abacus_phb"

# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)
# browser.visit(url)
# time.sleep(5)
# dnd_soup = BS(browser.html, 'html.parser')

# dnd_table = dnd_soup.find_all("a", {"class":"lst--border lst__row-inner"})
# hrefs = [x['href'] for x in dnd_table]
# print(type(hrefs[0]))
# #%%
# url = "https://5e.tools/items.html"
# c = 0
# for href in hrefs[365:]:
#     c += 1
#     name = href.split("#")[1].split("_")[0].replace('%20','_').replace('*','x')
#     new_url = url+href
#     print(name)
#     browser.visit(new_url)
#     if c < 2:    
#         time.sleep(5)
#     else:
#         time.sleep(2)
#     dnd_soup = BS(browser.html, 'html.parser')
#     dnd_soup = dnd_soup.find("table", {"class": "stats"})
#     with open(f"html_pages/items/{name}.html", "w") as temp:
#         pprint(dnd_soup.encode('utf8'), stream = temp)
#     print("     ", "finished")
# browser.quit()
#%%
def monster_unpacker(file):
    monster_json={}
#%%

with open('html_pages/monsters/lich.html', 'r') as mon:
    mon_soup = BS(mon, 'html.parser')

ability_soup = mon_soup.find_all('span', {'class':'roller render-roller'})
meal = {'tags':[]}
for ability in ability_soup:
    pre_json = (ability['data-packed-dice'].replace('\\','')+"\"").strip('\'{').split(',')
    bite = {}
    for element in pre_json:
        try:
            element = element.split(':')
            bite[element[0].strip('"')] = element[1].strip('"').lower()
        except:
            pass
    try:
        meal[bite['name']] = bite['displayText']
    except:
        pass
meal['name'] = mon_soup.find('h1').text
book_page = mon_soup.find('div',{"class":"stats-source flex-v-baseline"}).find_all('a')

print(book_page[0].attrs['title'])
meal['page'] = int(book_page[1].attrs['title'].split(" ")[1])
meal['book'] = book_page[0].attrs['title']
sta = mon_soup.find('div',{"class":"mon__wrp-size-type-align--token"}).text
sta = sta.split(',')
meal['alignment'] = ''.join([x.upper()[:1] for x in sta[1].split(' ')])
sta = sta[0].split(' ')
meal['size'] = sta[0]
meal['type'] = sta[1]
if len(sta)>2:
    meal['tags'].append(sta[2].strip().strip(')').strip('('))
# meal['hit_dice_type'] = 'd'+meal['hit'].split('d')[1]
# meal['num_hit_dice'] = int(meal['hit'].split('d')[0])
# meal.pop('hit')
meal['AC'] =  mon_soup.find('div',{"class":"mon__wrp-avoid-token"}).text
for word in meal['AC'].split(' '):
    if word.isnumeric():
        meal['AC'] = int(word)
        break
speed = [x.text for x in mon_soup.find_all('td', {'colspan':"6"}) if "Speed" in x.text][0].replace('Speed', '')
speed = [x.strip().strip('.').strip() for x in speed.split(',')]
meal['speed'] = speed
meal['saving_throws'] = {}
meal['skills'] = {}
proficiency_dict = {
    "1": "proficiency",
    "2": "expertise"
}
soup_dict = {}
piece_meal = mon_soup.find_all("td", {"colspan":"6"})+ mon_soup.find_all("td", {"colspan":"3"})
sections = ["Saving Throws", "Skills", "Damage Resistances", "Damage Immunities","Condition Immunities", "Senses", "Languages", "Challenge", ""]
for piece in piece_meal:
    for section in sections:
        if section in piece.text:
            soup_dict[section] = piece
            sections.remove(section)
            print(section)
            print(' ', piece.text)
            break
if "Saving Throws" in soup_dict.keys():
    
# %%
def html_cleaner(in_folder):
    files = os.listdir(in_folder)
    for file in files:
        with open(f"{in_folder}/{file}", 'r') as dirty:
            clean = str(dirty.read()).replace("' b'", '').replace("\" b'", '').replace("' b\"", '').replace("'\nb'", '').replace("""'
b'""", '').replace("""'
 b'""", '').replace("""\"
b'""", '').replace("""'
 b\"""", '').replace("""\"
 b'""", '').replace("""'
b\"""", '').replace('''"
b"''', '').replace('''" 
b"''', '').replace('''"
b "''', '').replace('''"
 b"''', '').replace("(b'", "")
        with open(f"{in_folder}/{file}", 'w') as new:
            new.write(clean)

# %%
