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

#Importamos un archivo con variables economicas de los paises en cuestion, este excel se ha obtenido desde la web World Economics Outlook database

# Cargar el archivo Excel
df_excel = pd.read_excel(os.path.join("data", "WEO_Data.xlsx"))


# %%
df_economic_paises = df_excel.pivot_table(
    index='Country',
    columns='Subject Descriptor',
    values='value'
).reset_index()


# %%
#Renombramos los paises de asia que aún estan en ingles y las columnas
df_economic_paises['Country'] = df_economic_paises['Country'].replace({
    'Brazil': 'Brasil',
    'Cambodia': 'Camboya',
    'Lao P.D.R.': 'Laos',
    'Malaysia': 'Malasia',
    'New Zealand': 'Nueva Zelanda',
    'Philippines': 'Filipinas',
    'Thailand': 'Tailandia',
})

df_economic_paises.rename(columns={
    'Country': 'Pais',
    'Gross domestic product, current prices': 'PIB (U.S. dollars)',
    'Gross national savings': 'Ahorro nacional bruto (% de PIB)',
    'Inflation, average consumer prices': '% Inflacion anual',
    'Population': 'Poblacion (Millones)',
    'Total investment': 'Inversion (% de PIB)',
    'Unemployment rate': '% paro'
}, inplace=True)


# %%
#Vemos que los datos para ahorro nacional bruto, inversion y paro no estan bien, ya que deberian ser porcertajes. 
# Esto viene del punto en los millares de la hoja de excel. Vamos a corregirlo aqui

excluir_indices = [4, 8, 9]
excluir_indices2 = [4, 9]

df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices), 'Inversion (% de PIB)'] = \
    round((df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices), 'Inversion (% de PIB)'] / 1000),2)

df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices2), 'Ahorro nacional bruto (% de PIB)'] = \
    round((df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices2), 'Ahorro nacional bruto (% de PIB)'] / 1000),2)

df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices), '% paro'] = \
    round((df_economic_paises.loc[~df_economic_paises.index.isin(excluir_indices), '% paro'] / 1000),2)

# %%

df_economic_paises1 =df_economic_paises
