# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
import time
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url_tasteatlas = "https://www.tasteatlas.com/best/cuisines"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url_tasteatlas)
time.sleep(3)

html = driver.page_source

taste_atlas = type("ResponseLike", (), {})()
taste_atlas.text = html
taste_atlas.status_code = 200
taste_atlas.reason = "OK"

driver.quit()

print(taste_atlas.status_code, taste_atlas.reason)

cuisine_taste_atlas = bs(taste_atlas.text, "html.parser")

print(taste_atlas.text[:500])

# %%
Pais = []
Ranking = []

dict_taste_atlas={'Pais': Pais,
      'Ranking': Ranking,
}

print(dict_taste_atlas)

# %%
ranking_items = cuisine_taste_atlas.find_all("div", class_="box-holder top-row-no-margin") 

for item in ranking_items: 

    # País
    pais_tag = item.find("div", class_="links flex second-row").find("a")
    if pais_tag:
        Pais.append(pais_tag["href"].split("/")[-1])
   
    # Ranking
    rank_tag = item.find("div", class_="rating with-title").find("span")
    if rank_tag:
        # Obtener el texto, reemplazar coma por punto y convertir a float
        Ranking.append(float(rank_tag.get_text().replace(",", ".")))

# %%
df_taste_atlas = pd.DataFrame(dict_taste_atlas)
df_taste_atlas = df_taste_atlas.rename(columns={'Ranking': 'Nota gastronomica'})

# %%
df_taste_atlas["Ranking Gastronomico"] = range(1, len(df_taste_atlas) + 1)

# %%
paises_seleccionados = ["australia","peru","mexico","brazil","thailand","chile","argentina","china","colombia","indonesia", "bolivia", "new-zealand", "laos","philippines", "vietnam","malaysia", "cambodia" ]

#Filtrar el DataFrame
df_taste_atlas = df_taste_atlas[df_taste_atlas["Pais"].isin(paises_seleccionados)]

# %%
#cambiamos los nombres para que detecte todos los paises en español
df_taste_atlas['Pais'] = df_taste_atlas['Pais'].replace({ 
    'mexico': 'Mexico',
    'indonesia': 'Indonesia',
    'china': 'China',
    'peru': 'Peru',
    'brazil': 'Brasil',
    'colombia': 'Colombia',
    'vietnam': 'Vietnam',
    'argentina': 'Argentina',
    'thailand': 'Tailandia',
    'chile': 'Chile',
    'philippines': 'Filipinas',
    'malaysia': 'Malasia',
    'australia': 'Australia',
    'new-zealand': 'Nueva Zelanda',
    'bolivia': 'Bolivia',
    'laos': 'Laos',
})


# %%
df_taste_atlas1=df_taste_atlas

# %%



