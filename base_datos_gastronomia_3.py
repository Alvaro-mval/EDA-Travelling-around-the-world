# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
from bs4 import BeautifulSoup as bs
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url_tasteatlas2 = "https://www.tasteatlas.com/best/dishes"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url_tasteatlas2)
time.sleep(3)

html2 = driver.page_source

taste_atlas2 = type("ResponseLike", (), {})()
taste_atlas2.text = html2
taste_atlas2.status_code = 200
taste_atlas2.reason = "OK"

driver.quit()

print(taste_atlas2.status_code, taste_atlas2.reason)

cuisine_taste_atlas2 = bs(taste_atlas2.text, "html.parser")

# %%
Pais = []
Nota = []

dict_taste_atlas2={'Pais': Pais,
      'Nota': Nota,
}

print(dict_taste_atlas2)

# %%
ranking_items2 = cuisine_taste_atlas2.find_all("div", class_="box-holder top-row-no-margin") 

for item in ranking_items2: 

    # País
    Pais_tag2 = item.find("div", class_="text flex").find("span")
    if Pais_tag2:
        # Obtener el texto
        Pais.append(Pais_tag2.get_text(strip=True))

   
    # Nota
    Nota_tag2 = item.find("div", class_="rating").find("span")
    if Nota_tag2:
        # Obtener el texto, reemplazar coma por punto y convertir a float
        Nota.append(float(Nota_tag2.get_text().replace(",", ".")))

# %%
df_taste_atlas_dish = pd.DataFrame(dict_taste_atlas2)
df_taste_atlas_dish = df_taste_atlas_dish.rename(columns={'Nota': 'Nota gastronomica'})

# %%
paises_seleccionados = ["Australia","Peru","Mexico","Brazil","Thailand","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "New Zealand", "Laos","Philippines", "Vietnam","Malaysia", "Cambodia" ]


#Filtrar el DataFrame
df_taste_atlas_dish = df_taste_atlas_dish[df_taste_atlas_dish["Pais"].isin(paises_seleccionados)]

# %%
df_taste_atlas_dish = (df_taste_atlas_dish["Pais"].value_counts())

# %%
df_dish = df_taste_atlas_dish.reset_index() #creamos un dataframe a partir de esta serie
df_dish.columns = ['Pais', 'Platos en top 100'] #renombramos columnas para tener una columna pais y otra cantidad de platos en el top100


# %%
df_dish1=df_dish

# %%



