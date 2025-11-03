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

# %%
from base_datos_tourmondista import df_mundo1
from base_datos_economia import df_economic_paises1
from base_datos_gastronomia import df_rest_count1
from base_datos_gastronomia_2 import df_taste_atlas1
from base_datos_gastronomia_3 import df_dish1
from base_datos_criminalidad import df_criminalidad1
from base_datos_corrupcion import df_corrupcion1
from base_datos_amigabilidad import df_friendly1
from base_datos_amigabilidad2 import df_paises_friendly1
from base_datos_afluencia_turistica import df_llegadas1
from base_datos_hoteles import df_accomodation1
from base_datos_ingles import df_ingles1
from base_datos_transporte import df_carreteras1
from base_datos_transporte import df_muertes_carreteras1



# %%
df_mundo_economics1 = pd.merge(df_mundo1,df_economic_paises1, how='left')

# %%
df_mundo_economics2 = pd.merge(df_mundo_economics1,df_rest_count1, how='left')
df_mundo_economics3 = pd.merge(df_mundo_economics2,df_taste_atlas1, how='left')
df_mundo_economics4 = pd.merge(df_mundo_economics3,df_dish1, how='left')

df_mundo_economics4['top 50 restaurantes'] = df_mundo_economics4['top 50 restaurantes'].fillna(0).astype(int)

#llenamos los datos que faltan de Camboya para poder hacer las graficas luego.
#Damos un valor por defecto de 3 en la nota y ranking de 125.

df_mundo_economics4.loc[df_mundo_economics4["Pais"] == "Camboya", "Nota gastronomica"] = (df_mundo_economics4.loc[df_mundo_economics4["Pais"] == "Camboya", "Nota gastronomica"].fillna(3).astype(int))

df_mundo_economics4.loc[df_mundo_economics4["Pais"] == "Camboya", "Ranking Gastronomico"] = (df_mundo_economics4.loc[df_mundo_economics4["Pais"] == "Camboya", "Ranking Gastronomico"].fillna(125).astype(int))

df_mundo_economics4['Platos en top 100'] = df_mundo_economics4['Platos en top 100'].fillna(0).astype(int) #llenamos de 0 los paises que no tengan platos en el top 100


# %%
df_mundo_economics5 = pd.merge(df_mundo_economics4,df_criminalidad1, how='left')
df_mundo_economics6 = pd.merge(df_mundo_economics5,df_corrupcion1, how='left')

# %%
df_mundo_economics7 = pd.merge(df_mundo_economics6,df_friendly1, how='left')
df_mundo_economics8 = pd.merge(df_mundo_economics7,df_paises_friendly1, how='left')
#llenamos de 100 los paises que no tengan ranking de amabilidad

df_mundo_economics8['Ranking amabilidad'] = df_mundo_economics8['Ranking amabilidad'].fillna(100).astype(int) 

df_mundo_economics8['Ranking amabilidad'] = round(df_mundo_economics8['Ranking amabilidad'], 0)

# %%
df_mundo_economics9 = pd.merge(df_mundo_economics8,df_llegadas1, how='left')
df_mundo_economics10 = pd.merge(df_mundo_economics9,df_accomodation1, how='left')

#Creamos una columna "% de poblacion en sector turismo" a traves de nuestros datos de poblacion y numero de trabajaradores en el turismo
df_mundo_economics10["% poblacion en turismo"] = round((df_mundo_economics10["Numero de personas en sector turismo"] / (df_mundo_economics10["Poblacion (Millones)"]*1000000))*100,1)

# %%
df_mundo_economics11 = pd.merge(df_mundo_economics10,df_ingles1, how='left')

poblacion_ingles_bolivia = ((df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Bolivia", "Poblacion (Millones)"])*1000000) /(df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Bolivia", "% personas que hablan ingles"])  
poblacion_ingles_vietnam = ((df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Vietnam", "Poblacion (Millones)"])*1000000) /(df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Vietnam", "% personas que hablan ingles"])  

df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Bolivia","Total English speakers"] = poblacion_ingles_bolivia
df_mundo_economics11.loc[df_mundo_economics11["Pais"] == "Vietnam","Total English speakers"] = poblacion_ingles_vietnam


# %%
df_mundo_economics12 = pd.merge(df_mundo_economics11,df_carreteras1, how='left')
df_mundo_economics = pd.merge(df_mundo_economics12,df_muertes_carreteras1, how='left')

# %%



