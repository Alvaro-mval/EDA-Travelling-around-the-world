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
from analisis_ingles import *
from streamlit_folium import st_folium

# %%
#Ingles>>>>>
def analisis_ingles_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis de Inglés", layout="wide")
    st.title("🗣️ Análisis del Inglés y Comunicación Turística por País")

    # --- Preparación de datos ---
    df_ingles = data_frame_ingles1(df_mundo_economics)
    st.subheader("Tabla de Inglés por País")
    st.dataframe(df_ingles)

    # Gráficos individuales
    st.subheader("Comunicación Turista-Local por País y % de Personas que Hablan Inglés por País")
    fig1_plot_ingles = plot_ingles1(df_ingles)
    st.pyplot(fig1_plot_ingles)


    st.markdown("""
    **Observaciones:**  
    - Claramente los países anglófonos (Australia y Nueva Zelanda) ocupan los primeros puestos tanto en comunicación "turista-local" como en % de personas que hablan inglés.  
    - Más allá de eso, vemos una enorme diferencia entre China y el resto de países en ambos parámetros.  
    - Los países con mejor comunicación después de Oceanía son Malasia, Filipinas y Colombia.  
    - En general, el inglés está mucho más extendido en el sudeste asiático que en los países latinoamericanos.
    """)

    # Gráfico comparativo de Total English speakers vs PIB
    st.subheader("Total English Speakers y PIB por País")
    fig_melt_ingles = plot_ingles2(df_ingles)
    st.pyplot(fig_melt_ingles)
    st.markdown("""
    **Observaciones:**  
    - No hay una relación clara entre ser un país rico (PIB) y la cantidad de gente que habla inglés.  
    - Las razones pueden ser población total o motivos históricos, como en el caso de Filipinas.
    """)

    # Heatmap correlaciones
    st.subheader("Matriz de Correlación")
    fig_heat_ingles,corr_matrix_ingles = plot_ingles3(df_ingles)
    st.dataframe(corr_matrix_ingles.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat_ingles)
    st.markdown("""
    **Observaciones:**  
    - A priori, se observa correlación entre comunicación y PIB, y entre comunicación y % de personas que hablan inglés.  
    - Los países con más "cultura" tienden a tener menor % de personas que hablan inglés, lo que repercute negativamente en la comunicación.
    """)

    # Eliminamos outliers y analizamos relaciones
    df_ingles1 = df_ingles.drop(index=[9])  # Eliminamos China como outlier
    st.subheader("Relaciones individuales sin outliers")
    pairs_to_plot = [
        ("Comunicacion", "Cultura"),
        ("Comunicacion", "Affluencia turistica"),
        ("% personas que hablan ingles", "Affluencia turistica"),
        ("Comunicacion", "Total English speakers"),
        ("Comunicacion", "% personas que hablan ingles"),
        ("Comunicacion", "PIB log"),
        ("PIB (U.S. dollars)", "% personas que hablan ingles")
    ]

    for x_col, y_col in pairs_to_plot:
        fig_lm_ingles, corr_val_ingles, pval_val_ingles = plot_ingles4(df_ingles1, x_col, y_col)
        st.pyplot(fig_lm_ingles)
        st.markdown(f"- **{x_col} vs {y_col}:** Corr={corr_val_ingles:.2f}, p-valor={pval_val_ingles:.4f}")
    st.markdown("""
    **Conclusiones:**  
    - La única correlación clara es la nota de comunicación local-turista y el % de personas que hablan inglés en el país.  
    - No existe correlación significativa entre el PIB de un país y % de personas que hablan inglés, ni entre PIB y número total de hablantes de inglés.  
    - Tampoco parece haber correlación entre comunicación y cultura, ni entre comunicación/% hablantes de inglés y afluencia turística.
    """)

    # Pairplot
    st.subheader("Pairplot de variables de inglés")
    fig_pairplot_ingles = plot_pairplot_ingles(df_ingles1)
    st.pyplot(fig_pairplot_ingles)



