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

#Una vez que tenemos variables economicas, vamos a variables culinarios de los paises. Para ello he descargado de kaggle los siguientes fichers:
#WorldsBestRestaurants.csv 
#Este dataframe indica los mejores restaurantes desde el año 2002 hasta el año 2023 por paises. 
import pandas as pd

# Cargar los CSV en DataFrames
df_best_restaurant = pd.read_csv(
    os.path.join("data", "WorldsBestRestaurants.csv"),
    encoding="latin-1"
)


# %%
df_best_restaurant = df_best_restaurant.drop(["location", "lat", "lng"], axis=1)

# %%
paises_seleccionados = ["Australia","Peru","Mexico","Brazil","Thailand","Chile","Argentina","China","Colombia",]

#Filtrar el DataFrame
df_paises_restaurantes = df_best_restaurant[df_best_restaurant["country"].isin(paises_seleccionados)]
df_paises_restaurantes.head(20)

# %%
df_paises_restaurantes = (df_paises_restaurantes["country"].value_counts())
print(df_paises_restaurantes)

# %%
df_rest_count = df_paises_restaurantes.reset_index() #creamos un dataframe a partir de esta serie
df_rest_count.columns = ['country', 'top 50 restaurantes'] #renombramos columnas para tener una columna pais y otra cantidad de restaurantes en el top50
df_rest_count = df_rest_count.rename(columns={'country': 'Pais'}) #cambiamos el nombre de country a pais para que haga match con nuestro df principal

#cambiamos los nombres para que detecte todos los paises en español
df_rest_count['Pais'] = df_rest_count['Pais'].replace({ 
    'Brazil': 'Brasil',
    'Thailand': 'Tailandia'
})


df_rest_count1 =df_rest_count
