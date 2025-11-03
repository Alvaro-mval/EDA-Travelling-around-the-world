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

url_crim = "https://es.numbeo.com/criminalidad/clasificaciones-por-pa%C3%ADs"


crim = requests.get(url_crim)

print(crim.status_code, crim.reason)

criminalidad_web = bs(crim.text, "lxml")

# %%
Pais = []
Criminalidad = []
Seguridad = []

dict_crim={'Pais': Pais,
      'Criminalidad': Criminalidad,
      'Seguridad': Seguridad,
}

print(dict_crim)

# %%
crim_secu = criminalidad_web.find_all("tr", attrs={"style": "width: 100%"})

for item in crim_secu: 

    # País
    pais_tag = item.find(class_="cityOrCountryInIndicesTable")
    if pais_tag:
        Pais.append(pais_tag.get_text(strip=True))
        
    # Criminalidad
    crim_tag = (item.find_all("td")[2]).get_text(strip=True)
    if crim_tag:
        Criminalidad.append(float(crim_tag.replace(",", ".")))

    # Seguridad
    secu_tag = (item.find_all("td")[3]).get_text(strip=True)
    if secu_tag:
        Seguridad.append(float(secu_tag.replace(",", ".")))

# %%
df_criminalidad = pd.DataFrame(dict_crim)

# %%
paises_seleccionados3 = ["Australia","Perú","México","Brasil","Tailandia","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "Nueva Zelanda", "Laos","Filipinas", "Vietnam","Malasia", "Camboya" ]


#Filtrar el DataFrame
df_criminalidad = df_criminalidad[df_criminalidad["Pais"].isin(paises_seleccionados3)]


# %%
#cambiamos los nombres para que detecte todos los paises en español
df_criminalidad["Pais"] = df_criminalidad["Pais"].replace({ 
    'Perú': 'Peru',
    'México': 'Mexico',
})

df_criminalidad = df_criminalidad.rename(columns={'Criminalidad': 'Indice de Criminalidad','Seguridad': 'Indice de Seguridad' })

# %%
#Nos falta el valor de Laos que no esta en los datos, 
# creamos la fila de Laos y le damos un valor de Criminalidad y Seguridad que sera la media de valores de los paises del sudeste asiatico.

mean_crim_sudasia = round(df_criminalidad.loc[df_criminalidad["Pais"].isin(["Camboya", "Malasia", "Indonesia", "Filipinas", "Vietnam", "Tailandia"]),"Indice de Criminalidad"].mean(),2)
mean_secu_sudasia = round(df_criminalidad.loc[df_criminalidad["Pais"].isin(["Camboya", "Malasia", "Indonesia", "Filipinas", "Vietnam", "Tailandia"]),"Indice de Seguridad"].mean(),2)

df_criminalidad.loc["200"] = ["Laos", mean_crim_sudasia, mean_secu_sudasia]

df_criminalidad1 =df_criminalidad
