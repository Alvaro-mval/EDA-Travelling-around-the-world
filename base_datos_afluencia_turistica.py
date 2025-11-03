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

#Vamos a la web https://datos.bancomundial.org/indicador/ST.INT.ARVL?end=2020&start=2020&year=2020 
# y nos descargamos un CSV con los datos de llegadas de pasajeros a nuestros paises.  

# Leer desde JSON
df_llegadas = pd.read_csv(r'C:\Users\Alvar\Documents\GitHub\Entornos-virtuales\EDA\data\llegadas_acomodacion\API_ST.INT.ARVL_DS2_es_csv_v2_34308.csv',on_bad_lines='warn', engine='python')


# %%
df_llegadas = df_llegadas.loc[:, ["Country Name", "2017", "2018", "2019", "2020", "2021", "2022", "2023","2024"]]

paises_seleccionados6 = ["Australia","Perú","México","Brasil","Tailandia","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "Nueva Zelandia", "República Democrática Popular Lao","Filipinas", "Viet Nam","Malasia", "Camboya" ]

df_llegadas = df_llegadas[df_llegadas["Country Name"].isin(paises_seleccionados6)]

# %%
#como no tenemos datos en los años 2021-2024, los eliminamos y nos quedamos con los años mas recientes, 2019 y 2020.

df_llegadas = df_llegadas.drop(columns=["2017","2018","2021","2022","2023","2024"])

#Creo una columna numero de turistas con los valores mas recientes, que mezcla datos de 2019 y 2020.

df_llegadas["Numero de turistas"] = df_llegadas["2020"].fillna(df_llegadas["2019"])                                                                               


# %%
#eliminamos las columnas 2019 y 2020 que ya no necesitamos
df_llegadas = df_llegadas.drop(columns=["2019","2020"])

#cambiamos el nombre de la columna Country Name a Pais

df_llegadas.rename(columns={
    'Country Name': 'Pais'
    }, inplace=True)

#cambiamos los nombres para que detecte todos los paises en español
df_llegadas["Pais"] = df_llegadas["Pais"].replace({ 
    'República Democrática Popular Lao': 'Laos',
    'México': 'Mexico',
    'Nueva Zelandia': 'Nueva Zelanda',
    'Perú': 'Peru',
    'Viet Nam': 'Vietnam'
})


df_llegadas1=df_llegadas
