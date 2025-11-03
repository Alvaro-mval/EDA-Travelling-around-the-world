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

#En wikipedia encontramos una lista de parametros sobre angloparlantes en paises del mundo que nos puede ayudar, la descargamos mediante API
TITLE = "List_of_countries_by_English-speaking_population"
url = f"https://en.wikipedia.org/api/rest_v1/page/html/{TITLE}"

headers = {
    "User-Agent": "MiProyecto/1.0 (Python script para análisis personal)"
}

resp = requests.get(url, headers=headers, timeout=30)
resp.raise_for_status()
html = resp.text

# pandas puede leer las tablas directamente desde un string HTML
n_tablas = pd.read_html(html)

# inspecciona cuántas tablas encontró y muestra la primera (probablemente la que buscas)
df_ingles = n_tablas[5]  # ajusta el índice si no es la tabla correcta
print(df_ingles.head(5))


# guarda a CSV
df_ingles.to_csv("english_speaking_by_country.csv", index=False, encoding="utf-8")

# %%
print(df_ingles.columns.tolist())

# %%
df_ingles = df_ingles.loc[
    df_ingles["Country"].isin([
        "Australia","Peru","Mexico","Brazil","Thailand","Chile",
        "Argentina","China","Colombia","Indonesia","Bolivia",
        "New Zealand","Laos","Philippines","Viet Nam","Malaysia",
        "Cambodia","Myanmar","Ecuador"
    ]),
    ["Country", "Total English speakers", "Total\xa0%"]
]

df_ingles = df_ingles.reset_index(drop=True)

# %%
#Como nos faltan 4 paises sin datos ["Peru", "Bolivia", "Laos", "Viet Nam"], vamos a sacarlos por dos metodos:
#Para Peru y Laos, suponemos que los paises vecinos de iguales parametros de habitantes y PIB pueden tener el mismo nivel de ingles
#En este contexto, remplazamos Ecuador por Peru y Myanmar por Laos.
#Aparte, remplazamos tambien las nombres en ingles por nombres en español
df_ingles["Country"] = df_ingles["Country"].replace({ 
    'Ecuador': 'Peru',
    'Myanmar': 'Laos',
    'Philippines': 'Filipinas',
    'Thailand': 'Tailandia',
    'Malaysia': 'Malasia',
    'Brazil': 'Brasil',
    'New Zealand': 'Nueva Zelanda',
    'Cambodia': 'Camboya',
})
#tambien cambiamos el nombre de las columnas 
df_ingles.rename(columns={
    'Country': 'Pais',
    'Total\xa0%': '% personas que hablan ingles',
    }, inplace=True)

# %%
#Para Vietnam y Bolivia, hacemos la media de porcentage de los paises que tienen alrededor. 
#Para hacer la media, quitamos el % de la columna y pasamos la variable a float
df_ingles["% personas que hablan ingles"] = df_ingles["% personas que hablan ingles"].str.replace("%", "", regex=False).astype(float)

media_bolivia =  round(df_ingles.loc[df_ingles["Pais"].isin(["Brasil", "Argentina", "Colombia", "Peru"]),"% personas que hablan ingles"].mean(),2)
media_vietnam =  round(df_ingles.loc[df_ingles["Pais"].isin(["Indonesia", "Filipinas", "Tailandia", "Malasia", "Camboya"]),"% personas que hablan ingles"].mean(),2)
df_ingles.loc[15] = ["Bolivia", np.nan, media_bolivia]
df_ingles.loc[16] = ["Vietnam", np.nan, media_vietnam]

# %%

df_ingles1=df_ingles
