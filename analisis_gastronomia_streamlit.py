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
from analisis_gastronomia import *
from streamlit_folium import st_folium

# %%
#GASTRONOMICO>>>>>>>
def analisis_gastronomia_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis de Gastronomía", layout="wide")
    st.title("🍽️ Análisis de Gastronomía y Rankings por País")

    # Cargar y preparar datos
    df_comida = data_frame_comida(df_mundo_economics)
    st.subheader("Tabla de Gastronomía y Rankings por País")
    st.dataframe(df_comida)

    # Gráfico opinión turistas
    st.subheader("Opinión de turistas sobre gastronomía")
    fig1 = plot_comida1(df_comida)
    st.pyplot(fig1)
    st.markdown("""
    **Análisis:**  
    - Tailandia, Vietnam y Colombia son los países mejor valorados por los turistas.
    """)

    # Gráficos comparativos
    df_melt_comida2, df_melt1_comida2 = data_frame_comida2(df_comida)
    st.subheader("Gráficos comparativos de gastronomía")
    fig2 = plot_comida2(df_melt_comida2, df_melt1_comida2)
    st.pyplot(fig2)
    st.markdown("""
    **Análisis:**  
    #Aqui vemos las cuatro categorias de gastronomia. México, Indonesia y China son las mejores gastronomias según TasteAtlas.
    # En cuanto a restaurantes de calidad, Australia, Perú y México ocupan el top 3.

    #En la grafica de la izquierda vemos en azul la cantidad de platos de una gastronomia en el top 100. China sobresale con 8 seguido de Indonesia y México.
    #En cuanto a la nota gastronomica, los mismos tres paises ocupan el top 3. 
    """)

    # Heatmap correlaciones
    st.subheader("Matriz de Correlación")
    corr_matrix_comida1, fig_heat_comida1 = plot_comida3_heatmap(df_comida)
    st.dataframe(corr_matrix_comida1.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat_comida1)
    st.markdown("""
    **Observaciones:**  
    #Vemos que la mayor correlación existe entre Nota gastronomica y el ranking de puntos (ranking de paises con mejores gastronomias). 
    #Igualmente la opinión de los turistas (Columna Gastronomia) presenta una correlación del 0.43 respecto al ranking de paises con mejor gastronomia.
    #El PIB total de un pais parece influir positivamente en la gastronomia de un pais, como se ve reflejado en su correlación con las notas gastronomicas y el ranking de gastronomias. 
    #Sin embargo, no existe una fuerte correlación entre la opinión de los turistas y los paises que poseen restaurantes top, ni tampoco con la riqueza de un pais (PIB).
    #Igualmente existe una correlación entre el numero de platos en el top100 y el ranking de puntos y sobre todo con el PIB (0.8)
    """)

    # Eliminamos outlier Camboya
    df_comida1 = df_comida.drop(index=[16])
    st.subheader("Relación Opinión de turistas vs Nota gastronómica (sin outliers)")
    fig3_comida, corr3_comida, pval3_comida = plot_comida4_lm(df_comida1, "Gastronomia", "Nota gastronomica")
    st.pyplot(fig3_comida)
    st.markdown(f"""
    **Correlación de Pearson:** {corr3_comida:.2f}  
    **p-valor:** {pval3_comida:.4f}  
    **Análisis:**  
    #Vemos que camboya parece ser un outlayer en terminos de gastronomia. 
    #Aunque conocemos la nota de los turistas (7.4) la nota gastronomica esta trucada y no tiene ni restaurantes en el top 50 ni ranking gastronomico.
    """)

    # Relación PIB vs Gastronomía (sin outliers)
    df_comida1 = df_comida1.drop(index=[9])  # Eliminamos China
    st.subheader("Relación Opinión de turistas vs PIB (sin China)")
    fig4_comida, corr4_comida, pval4_comida = plot_comida4_lm(df_comida1, "Gastronomia", "PIB (U.S. dollars)")
    st.pyplot(fig4_comida)
    st.markdown(f"""
    **Correlación de Pearson:** {corr4_comida:.2f}  
    **p-valor:** {pval4_comida:.4f}  
    **Análisis:** 
    #Miramos ahora el PIB con respecto al indice gastronomico, sabemos que China tiene un PIB "anormalmente" grande, que puede ser considerado como outlayer. Lo vemos 
    - Sin China, tampoco se aprecia correlación clara entre opinión de turistas y PIB.
    """)

    # Nueva matriz de correlación tras eliminar outliers
    st.subheader("Matriz de Correlación (sin outliers)")
    corr_matrix2_comida, fig_heat2_comida = plot_comida3_heatmap(df_comida1)
    st.dataframe(corr_matrix2_comida.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat2_comida)
    st.markdown("""
    **Observaciones:**  
    #Observamos que las correlacciones son mejores en general, con un 0.98 entre nota gastronómica 
    #y ranking y una mayor correlación entre numero de restaurantes en el top 50 y el PIB. 
    #También la opinión de los turistas esta mas correlacionada con las notas y el ranking dados por atlasweb, aunque sigue sin haberla resepcto a los restaurantes top y el PIB
    """)

    # Pairplot
    st.subheader("Pairplot de variables gastronómicas")
    fig_pair = sns.pairplot(df_comida1[df_comida1.columns.to_list()[1:]], diag_kind="hist", diag_kws={"bins":10})
    st.pyplot(fig_pair.figure)

    # Correlaciones Pearson individuales
    st.subheader("Correlaciones individuales")
    cols_to_test_gastronomia = ["Nota gastronomica", "top 50 restaurantes", "Platos en top 100", "Ranking puntos"]
    for col in cols_to_test_gastronomia:
        corr_val_comida, pval_val_comida = pearsonr(df_comida1["Gastronomia"], df_comida1[col])
        st.markdown(f"- **Gastronomia vs {col}:** Corr={corr_val_comida:.2f}, p-valor={pval_val_comida:.4f}")

    st.markdown("""
    **Conclusiones:**  
    #Los p valores que relacionan las opiniones de los turistas con variables gastronomicas son bastante elevados. 
    #Solo la nota gastronómica y el ranking de gastronomias esta por debajo de 0.05 y podemos afirmar que existe una correlación. 
    #En cuanto al numero de restaurantes top y el numero de platos top, no podemos afirmar que exite correlación, quizas debido a la baja cantidad de datos y a que muchos paises no presentan ni platos ni restaurantes en el top, y esos valores 0 otorgados pesan mucho.
    """)


