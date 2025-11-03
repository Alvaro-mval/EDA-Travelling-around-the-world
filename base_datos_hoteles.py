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

#Vamos a la web https://www.untourism.int/tourism-statistics 
# y descargamos varios ficheros excel correspondientes al numero de personas que trabajan para el turismo y varios datos de hoteles y acomodacion.

# Leer desde JSON
df_sector_turismo = pd.read_excel(
    os.path.join("data", "llegadas_acomodacion", "UN_Tourism_8_9_2_employed_persons_04_2025.xlsx"),
    sheet_name=1,
    engine="openpyxl"
)

df_accomodation = pd.read_excel(
    os.path.join("data", "llegadas_acomodacion", "UN_Tourism_accommodation_hotels_10_2025.xlsx"),
    sheet_name=1,
    engine="openpyxl"
)


# %%
#filtramos filas y columnas para quedarnos con los años mas recientes y con las columnas de pais, año, parametro y valor.

df_sector_turismo = df_sector_turismo.loc[df_sector_turismo["TimePeriod"].isin([2018,2019,2020,2021,2022, 2023]),["GeoAreaName", "TimePeriod", "Value"]]

df_accomodation = df_accomodation.loc[df_accomodation["year"].isin([2018,2019,2020,2021,2022, 2023]),["reporter_area_label", "indicator_label","year", "value"]]

# %%
paises_seleccionados7 = ["Australia","Peru","Mexico","Brazil","Thailand","Chile","Argentina","China","Colombia","Indonesia", "Bolivia", "New Zealand", "Laos","Philippines", "Viet Nam","Malaysia", "Cambodia"]

#quitamos todos los demas paises 
df_sector_turismo = df_sector_turismo[df_sector_turismo["GeoAreaName"].isin(paises_seleccionados7)]

df_accomodation = df_accomodation[df_accomodation["reporter_area_label"].isin(paises_seleccionados7)]

#y hacemos value_count para comprobar que tenemos los 17 que nos interesan
print(df_accomodation["reporter_area_label"].value_counts())
print(df_sector_turismo["GeoAreaName"].value_counts())

# %%
#Creo una columna con los valores mas recientes, que mezcla datos desde 2018 a 2024.

df_sector_turismo = df_sector_turismo.sort_values(["GeoAreaName", "TimePeriod"], ascending=[True, False])

df_accomodation = df_accomodation.sort_values(["reporter_area_label","indicator_label", "year"], ascending=[True,True, False])

# Quedarse solo con la fila más reciente por país

df_sector_turismo = df_sector_turismo.drop_duplicates(subset="GeoAreaName", keep="first")
df_accomodation = df_accomodation.drop_duplicates(subset=["reporter_area_label","indicator_label"], keep="first")

# %%
#modificamos el dataframe para tener una fila por pais y los parametros uno en cada columna
df_accomodation = df_accomodation.pivot_table(
    index='reporter_area_label',
    columns='indicator_label',
    values='value'
).reset_index()

#Cambio el nombre de las columnas
df_accomodation.rename(columns={
    'reporter_area_label': 'Pais',
    'capacity - accommodation - short-term accommodation, hotels and similar (ISIC 5510) - bed places': 'Numero de camas',
    'capacity - accommodation - short-term accommodation, hotels and similar (ISIC 5510) - establishments': 'Numero de hoteles',
    'capacity - accommodation - short-term accommodation, hotels and similar (ISIC 5510) - rooms': 'Numero de habitaciones',
    'capacity - accommodation - short-term accommodation, hotels and similar (ISIC 5510) - rooms - rate': 'Ratio de ocupacion'
}, inplace=True)

#Elimino la columna de dias de estancia media que no vamos a usar.
df_accomodation = df_accomodation.drop(columns=["capacity - accommodation - short-term accommodation, hotels and similar (ISIC 5510) - length of stay - average"])

#Comprobamos que los datos tienen sentido y que hay mayor numero de camas que de habitaciones y que de hoteles
#df_accomodation["comprobacion"] = df_accomodation["Numero de camas"] > df_accomodation["Numero de habitaciones"]
#df_accomodation["comprobacion2"] = df_accomodation["Numero de habitaciones"] > df_accomodation["Numero de hoteles"]



# %%
#Ahora ya podemos suprimir la columna TimePeriod

df_sector_turismo = df_sector_turismo.drop(columns=["TimePeriod"])

#cambiamos el nombre de la columna GeoAreaName Name a Pais

df_sector_turismo.rename(columns={
    'GeoAreaName': 'Pais',
    "Value": "Numero de personas en sector turismo"
    }, inplace=True)

#cambiamos los nombres para que detecte todos los paises en español para nuestros dos dataframes
df_sector_turismo["Pais"] = df_sector_turismo["Pais"].replace({ 
    'Brazil': 'Brasil',
    'Cambodia': 'Camboya',
    'Malaysia': 'Malasia',
    'New Zealand': 'Nueva Zelanda',
    'Thailand': 'Tailandia',
    'Philippines': 'Filipinas',
    'Viet Nam': 'Vietnam'
})

df_accomodation["Pais"] = df_accomodation["Pais"].replace({ 
    'Brazil': 'Brasil',
    'Cambodia': 'Camboya',
    'Malaysia': 'Malasia',
    'New Zealand': 'Nueva Zelanda',
    'Thailand': 'Tailandia',
    'Philippines': 'Filipinas',
    'Viet Nam': 'Vietnam'
})


# %%
#hacemos el merge manteniendo entero los dos nuevos data frame (acomodation y numero de turistas)
df_accomodation = pd.merge(df_accomodation, df_sector_turismo, how='left') 

# %%

# %%

df_accomodation1 = df_accomodation

