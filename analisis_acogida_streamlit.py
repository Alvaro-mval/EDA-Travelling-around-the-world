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
from analisis_acogida import *
from streamlit_folium import st_folium

# %%
#<<<<<<<<#ACOGIDA>>>>>>>>>>>
def analisis_acogida_streamlit(df_mundo_economics):
  #st.set_page_config(page_title="Análisis de Acogida", layout="wide")
  st.title("🌍 Análisis de Acogida y Rankings por País")


  df_acogida  = data_frame_acogida1(df_mundo_economics)

  st.subheader("Tabla de Acogida y Rankings por País")
  st.dataframe(data_frame_acogida1(df_mundo_economics))


  st.subheader("Gráfico de Acogida por País")
  fig1_acogida = plot_acogida1(df_acogida)
  st.pyplot(fig1_acogida)


  st.markdown("""
  **Análisis:**  
  - Los datos de acogida suelen ser buenos en general salvo excepciones como Bolivia y China.  
  - No parece haber una tendencia clara entre Oceania, Latinoamérica y Sudeste Asiático respecto a países mejor y peor puntuados.  
  - El país con mejor nota de acogida es Colombia, seguido de Indonesia.
  """)

  st.set_page_config(page_title="Análisis de Acogida", layout="wide")
  st.title("🌍 Análisis de Acogida y Relaciones entre Variables")

  df_melt_acogida2, df_melt1_acogida2 = data_frame_acogida2(df_acogida)

  st.subheader("Gráficos comparativos de acogida")
  fig2_acogida = plot_acogida2(df_melt_acogida2, df_melt1_acogida2)
  st.pyplot(fig2_acogida)


  st.markdown("""
  **Análisis:**  
  - En general, las tres variables están correlacionadas entre sí.  
  - Bolivia y Laos parecen ser los países menos amables, junto con China y Camboya.  
  - Colombia lidera en facilidad de adaptación y bienvenida, seguida de Indonesia y Filipinas.  
  - Australia destaca como el país con mayor amabilidad.  
  - Los peores países para hacer amigos parecen ser Brasil y Bolivia,  
    mientras que Colombia, México, Filipinas y Tailandia encabezan la facilidad para hacer amigos.
  """)

  st.title("🔢 Correlación entre variables de acogida")

  corr_matrix_acogida1, fig_heatmap_plot_acogida4 = plot_acogida4(df_acogida)

  st.dataframe(corr_matrix_acogida1.style.background_gradient(cmap="coolwarm"))


  st.subheader("Matriz de Correlación (HeatMap)")
  st.pyplot(fig_heatmap_plot_acogida4)
  st.markdown("""
  **Análisis:**  
  #Como comentamos, los rankings de amistad, bienvenida y adaptación parecen bastante correlacionados entre si. Algo menos esta el ranking de amabilidad y la nota de acogida de los turistas. 
  """)

  st.subheader("Relaciones entre Variables (Pairplot)")
  st.pyplot(plot_acogida5(df_acogida))


  st.set_page_config(page_title="Análisis de Amabilidad", layout="wide")
  st.title("💬 Relación entre Acogida y Ranking de Amabilidad")

  # Ejecutar la función
  fig_plot_acogida6, corr_plot_acogida6, pval_plot_acogida6 = plot_acogida6(df_acogida)

  # Mostrar gráfico
  st.subheader("Gráfico de dispersión")
  st.pyplot(fig_plot_acogida6)

  # Mostrar correlación
  st.markdown(f"""
  **Correlación de Pearson:** {corr_plot_acogida6:.2f}  
  **p-valor:** {pval_plot_acogida6:.4f}
  """)

  # Texto interpretativo
  st.markdown("""
  **Análisis:**  
  - Laos, Bolivia y Nueva Zelanda no aparecen en el ranking de amabilidad,  
    pero tienen buena nota en acogida, lo que los convierte en *outliers*.  
  - Podrían eliminarse en un análisis posterior para obtener una correlación más precisa.
  """)


  st.set_page_config(page_title="Análisis sin Outliers", layout="wide")
  st.title("💬 Relación entre Acogida y Ranking de Amabilidad (sin outliers)")

  # Ejecutar función
  fig_plot_acogida7, corr_plot_acogida7, pval_plot_acogida7, df_acogida1 = plot_acogida7(df_acogida)

  # Mostrar gráfico
  st.subheader("Gráfico sin outliers")
  st.pyplot(fig_plot_acogida7)

  # Mostrar resultados numéricos
  st.markdown(f"""
  **Correlación de Pearson:** {corr_plot_acogida7:.2f}  
  **p-valor:** {pval_plot_acogida7:.4f}
  """)

  # Comentario analítico
  st.markdown("""
  **Análisis:**  
  - Aun eliminando los outliers (Laos, Bolivia y Nueva Zelanda),  
    el valor p ≈ 0.2 sigue siendo demasiado alto para afirmar  
    que existe una correlación significativa entre la acogida  
    y el ranking de amabilidad.
  """)



  st.set_page_config(page_title="Análisis de Bienvenida Calurosa", layout="wide")
  st.title("🔥 Relación entre Acogida y Ranking de Bienvenida Calurosa")

  # Ejecutar la función
  fig_plot_acogida8, corr_plot_acogida8, pval_plot_acogida8 = plot_acogida8(df_acogida)

  # Mostrar gráfico
  st.subheader("Gráfico de dispersión")
  st.pyplot(fig_plot_acogida8)

  # Mostrar correlación
  st.markdown(f"""
  **Correlación de Pearson:** {corr_plot_acogida8:.2f}  
  **p-valor:** {pval_plot_acogida8:.4f}
  """)

  # Comentario analítico
  st.markdown("""
  **Análisis:**  
  - Se observa una **fuerte correlación positiva** entre la nota de acogida  
    de los turistas y el *ranking de bienvenida calurosa*.  
  - Los países con mejor percepción de acogida suelen ser también aquellos  
    donde los turistas reportan una bienvenida más cálida.
  """)


  st.set_page_config(page_title="Análisis Amistad y Adaptación", layout="wide")
  st.title("🌍 Relación entre Acogida y Facilidad de Hacer Amigos / Adaptación")

  # Ejecutar función
  graf1_plot_acogida9, graf2_plot_acogida9, graf3_plot_acogida9, df_acogida2 = plot_acogida9(df_acogida)

  # --- Mostrar Gráfico 1 ---
  st.subheader("Acogida vs Ranking amigos locales")
  st.pyplot(graf1_plot_acogida9[0])
  st.markdown(f"Correlación: {graf1_plot_acogida9[1]:.2f}, p-valor: {graf1_plot_acogida9[2]:.4f}")

  # --- Mostrar Gráfico 2 ---
  st.subheader("Acogida vs Ranking facilidad de adaptación")
  st.pyplot(graf2_plot_acogida9[0])
  st.markdown(f"Correlación: {graf2_plot_acogida9[1]:.2f}, p-valor: {graf2_plot_acogida9[2]:.4f}")

  # --- Mostrar Gráfico 3 ---
  st.subheader("Acogida vs Ranking facilidad amigos")
  st.pyplot(graf3_plot_acogida9[0])
  st.markdown(f"Correlación: {graf3_plot_acogida9[1]:.2f}, p-valor: {graf3_plot_acogida9[2]:.4f}")

  st.markdown("""
  **Análisis:**  
  - Existe cierta correlación entre 'Acogida' y 'Facilidad de adaptación' (p ≈ 0.05).  
  - No hay evidencia significativa de correlación entre 'Acogida' y 'Facilidad para hacer amigos locales'.  
  - Chile se elimina por ser un valor atípico que distorsiona la interpretación.
  """)


