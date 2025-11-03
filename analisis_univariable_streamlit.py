# %%
import streamlit as st
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
from scipy.stats import pearsonr
from merge_df import df_mundo_economics
from analisis_univariable import *
from streamlit_folium import st_folium

# %%
#UNIVARIANTE>>>>>>>>
def analisis_univariante_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis Univariante", layout="wide")
    st.title("📊 Análisis Univariante por Región y País")

    # Preparar regiones
    df_mundo_economics = preparar_regiones(df_mundo_economics)

    # Variables a graficar
    vars_to_plot = [
        "Nota Global", "PIB (U.S. dollars)", "% personas que hablan ingles", "% poblacion en turismo",
        "Presupuesto", "Acogida", "Cultura", "Gastronomia", "Paisajes", "Seguridad",
        "Transportes", "Ciudades", "Limpieza", "Hoteles", "Affluencia turistica"
    ]

    st.subheader("📈 Promedios por Región")
    for var in vars_to_plot:
        fig = plot_categorical_numerical_relationship(df_mundo_economics, "Region", var)
        st.pyplot(fig)

    st.subheader("📝 Boxplot de Nota Global por Región")
    fig_box = plot_grouped_boxplots(df_mundo_economics, "Region", "Nota Global")
    st.pyplot(fig_box)

    st.subheader("🌍 Nota Global por País")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_mundo_economics, x="Pais", y="Nota Global", estimator='mean', ax=ax)
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    ### Análisis Regional Turístico

    **Nota Global:** Oceanía resulta más atractiva para los turistas, con Latinoamérica (LA) y Sudeste Asiático (SA) bastante cerca, y China en último lugar.  
    **PIB:** China supera por mucho el PIB de las otras regiones. SA ocupa la última posición.  
    **Dominio del Inglés:** Oceanía 94%, LA 6.3%, SA 35%.  
    **Personal Turístico:** SA registra 5.3% frente al 3% de LA.  
    **Presupuesto:** Viajar a SA o LA más económico que a Oceanía.  
    **Acogida:** China ofrece la peor acogida, mientras que las otras regiones superan 8/10.  
    **Cultura:** Las puntuaciones culturales son altas en todas las regiones.  
    **Gastronomía:** Oceanía en último lugar; China y SA disputadas.  
    **Paisajes:** Oceanía y Latinoamérica primeras posiciones.  
    **Seguridad:** Oceanía destaca con 9.3/10; LA 7.1, China 8.9, SA 8.3.  
    **Transportes:** Mejores notas en Oceanía y China.  
    **Ciudades:** SA peor valorada; otras regiones equilibradas.  
    **Limpieza:** Oceania +2 puntos sobre otras regiones.  
    **Afluencia Turística:** Mejor valorada en Oceanía y Latinoamérica.
    """)


