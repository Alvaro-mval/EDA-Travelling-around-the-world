# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
import os
from bs4 import BeautifulSoup as bs

#Vamos a la web https://worldpopulationreview.com/country-rankings/friendliest-countries 
# y nos descargamos un json llamado friendliest-countries con unos rankings relacionados con la acogida de un pais a los extranjeros:
#facilidad de adaptacion, bienvenida, amigos locales , facilidad para hacer amigos.

# Leer desde JSON
with open(os.path.join("data", "friendliest-countries.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# %%
df_paises_friendly = pd.DataFrame(paises_friendly_json)

# %%
df_paises_friendly = df_paises_friendly.drop(df_paises_friendly.index[0])

paises_seleccionados5 = ["Australia","Peru","Mexico","Brazil","Thailand","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "NewZealand", "Laos","Philippines", "Vietnam","Malaysia", "Cambodia" ]
#Renombramos el pais de Nueva Zelanda porque dada el formato de la tabla no reconoce el texto.
df_paises_friendly.loc[df_paises_friendly["flagCode"] == "NZ", "country"] = "NewZealand"

#Elimino la columna ranking amabilidad porque el indice me vale luego para eso.
df_paises_friendly = df_paises_friendly.drop(columns=["flagCode"])

#Filtrar el DataFrame con paises seleccionados2 (son todos nuestros paises en ingles)
df_paises_friendly = df_paises_friendly[df_paises_friendly["country"].isin(paises_seleccionados5)]


# %%
#cambiamos los nombres para que detecte todos los paises en español
df_paises_friendly["country"] = df_paises_friendly["country"].replace({ 
    'Thailand': 'Tailandia',
    'Brazil': 'Brasil',
    'Philippines': 'Filipinas',
    'Malaysia': 'Malasia',
    'Cambodia': 'Camboya',
    "NewZealand": "Nueva Zelanda"
})

df_paises_friendly.rename(columns={
    'country': 'Pais',
    'InterNationsEaseOfSettlingInIndex_2024': 'Ranking facilidad de adaptación',
    'InterNationsCultureAndWelcomeIndex_2024': 'Ranking bienvenida calurosa',
    'InterNationsLocalFriendlinessIndex_2024': 'Ranking amigos locales',
    'InterNationsFindingFriendsIndex_2024': 'Ranking facilidad amigos'
}, inplace=True)


df_paises_friendly1 =df_paises_friendly
