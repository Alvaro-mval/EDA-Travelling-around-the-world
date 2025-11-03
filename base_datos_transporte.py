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

#En wikipedia encontramos una lista de datos de la mortalidad en carretera por paises, la descargamos mediante API
TITLE = "Anexo:Países_por_tasa_de_muertes_por_siniestros_de_tránsito"
url_road = f"https://es.wikipedia.org/api/rest_v1/page/html/{TITLE}"

headers = {
    "User-Agent": "MiProyecto/1.0 (script personal para análisis educativo)"
}

resp = requests.get(url_road, headers=headers, timeout=30)
resp.raise_for_status()
html_road = resp.text

# pandas puede leer las tablas directamente desde un string HTML
tablas_road = pd.read_html(html_road)

df_muertes_carreteras = tablas_road[0]


# guarda a CSV
df_muertes_carreteras.to_csv("muertes_carreteras.csv", index=False, encoding="utf-8")

df_muertes_carreteras = df_muertes_carreteras.loc[
    df_muertes_carreteras["Países"].isin([
        "Australia","Perú","México","Brasil","Tailandia","Chile",
        "Argentina","China","Colombia","Indonesia","Bolivia",
        "Nueva Zelanda","Laos","Filipinas","Vietnam","Malasia",
        "Camboya"
    ]),
    ["Países", "Tasa de mortalidad en siniestros de tránsito por cada 100 000 habitantes",
      "Tasa de mortalidad en siniestros de tránsito por cada 100 000 vehículos motorizados",
      "Total fallecidos año más reciente (ajustado/estimado por el OMS)"]
]


df_muertes_carreteras = df_muertes_carreteras.reset_index(drop=True)

#tambien cambiamos el nombre de las columnas 
df_muertes_carreteras.rename(columns={
    'Países': 'Pais',
    'Tasa de mortalidad en siniestros de tránsito por cada 100 000 habitantes': 'muertes en carretera por cada 100.000 habitantes',
    'Tasa de mortalidad en siniestros de tránsito por cada 100 000 vehículos motorizados': 'muertes en carretera por cada 100.000 vehiculos',
    'Total fallecidos año más reciente (ajustado/estimado por el OMS)': 'Total fallecidos al año',
    }, inplace=True)
#cambiamos nombres quitando los acentos
df_muertes_carreteras['Pais'] = df_muertes_carreteras['Pais'].replace({ 
    'México': 'Mexico',
    'Perú': 'Peru'
})

#Vemos que el primer valor para nueva zelanda no es numerico ya que tiene un pie de pagina, vamos a quitarselo.
df_muertes_carreteras.loc[df_muertes_carreteras["Pais"] == "Nueva Zelanda","muertes en carretera por cada 100.000 habitantes"] = 8.5

#tambien vemos que la ultima columna tiene algunos espacios que correspondian a comas en la tabla de wikipedia, vamos a quitarlos para poder trabajar con la tabal

df_muertes_carreteras["Total fallecidos al año"] = df_muertes_carreteras["Total fallecidos al año"].astype(str).str.replace(" ", "", regex=False)
df_muertes_carreteras["Total fallecidos al año"] = pd.to_numeric(df_muertes_carreteras["Total fallecidos al año"], errors="coerce")


#En la web https://www.indexmundi.com/map/?v=115&l=es vemos una tabla que nos muestra los paises por numero de km de carreteras, obtenemos la tabla mediante web scrapping
from bs4 import BeautifulSoup as bs

url_carreteras = "https://www.indexmundi.com/map/?v=115&l=es"

carreteras = requests.get(url_carreteras)

print(carreteras.status_code, carreteras.reason)

carreteras_km = bs(carreteras.text, "lxml")

Pais = []
Km_carreteras = []

dict_carreteras={'Pais': Pais,
      'Total Km carreteras': Km_carreteras,
}

print(dict_carreteras)

paises_carretera = carreteras_km.find("table", attrs={'cellspacing': "0"})

filas = paises_carretera.find_all("tr")
for fila in filas:
    celdas = fila.find_all("td")
    if len(celdas) < 2:
        continue
    # País
    Pais.append(celdas[0].text.strip())
    # Km carreteras
    Km_carreteras.append(celdas[1].text.strip().replace(",", ""))

print(dict_carreteras)

df_carreteras = pd.DataFrame(dict_carreteras)

df_carreteras = df_carreteras.loc[
    df_carreteras["Pais"].isin([
        "Australia","Perú","México","Brasil","Tailandia","Chile",
        "Argentina","China","Colombia","Indonesia","Bolivia",
        "Nueva Zelanda","Laos","Filipinas","Vietnam","Malasia",
        "Camboya"
    ])
]

df_carreteras['Pais'] = df_carreteras['Pais'].replace({ 
    'México': 'Mexico',
    'Perú': 'Peru'
})

df_carreteras = df_carreteras.reset_index(drop=True)

df_carreteras1=df_carreteras
df_muertes_carreteras1=df_muertes_carreteras