# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import openpyxl
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bootcampviztools import plot_categorical_relationship_fin, pinta_distribucion_categoricas, plot_grouped_histograms,\
    plot_grouped_boxplots, plot_combined_graphs, plot_categorical_numerical_relationship, bubble_plot,\
        grafico_dispersion_con_correlacion
from scipy.stats import chi2_contingency, mannwhitneyu

from merge_df import df_mundo_economics

# %%
import warnings
warnings.filterwarnings("ignore")

# %%
# Primero dividir las variables por tipo, usando la función que programamos en los ejercicios
def card_tipo(df,umbral_categoria = 10, umbral_continua = 30):
    # Primera parte: Preparo el dataset con cardinalidades, % variación cardinalidad, y tipos
    df_temp = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad y porcentaje de variación de cardinalidad
    df_temp = df_temp.T # Como nos da los valores de las columnas en columnas, y quiero que estas sean filas, la traspongo
    df_temp = df_temp.rename(columns = {0: "Card", 1: "%_Card", 2: "Tipo"}) # Cambio el nombre de la transposición anterior para que tengan más sentido, y uso asignación en vez de inplace = True (esto es arbitrario para el tamaño de este dataset)

    # Corrección para cuando solo tengo un valor
    df_temp.loc[df_temp.Card == 1, "%_Card"] = 0.00

    # Creo la columna de sugerenica de tipo de variable, empiezo considerando todas categóricas pero podría haber empezado por cualquiera, siempre que adapte los filtros siguientes de forma correspondiente
    df_temp["tipo_sugerido"] = "Categorica"
    df_temp.loc[df_temp["Card"] == 2, "tipo_sugerido"] = "Binaria"
    df_temp.loc[df_temp["Card"] >= umbral_categoria, "tipo_sugerido"] = "Numerica discreta"
    df_temp.loc[df_temp["%_Card"] >= umbral_continua, "tipo_sugerido"] = "Numerica continua"
    # Ojo los filtros aplicados cumplen con el enunciado pero no siguen su orden y planteamiento

    return df_temp

# %%
#Vemos que en nuestro análisis todas las variables son de tipo Numérica continua, por lo tanto no haremos análisis categóricos.

card_tipo(df_mundo_economics)

# %%
numericas = ['Nota Global', 'Presupuesto', 'Acogida', 'Comunicacion',
       'Cultura', 'Affluencia turistica', 'Gastronomia', 'Hoteles', 'Paisajes',
       'Limpieza', 'Seguridad', 'Tranquilidad', 'Transportes', 'Ciudades',
       'PIB (U.S. dollars)', 'Ahorro nacional bruto (% de PIB)',
       '% Inflacion anual', 'Poblacion (Millones)', 'Inversion (% de PIB)',
       '% paro', 'top 50 restaurantes', 'Nota gastronomica', 'Ranking Gastronomico',
       'Platos en top 100', 'Indice de Criminalidad', 'Indice de Seguridad',
       'Ranking Corrupcion', 'Indice de Corrupcion', 'Ranking amabilidad',
       'Ranking facilidad de adaptación', 'Ranking bienvenida calurosa',
       'Ranking amigos locales', 'Ranking facilidad amigos',
       'Numero de turistas', 'Numero de camas', 'Numero de hoteles',
       'Numero de habitaciones', 'Ratio de ocupacion',
       'Numero de personas en sector turismo', '% poblacion en turismo',
       'Total English speakers', '% personas que hablan ingles',
       'Total Km carreteras',
       'muertes en carretera por cada 100.000 habitantes',
       'muertes en carretera por cada 100.000 vehiculos',
       'Total fallecidos al año']

# %%
def preparar_regiones(df_mundo_economics):
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Australia", "Nueva Zelanda"]), "Region"] = "Oceania"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["China"]), "Region"] = "China"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Argentina", "Mexico", "Brasil", "Colombia", "Peru", "Bolivia", "Chile"]), "Region"] = "Latinoamerica"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Filipinas", "Indonesia", "Tailandia", "Vietnam", "Laos", "Malasia", "Camboya"]), "Region"] = "Sudeste asiatico"
    return df_mundo_economics

# %%
def plot_categorical_numerical_relationship(df, categorical_col, numerical_col):
    """
    Genera un barplot mostrando el valor promedio de una variable numérica por categoría.
    Convierte automáticamente la columna a numérica si no lo es y elimina NaN.
    """
    # Convertir a numérico si es necesario
    df[numerical_col] = pd.to_numeric(df[numerical_col], errors='coerce')

    # Eliminar filas con NaN en la columna numérica
    df_clean = df.dropna(subset=[numerical_col])

    # Agrupar y calcular promedio
    grouped_data = df_clean.groupby(categorical_col)[numerical_col].mean()

    # Graficar
    fig, ax = plt.subplots(figsize=(8, 4))
    grouped_data.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel(numerical_col)
    ax.set_xlabel(categorical_col)
    ax.set_title(f"{numerical_col} promedio por {categorical_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# %%
def analisis_univariante(df_mundo_economics, plot_categorical_numerical_relationship, plot_grouped_boxplots):

    def plot_categorical_numerical_relationship(df_mundo_economics, categorical_col, numerical_col):
        
        # Convertir a numérico si es necesario
        df_mundo_economics[numerical_col] = pd.to_numeric(df_mundo_economics[numerical_col], errors='coerce')

        # Eliminar filas con NaN en la columna numérica
        df_clean = df_mundo_economics.dropna(subset=[numerical_col])

        # Agrupar y calcular promedio
        grouped_data = df_clean.groupby(categorical_col)[numerical_col].mean()

        # Graficar
        fig, ax = plt.subplots(figsize=(8, 4))
        grouped_data.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel(numerical_col)
        ax.set_xlabel(categorical_col)
        ax.set_title(f"{numerical_col} promedio por {categorical_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    

    # === Clasificación de variables ===
    numericas = ['Nota Global', 'Presupuesto', 'Acogida', 'Comunicacion',
       'Cultura', 'Affluencia turistica', 'Gastronomia', 'Hoteles', 'Paisajes',
       'Limpieza', 'Seguridad', 'Tranquilidad', 'Transportes', 'Ciudades',
       'PIB (U.S. dollars)', 'Ahorro nacional bruto (% de PIB)',
       '% Inflacion anual', 'Poblacion (Millones)', 'Inversion (% de PIB)',
       '% paro', 'top 50 restaurantes', 'Nota gastronomica', 'Ranking Gastronomico',
       'Platos en top 100', 'Indice de Criminalidad', 'Indice de Seguridad',
       'Ranking Corrupcion', 'Indice de Corrupcion', 'Ranking amabilidad',
       'Ranking facilidad de adaptación', 'Ranking bienvenida calurosa',
       'Ranking amigos locales', 'Ranking facilidad amigos',
       'Numero de turistas', 'Numero de camas', 'Numero de hoteles',
       'Numero de habitaciones', 'Ratio de ocupacion',
       'Numero de personas en sector turismo', '% poblacion en turismo',
       'Total English speakers', '% personas que hablan ingles',
       'Total Km carreteras',
       'muertes en carretera por cada 100.000 habitantes',
       'muertes en carretera por cada 100.000 vehiculos',
       'Total fallecidos al año']

    df_mundo_economics = preparar_regiones(df_mundo_economics)

    # === Agrupación descriptiva ===
    df_grouped = df_mundo_economics.groupby("Region").describe()
    print(df_grouped)

    # === Histogramas comparativos ===
    vars_to_plot = [
        "Nota Global", "PIB (U.S. dollars)", "% personas que hablan ingles", "% poblacion en turismo",
        "Presupuesto", "Acogida", "Cultura", "Gastronomia", "Paisajes", "Seguridad",
        "Transportes", "Ciudades", "Limpieza", "Hoteles", "Affluencia turistica"
    ]

    for var in vars_to_plot:
        plot_categorical_numerical_relationship(df_mundo_economics, "Region", var)

    # === Texto explicativo ===
    print("""
    ### Análisis Regional Turístico

    **Nota Global:** En general, respecto a la nota global, Oceanía resulta más atractiva para los turistas, con Latinoamérica (LA) y el Sudeste Asiático (SA) bastante cerca, y China en último lugar.
    **PIB:** Como era de esperar, China supera por mucho el PIB de las otras tres regiones. El Sudeste Asiático ocupa la última posición con un valor de 4.96e+05.
    **Dominio del Inglés:** En cuanto al dominio del idioma inglés, el 94% de la población en Oceanía lo habla, lo cual es lógico teniendo en cuenta que solo se recopilan datos de Australia y Nueva Zelanda. Sin embargo, existe una gran diferencia entre LA y SA: el 35% de la población del Sudeste Asiático habla inglés, frente al 6.3% en Latinoamérica, lo cual indica una mayor preparación para el turismo en la región asiática.
    **Personal Turístico:** Estos datos también se reflejan en el porcentaje de personas dedicadas al turismo, donde el Sudeste Asiático registra un 5.3% frente al 3% de Latinoamérica.
    **Presupuesto:** En cuanto al gasto medio para turistas, resulta mucho más económico viajar a SA o LA (8/10) que a Oceanía (5.3/10).
    **Acogida:** China es la región que peor acogida ofrece al turista (6.7/10), mientras que las otras tres regiones superan los 8 puntos, mostrando una recepción generalmente buena.
    **Cultura:** Los turistas suelen puntuar positivamente las cuatro regiones en términos culturales, siendo Oceanía ligeramente inferior al resto.
    **Gastronomía:** No ocurre lo mismo en gastronomía, donde Oceanía vuelve a situarse en el último lugar. La cabeza está muy disputada entre China y el Sudeste Asiático, seguidos de cerca por Latinoamérica.
    **Paisajes:** La situación se invierte en cuanto a paisajes, donde Oceanía y Latinoamérica ocupan los primeros puestos con puntuaciones de 9.35/10 y 9.2/10, respectivamente.
    **Seguridad:** En términos de seguridad, Oceanía destaca con un 9.3/10, muy por encima de Latinoamérica (7.1), situándose China (8.9) y SA (8.3) en valores intermedios.
    **Transportes:** En promedio, las infraestructuras de transporte de los países desarrollados de Oceanía y China obtienen una ligera mejor nota que las de Latinoamérica y SA.
    **Ciudades:** Las ciudades del Sudeste Asiático parecen ser las menos valoradas por los turistas, mientras que las de las otras tres regiones obtienen puntuaciones más altas y equilibradas.
    **Limpieza:** En términos de limpieza, Oceania supera en mas de 2 puntos a las otras tres regiones. Sin embargo, esta puntuación se iguala muchísimo en la valoración de los hoteles en general.
    **Afluencia Turística:** Las regiones mejor valoradas en cuanto a poca afluencia turística y por lo tanto mas cómodos de visitar son Oceania y Latinoamérica, con gran diferencia respecto al sudeste asiatico y China.
    """)

    # === Boxplot general por región ===
    plot_grouped_boxplots(df_mundo_economics, "Region", "Nota Global")

    # === Barplot por país ===
    sns.barplot(data=df_mundo_economics, x="Pais", y="Nota Global", estimator='mean')
    plt.xticks(rotation=90)
    plt.legend(fontsize=3)
    plt.show()

    print("""
    Los países mejor valorados en nota global son Malasia, Nueva Zelanda y Colombia.
    Los menos valorados: China, Camboya y Filipinas.
    """)

# %% [markdown]
# 


