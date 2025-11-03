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
from funcion_paises_funcion import *
from streamlit_folium import st_folium

# %%
#FUNCION PAISES PREFERIDOS>>>>>
def funcion_destinos_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Destinos Turísticos Recomendados", layout="centered")

    st.title("🎯 Recomendador de Destinos Turísticos")
    st.markdown("""
    Selecciona los **tres criterios más importantes** para ti al viajar, y el sistema te mostrará los **destinos más adecuados** según tus preferencias.
    """)

    df_funcion = preparar_datos_destinos(df_mundo_economics)
    criterios = obtener_criterios()

    st.success("Datos cargados correctamente ✅")

    # === Selección de criterios ===
    st.subheader("✈️ Selecciona tus tres criterios más importantes:")
    crit1 = st.selectbox("Primer criterio", criterios, key="crit1")
    crit2 = st.selectbox("Segundo criterio", criterios, key="crit2")
    crit3 = st.selectbox("Tercer criterio", criterios, key="crit3")

    criterios_elegidos = [crit1, crit2, crit3]

    # === Botón de cálculo ===
    if st.button("🎯 Mostrar mis destinos ideales"):
        st.write(f"**Has elegido:** {', '.join(criterios_elegidos)}")
        resultado = calcular_puntajes(df_funcion, criterios_elegidos)
        st.subheader("🌟 Top 3 destinos recomendados:")
        st.dataframe(resultado, use_container_width=True)

        st.markdown("""
        ---
        **Interpretación:**
        - El ranking se basa en tus tres criterios principales.
        - Cada criterio tiene un peso mayor en el cálculo de la **Nota Global**.
        - Puedes cambiar tus criterios y recalcular en cualquier momento.
        """)


