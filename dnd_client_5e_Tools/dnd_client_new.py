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
def sterilizer(string_text):
    clean_text = string_text.replace('\n', '').replace('\\', '').replace("""\'
    """,'').replace('''\"
    ''','').strip()
    while '  ' in clean_text:
        clean_text = clean_text.replace('  ', ' ')
    return clean_text
proficiency_dict = {
    "1": "proficient",
    "2": "expert"
}
file_name = "lich.html"
# def html_to_json_monster(file_name, save = True):
#     print(file_name.split('.')[0])
#     with open(f'html_pages/monster/{file_name}', 'r') as mon:
#         mon_soup = BS(mon, 'html.parser')
#     new_file_name = file_name.split('.')[0]+".json"
#     ability_soup = mon_soup.find_all('span', {'class':'roller render-roller'})
#     meal = {'tags':[]}
#     for ability in ability_soup:
#         pre_json = (ability['data-packed-dice'].replace('\\','')+"\"").strip('\'{').split(',')
#         bite = {}
#         for element in pre_json:
#             try:
#                 element = element.split(':')
#                 bite[element[0].strip('"')] = element[1].strip('"').lower()
#             except:
#                 pass
#         try:
#             meal[bite['name']] = bite['displayText']
#         except:
#             pass
#     meal['name'] = mon_soup.find('h1').text
#     hp_soup = mon_soup.find_all("div")
#     hp_bite = [x for x in hp_soup if "Hit Points" in x.text][0]
#     hp = hp_bite.text.replace(hp_bite.strong.text, '')
#     meal['HP'] = sterilizer(hp)
#     meal['AC'] =  mon_soup.find('div',{"class":"mon__wrp-avoid-token"})

#     if meal['AC'] is None:
#         meal['AC'] = mon_soup.find_all("td", {'colspan':"6"})[1]

#     meal['AC'] = meal['AC'].text

#     for word in meal['AC'].split(' '):
#         if word.isnumeric():
#             meal['AC'] = int(word)
#             break
#     speed = [x.text for x in mon_soup.find_all('td', {'colspan':"6"}) if "Speed" in x.text][0].replace('Speed', '')
#     speed = [x.strip().strip('.').strip() for x in speed.split(',')]
#     meal['speed'] = speed
#     meal['saving_throws'] = {}
#     meal['skills'] = {}
#     soup_dict = {}
#     piece_meal = mon_soup.find_all("td", {"colspan":"6"})+ mon_soup.find_all("td", {"colspan":"3"})
#     sections = ["Saving Throws", "Skills", "Damage Resistances", "Damage Immunities","Condition Immunities", "Senses", "Languages", "Challenge"]
#     for piece in piece_meal:
#         for section in sections:
#             if section in piece.text:
#                 soup_dict[section] = piece
#                 sections.remove(section)
#                 break
#     mon_text = mon_soup.text
#     if "Saving Throws" in mon_text:
#         if "homunculus_servant" in file_name:
#             meal['saving_throws']['dexterity'] = 'proficient'
#         else:
#             saves = soup_dict["Saving Throws"].find_all('span',{'class':'roller render-roller'})
#             for save in saves:
#                 save_type = save['title'].split(" ")[0].lower()
#                 try:
#                     save_prof = proficiency_dict[save.find('span', {'class':'rd__roller--roll-prof-dice'}).text.replace('+','').split('d')[0]]
#                 except:
#                     save_prof = 'proficient'
#                 meal['saving_throws'][save_type] = save_prof

#     if 'Skills' in mon_text:
#         if "homunculus_servant" in file_name:
#             meal['skills']['stealth'] = 'proficient'
#             meal['skills']['perception'] = 'expert'
#         else:
#             skills = soup_dict["Skills"].find_all('span',{'class':'roller render-roller'})
#             for skill in skills:
#                 skill_type = skill['data-roll-name'].lower()
#                 try:
#                     skill_prof = proficiency_dict[skill['data-roll-prof-dice'].replace('+','').split('d')[0]]
#                 except:
#                     skill_prof = 'proficient'
#                 meal['skills'][skill_type] = skill_prof
    
#     if 'Damage Immunities' in mon_text:
#         immunities = soup_dict['Damage Immunities'].text.replace('Damage Immunities ', '').split(';')
#         immunities = [x.strip() for x in immunities]
#         meal['damage_immunities'] = immunities

#     if 'Damage Resistances' in mon_text:
#         resistances = soup_dict['Damage Resistances'].text.replace('Damage Resistances ', '').split(';')
#         resistances = [x.strip() for x in resistances]
#         meal['resistances'] = resistances
    
#     if 'Condition Immunities' in mon_text:
#         immunities = soup_dict['Condition Immunities'].text.replace('Condition Immunities ', '').split(';')
#         immunities = [x.strip() for x in immunities]
#         meal['condition_immunities'] = immunities
    
#     if 'Senses' in mon_text:
#         senses = soup_dict['Senses'].text.replace('Senses', '').split(',')
#         senses = [sterilizer(x) for x in senses]
#         meal['senses'] = senses
    
#     if 'Languages' in mon_text:
#         languages = soup_dict['Languages'].text.replace('Languages', '').split(',')
#         languages = [x.strip() for x in languages]
#         meal['languages'] = languages

#     if 'XP)' in soup_dict['Challenge'].text:
#         meal['CR'] = sterilizer(soup_dict['Challenge'].text).replace('Challenge', '').replace('n', '')

#     book_page = mon_soup.find('div',{"class":"stats-source flex-v-baseline"}).find_all('a')
#     if len(book_page) < 2:
#         book_page = mon_soup.find('div',{"class":"stats-source flex-v-baseline"}).find_all('span')
#     if len(book_page) < 2:
#         book = mon_soup.find("th", {'class': "rnd-name"}).find('a')
#         meal['book'] = book.attrs['title']
#     else:
#         meal['page'] = int(book_page[1].attrs['title'].split(" ")[1])
#         meal['book'] = book_page[0].attrs['title']
#     trait_soup = mon_soup.find('tr', {'class', 'trait'})
#     if trait_soup is not None:
#         traits = trait_soup.find_all('div', {'class': 'rd__b rd__b--3'})
#         meal['traits'] = {}
#         for trait in traits:
#             try:
#                 trait_name = trait.find("span", {"class":"entry-title-inner help-subtle"}).text
#             except:
#                 trait_name = trait.text.split('.')[0].strip()
#             if "Legendary Resistance" in trait:
#                 meal['traits']['legendary_resistance'] = int(trait_name.split("/Day")[0].split('(')[-1])
#             elif "Spellcasting" in trait_name:
#                 spellcasting_dict = {}
#                 spellcasting_dict['ability'] = trait.text.split(' (spell save DC')[0].split('spellcasting ability is ')[-1].lower()
#                 if 'innately' in trait.p.text or 'innate spellcasting' in mon_text.lower():
#                     spellcasting_dict['type']= "innate"
#                 elif 'magewright' in file_name:
#                     spellcasting_dict['type']= "ritualist"
#                 else:
#                     try:
#                         spellcasting_dict['level']= int(trait.p.text.split('th-level')[0].split(' ')[-1])
#                     except:
#                         try:
#                             spellcasting_dict['level']= int(trait.p.text.split('st-level')[0].split(' ')[-1])
#                         except:
#                             try:
#                                 spellcasting_dict['level']= int(trait.p.text.split('rd-level')[0].split(' ')[-1])
#                             except:
#                                 spellcasting_dict['level']= int(trait.p.text.split('nd-level')[0].split(' ')[-1])

#                     spellcasting_dict['type'] = trait.p.text.split('the following ')[-1].split(' spells')[0]
#                 if spellcasting_dict['type'] == 'innate':
#                     spell_dict = {}
#                     for box in trait.find_all("li", {"class":"rd__li rd__li-spell"}):
#                         print(box.p.text)
#                         par_diem = box.p.text.replace(':', '').strip().split(' ')[0]
#                         if par_diem == 'At':
#                             par_diem = 'at will' 
#                         spell_dict[par_diem] = []
#                         for a in box.find_all('a'):
#                             spell_dict[par_diem].append(a.text)
#                     spellcasting_dict['spells'] = spell_dict
#                 else:
#                     spellcasting_dict['spells'] = [x.text.replace('\n', '').replace('\\', '') for x in trait.find_all('a', {'data-vet-page':"spells.html"})]
#                 meal['traits']['spellcasting'] = spellcasting_dict
#             else:
#                 meal['traits'][sterilizer(trait_name).strip('.')] = sterilizer(trait.p.text)
#     meal['actions'] = {}

#     action_soup = mon_soup.find('tr', {'class', 'action'})

#     if action_soup is not None:

#         actions = action_soup.find_all('td', {'class', 'rd__b rd__b--3'})
#         if len(actions)<1:
#             actions = action_soup.find_all('div', {'class', 'rd__b rd__b--3'})
#         for action in actions:
#             action_name = action.find("span", {"class":"entry-title-inner help-subtle"}).text.replace('.','').strip()
#             action_text = action.p.text
#             meal['actions'][sterilizer(action_name)] = sterilizer(action_text)

#     legendary_dict = {
#         'number': 0,
#         'options': {}
#     }

#     if 'Legendary Actions' in mon_text:
#         legendary_soup = mon_soup.find_all('tr', {'class': 'legendary'})
#         legendary_dict['number'] = int(legendary_soup[0].find('td',{'colspan':"6"}).text.split(' legendary actions')[0].split(' ')[-1])
#         legendaries = legendary_soup[1].find_all('li', {'class':"rd__li"})
#         for legendary in legendaries:
#             leg_name = sterilizer(legendary.find('span', {'class': 'bold rd__list-item-name'}).text)
#             leg_text = sterilizer(legendary.p.text)
#             leg_text = leg_text.replace(leg_name, '')
#             legendary_dict['options'][leg_name.strip('.')] = leg_text
#         meal['legendary_actions'] = legendary_dict
#     if 'lair action' in mon_text.lower() and 'initiative count 20' in mon_text.lower():
#         lair_soup = mon_soup.find('tr', {'class':'lairaction'})
#         lair_actions = lair_soup.find_all('li', {'class': "rd__li"})

#         meal['in_lair'] = {
#             'CR_increase':1,
#             'actions':[]
#         }
#         for action in lair_actions:
#             lair_action = sterilizer(action.text)
#             meal['in_lair']['actions'].append(lair_action)

#     try:
#         sta = mon_soup.find('div',{"class":"mon__wrp-size-type-align--token"}).text
#     except:
#         sta = mon_soup.find_all('i')[0].text
#     if ',' not in sta:
#         meal['alignment'] = 'U'
#         sta = sta.split(' ')
#     else:
#         sta = sta.split(',')
#         meal['alignment'] = ''.join([x.upper()[:1] for x in sta[1].split(' ')])    
#         sta = sta[0].split(' ')
#     meal['size'] = sta[0]
#     meal['type'] = sta[1]
#     if len(sta)>2:
#         meal['tags'].append(sta[2].strip().strip(')').strip('('))
#     if save:
#         with open(f'jsons/monsters/{new_file_name}', 'w') as out:
#             json.dump(meal, out, indent = 4)

# %%
# files = os.listdir("html_pages/info")
# for file in files:
#     html_to_json(file)

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
 b"''', '').replace("(b'", "").replace("""
""", "")
        with open(f"{in_folder}/{file}", 'w') as new:
            new.write(clean)
# %%
html_cleaner('html_pages/spells')
# %%
def html_to_json_spells(file):
    with open(f'html_pages/spells/{file}', 'r') as mon:
        spell_soup = BS(mon, 'html.parser')
    spell_dict = {}
    name = spell_soup.find('h1').text
    spell_dict['name'] = sterilizer(name)
    lvl_school = spell_soup.find('td', {'class':"rd-spell__level-school-ritual"})
    if 'cantrip' in lvl_school.text.lower():
        spell_dict['level'] = 0
        school = sterilizer(lvl_school.text.split(' ')[0].lower())
    else:
        spell_dict['level'] = int(lvl_school.text.split('-level ')[0][:-2])
        school = sterilizer(lvl_school.text.split('-level ')[1].lower())
    if ' (ritual)' in school:
        spell_dict['ritual'] = True
        school = school.replace(' (ritual)','')
    else:
        spell_dict['ritual'] = False
    spell_dict['school'] = school
    basic_soup = spell_soup.find_all('td', {'colspan':'6'})[1:5]
    for bite in basic_soup:
        key = bite.find('span',{'class':'bold'}).text
        value = bite.text.replace(key, '')
        key = key.split(':')[0]
        spell_dict[key.lower()]=value
    if 'Concentration' in spell_dict['duration']:
        spell_dict['duration'] = spell_dict['duration'].replace('Concentration u', 'U')
        spell_dict['concentration'] = True
    else:
        spell_dict['concentration'] = False
    if '(' in spell_dict['components']:
        extras = spell_dict['components'].split('(')[1].replace(')', '')
        spell_dict['components'] = spell_dict['components'].split(' (')[0]
        spell_dict['extras'] = sterilizer(extras)
        costly_components = [int(x) for x in extras.split(' ') if x.isnumeric()]
        spell_dict['cost'] = sum(costly_components)
    description = spell_soup.find("td", {"class":"text", "colspan":"6"})
    description = description.find_all('div')
    description = [x.text for x in description]
    higher_levels = [x for x in description if 'at higher levels' in x.lower()]
    for h in higher_levels:
        description.remove(h)
    description = " ".join(description)
    description = sterilizer(description).replace('.','. ').replace('.  ', '. ')
    print(description)
    spell_dict["description"] = description
    if len(higher_levels) > 0:
        spell_dict["higher_levels"] = sterilizer(higher_levels[0]).replace('At Higher Levels.','')
    with open ('test.js', 'w') as pout:
        pprint(spell_dict, stream = pout)

spell_files = os.listdir('html_pages/spells')

for spell in spell_files[10:11]:
    html_to_json_spells(spell)
# %%
