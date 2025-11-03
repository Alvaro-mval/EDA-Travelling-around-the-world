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

#obtenemos valores de indices de paises mas amigables via la web: https://worldpopulationreview.com/country-rankings/friendliest-countries
url_friend = "https://worldpopulationreview.com/country-rankings/friendliest-countries"


friend = requests.get(url_friend)

print(friend.status_code, friend.reason)

friend_web = bs(friend.text, "lxml")

# %%
Pais = []
Ranking_friendly = []

dict_friend={'Pais': Pais,
      'Ranking amabilidad': Ranking_friendly,
}

print(dict_friend)

# %%
fr_web = friend_web.find_all("tr")

for item in fr_web:

    # País
    pais_tag1 = item.find("a", href=True) 
    if pais_tag1:  # Solo si existe
        Pais.append(pais_tag1.text.strip())
    else:
        Pais.append(None)

    # Amabilidad
    td_ama = item.find_all("td")
    if len(td_ama) > 2:
        td_ama2 = (td_ama[2].text.strip())
        separar = re.search(r"\d+", td_ama2)
        Ranking_friendly.append(int(separar.group()))
    else:
        Ranking_friendly.append(None)

# %%
df_friendly = pd.DataFrame(dict_friend)
#Elimino el primer valor que es None (era el encabezado de la web)
df_friendly = df_friendly.drop(df_friendly.index[0])

#Elimino la columna ranking amabilidad porque el indice me vale luego para eso.
df_friendly = df_friendly.drop(columns=["Ranking amabilidad"])


# %%
paises_seleccionados2 = ["Australia","Peru","Mexico","Brazil","Thailand","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "New Zealand", "Laos","Philippines", "Vietnam","Malaysia", "Cambodia" ]
#Filtrar el DataFrame
df_friendly = df_friendly[df_friendly["Pais"].isin(paises_seleccionados2)]

#pasamos el ranking a columna y reseteamos index
df_friendly = df_friendly.reset_index(names="Ranking amabilidad")


# %%
#cambiamos los nombres para que detecte todos los paises en español
df_friendly["Pais"] = df_friendly["Pais"].replace({ 
    'Thailand': 'Tailandia',
    'Brazil': 'Brasil',
    'Philippines': 'Filipinas',
    'Malaysia': 'Malasia',
    'Cambodia': 'Camboya',
})

df_friendly1 =df_friendly
