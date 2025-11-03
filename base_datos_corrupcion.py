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


#obtenemos valores de indices de corrupcion por pais via la web: https://www.datosmundial.com/corrupcion.php?full
url_corr = "https://www.datosmundial.com/corrupcion.php?full"


corr = requests.get(url_corr)

print(corr.status_code, corr.reason)

corrupcion_web = bs(corr.text, "lxml")

# %%
Pais = []
Corrupcion = []

dict_corr={'Pais': Pais,
      'Indice de Corrupcion': Corrupcion,
}

print(dict_corr)

# %%
corr_web = corrupcion_web.find_all("tr")

for item in corr_web:

    # País
    a_tag = item.find("a", href=True) 
    if a_tag:  # Solo si existe
        Pais.append(a_tag.text.strip())
    else:
        Pais.append(None)

    # Corrupción
    td_list = item.find_all("td")
    if len(td_list) > 1:
        Corrupcion.append(td_list[1].text.strip())
    else:
        Corrupcion.append(None)

# %%
df_corrupcion = pd.DataFrame(dict_corr)
#Elimino el primer valor que es None (era el encabezado de la web)
df_corrupcion = df_corrupcion.drop(df_corrupcion.index[0])


# %%
paises_seleccionados4 = ["Australia","Perú","México","Brasil","Tailandia","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "Nueva Zelandia", "Laos","Filipinas", "Vietnam","Malasia", "Camboya" ]

#Filtrar el DataFrame
df_corrupcion = df_corrupcion[df_corrupcion["Pais"].isin(paises_seleccionados4)]

#pasamos el ranking a columna y reseteamos index
df_corrupcion = df_corrupcion.reset_index(names="Ranking Corrupcion")


# %%
#cambiamos los nombres para que detecte todos los paises en español
df_corrupcion["Pais"] = df_corrupcion["Pais"].replace({ 
    'Perú': 'Peru',
    'México': 'Mexico',
    'Nueva Zelandia': 'Nueva Zelanda',
})

# %%

# %%
df_corrupcion1 =df_corrupcion


