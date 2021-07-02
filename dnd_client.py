#%%
import pandas as pd

url = "https://donjon.bin.sh/5e/monsters/"

monsters = pd.read_html(url)

monsters.to_csv("monster_list.csv")