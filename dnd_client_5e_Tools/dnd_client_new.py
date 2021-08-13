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
url = "https://5e.tools/bestiary.html#aarakocra_mm"

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
time.sleep(5)
dnd_soup = BS(browser.html, 'html.parser')

dnd_table = dnd_soup.find_all("a", {"class":"lst--border lst__row-inner"})
hrefs = [x['href'] for x in dnd_table]
print(type(hrefs[0]))
#%%
url = "https://5e.tools/bestiary.html"
for href in hrefs:
    name = href.split("#")[1].split("_")[0].replace('%20','_')
    new_url = url+href
    print(name)
    browser.visit(new_url)    
    time.sleep(5)
    try:
        browser.find_by_value('Statblock').click()
    except:
        pass
    dnd_soup = BS(browser.html, 'html.parser')
    dnd_soup = dnd_soup.find("table", {"class": "stats monster"})
    with open(f"html_pages/monsters/{name}.html", "w") as temp:
        pprint(dnd_soup, stream = temp)
    try:
        time.sleep(2)
        info_soup = BS(browser.html, 'html.parser')
        info_soup = info_soup.find("td", {"colspan":"6", "class":"text"})
        pprint(info_soup)
        with open(f"html_pages/info/{name}.html", "w") as temp:
            pprint(info_soup, stream = temp)
    except:
        pass
    try:
        browser.find_by_value('Images').click()
        time.sleep(2)
        image_soup = BS(browser.html, 'html.parser')
        image_soup = image_soup.find("div", {"class":"rd__wrp-image relative"})
        image_soup = image_soup.find("a", {'target':'_blank',"rel":"noopener noreferrer"})
        image_soup = image_soup.find('img')
        pprint(image_soup)
        img_src = image_soup['src']
        image_url = "https://5e.tools/"+img_src
        with open(f"images/{name}.jpg","wb") as f:
            f.write(req.get(image_url).content)
    except:
        pass
    print("     ", "finished")
browser.quit()
#%%
name_links = {}
for bit in dnd_soup.find_all("a",href=True):
    name_links[bit.text] = bit['href']

df = pd.read_html(browser.html)
browser.quit()
df['URL']=df['Name'].apply(url_finder)

df = pd.read_csv('spells.csv')
def html_writer(x, url):
    nameo=x.lower().replace("'",'-').replace(' ','-')
    url = f"https://www.aidedd.org/dnd/sorts.php?vo={nameo}"
    nameo=x.replace('/', ' OR ')
    print(f"Getting {x}")
    file_name = f"html_pages/spells/{nameo}.html"
    response = req.get(url)

    with open(file_name, 'w', encoding='utf-8') as stuff:
        stuff.write(response.text)


#%%
