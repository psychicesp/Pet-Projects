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
c = 0
for href in hrefs[160:]:
    c += 1
    name = href.split("#")[1].split("_")[0].replace('%20','_')
    new_url = url+href
    print(name)
    browser.visit(new_url)
    if c < 2:    
        time.sleep(5)
    else:
        time.sleep(2)
    dnd_soup = BS(browser.html, 'html.parser')
    dnd_soup = dnd_soup.find("table", {"class": "stats monster"})
    with open(f"html_pages/monsters/{name}.html", "w") as temp:
        pprint(dnd_soup.encode('utf8'), stream = temp)
    try:
        browser.find_by_value('Info').click()
        time.sleep(2)
        info_soup = BS(browser.html, 'html.parser')
        info_soup = info_soup.find("td", {"colspan":"6", "class":"text"})
        with open(f"html_pages/info/{name}.html", "w") as temp:
            pprint(info_soup.encode('utf8'), stream = temp)
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
    try:
        browser.find_by_value('Statblock').click()
    except:
        pass
    print("     ", "finished")
browser.quit()
#%%

#%%
