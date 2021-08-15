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
proficiency_dict = {
    "1": "proficient",
    "2": "expert"
}
file_name = "lich.html"
def html_to_json(file_name, save = True):
    try:
        with open(f'html_pages/monsters/{file_name}', 'r') as mon:
            mon_soup = BS(mon, 'html.parser')
        new_file_name = file_name.split('.')[0]+".json"
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
        soup_dict = {}
        piece_meal = mon_soup.find_all("td", {"colspan":"6"})+ mon_soup.find_all("td", {"colspan":"3"})
        sections = ["Saving Throws", "Skills", "Damage Resistances", "Damage Immunities","Condition Immunities", "Senses", "Languages", "Challenge"]
        for piece in piece_meal:
            for section in sections:
                if section in piece.text:
                    soup_dict[section] = piece
                    sections.remove(section)
                    break
        try:
            saves = soup_dict["Saving Throws"].find_all('span',{'class':'roller render-roller'})
            for save in saves:
                save_type = save['title'].split(" ")[0].lower()
                save_prof = proficiency_dict[save.find('span', {'class':'rd__roller--roll-prof-dice'}).text.replace('+','').split('d')[0]]
                meal['saving_throws'][save_type] = save_prof
        except:
            pass
        try:
            skills = soup_dict["Skills"].find_all('span',{'class':'roller render-roller'})
            for skill in skills:
                skill_type = skill['data-roll-name'].lower()
                skill_prof = proficiency_dict[skill['data-roll-prof-dice'].replace('+','').split('d')[0]]
                meal['skills'][skill_type] = skill_prof
        except:
            pass
        try:
            immunities = soup_dict['Damage Immunities'].text.replace('Damage Immunities ', '').split(';')
            immunities = [x.strip() for x in immunities]
            meal['damage_immunities'] = immunities
        except:
            pass
        try:
            resistances = soup_dict['Damage Resistances'].text.replace('Damage Resistances ', '').split(';')
            resistances = [x.strip() for x in resistances]
            meal['resistances'] = resistances
        except:
            pass
        try:
            immunities = soup_dict['Condition Immunities'].text.replace('Condition Immunities ', '').split(';')
            immunities = [x.strip() for x in immunities]
            meal['condition_immunities'] = immunities
        except:
            pass
        try:
            senses = soup_dict['Senses'].text.replace('Senses', '').split(',')
            senses = [x.strip() for x in senses]
            meal['senses'] = senses
        except:
            pass
        try:
            languages = soup_dict['Languages'].text.replace('Languages', '').split(',')
            languages = [x.strip() for x in languages]
            meal['languages'] = languages
        except:
            pass
        meal['CR'] = soup_dict['Challenge'].text.strip("\\n").split("\\n")[1]
        book_page = mon_soup.find('div',{"class":"stats-source flex-v-baseline"}).find_all('a')
        meal['page'] = int(book_page[1].attrs['title'].split(" ")[1])
        meal['book'] = book_page[0].attrs['title']
        trait_soup = mon_soup.find('tr', {'class', 'trait'})
        try:
            traits = trait_soup.find_all('div', {'class', 'rd__b rd__b--3'})
            meal['traits'] = {}
            for trait in traits:
                trait_name = trait.find("span", {"class":"entry-title-inner help-subtle"}).text
                try:
                    if "Legendary Resistance" in trait:
                        meal['traits']['legendary_resistance'] = int(trait_name.split("/Day")[0].split('(')[-1])
                    elif "Spellcasting" in trait_name:
                        spellcasting_dict = {}
                        if 'innately' in trait.p.text:
                            spellcasting_dict['type']= "innate"
                        else:
                            spellcasting_dict['level']= int(trait.p.text.split('th-level')[0].split(' ')[-1])
                            spellcasting_dict['type'] = trait.p.text.split('the following ')[-1].split(' spells')[0]
                        spellcasting_dict['spells'] = [x.text.replace('\n', '').replace('\\', '') for x in trait.find_all('a', {'data-vet-page':"spells.html"})]
                        meal['traits']['spellcasting'] = spellcasting_dict
                    else:
                        meal['traits'][trait_name.strip('.')] = trait.p.text.replace('\n', '').replace('\\', '')
                except:
                    pass
        except:
            pass
        meal['actions'] = {}
        try:
            action_soup = mon_soup.find('tr', {'class', 'action'})
            actions = action_soup.find_all('td', {'class', 'rd__b rd__b--3'})
            for action in actions:
                action_name = action.find("span", {"class":"entry-title-inner help-subtle"}).text.replace('.','').strip()
                action_text = action.p.text
                meal['actions'][action_name] = action_text
        except:
            pass
        try:
            legendary_soup = mon_soup.find_all('tr', {'class': 'legendary'})
            legendary_dict = {
                'number': 0,
                'options': {}
            }
            legendary_dict['number'] = int(legendary_soup[0].find('td',{'colspan':"6"}).text.split(' legendary actions')[0].split(' ')[-1])
            legendaries = legendary_soup[1].find_all('li', {'class':"rd__li"})
            for legendary in legendaries:
                leg_name = legendary.find('span', {'class': 'bold rd__list-item-name'}).text.replace('\n', '').replace('\\', '')
                leg_text = legendary.p.text.replace('\n', '').replace('\\', '').replace(leg_name, '').strip()
                while '  ' in leg_name:
                    leg_name = leg_name.replace('  ', ' ')
                while '  ' in leg_text:
                    leg_text = leg_text.replace('  ', ' ')
                legendary_dict['options'][leg_name.strip('.')] = leg_text
        except:
            pass
        meal['legendary_actions'] = legendary_dict
        try:
            lair_soup = mon_soup.find('tr', {'class':'lairaction'})
            lair_actions = lair_soup.find_all('li', {'class': "rd__li"})

            meal['in_lair'] = {
                'CR_increase':1,
                'actions':[]
            }

            for action in lair_actions:
                lair_action = action.text.replace('\n', '').replace('\\', '')
                while "  " in lair_action:
                    lair_action = lair_action.replace("  ", " ")
                meal['in_lair']['actions'].append(lair_action)
        except:
            pass
        sta = mon_soup.find('div',{"class":"mon__wrp-size-type-align--token"}).text
        sta = sta.split(',')
        meal['alignment'] = ''.join([x.upper()[:1] for x in sta[1].split(' ')])
        sta = sta[0].split(' ')
        meal['size'] = sta[0]
        meal['type'] = sta[1]
        if len(sta)>2:
            meal['tags'].append(sta[2].strip().strip(')').strip('('))
        if save:
            with open(f'jsons/monsters/{new_file_name}', 'w') as out:
                json.dump(meal, out, indent = 4)
    except:
        if save:
            with open(f'jsons/failed_monsters/{new_file_name}', 'w') as out:
                json.dump(meal, out, indent = 4)

# html_to_json(file_name)
# %%
files = os.listdir("html_pages/monsters")
for file in files:
    html_to_json(file)

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
