# %%
import streamlit as st
import pandas as pd
from analisis_acogida_streamlit import analisis_acogida_streamlit
from analisis_economico_streamlit import analisis_economico_streamlit
from analisis_gastronomia_streamlit import analisis_gastronomia_streamlit
from analisis_hospedaje_streamlit import analisis_hospedaje_streamlit
from analisis_ingles_streamlit import analisis_ingles_streamlit
from analisis_seguridad_streamlit import analisis_seguridad_streamlit
from analisis_transportes_streamlit import analisis_transportes_streamlit
from analisis_univariable_streamlit import analisis_univariante_streamlit
from mapa_paises_streamlit import mapa_paises_streamlit
from funcion_destinos_streamlit import funcion_destinos_streamlit

df_mundo_economics = pd.read_csv('merge.csv', encoding='utf-8')
# %%
st.set_page_config(page_title="Dashboard Turístico", layout="wide")
st.title("🌎 Dashboard de Análisis Turístico Internacional")

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8f4e3, #e6ccb2, #d5a67a);
    color: black;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar principal
st.sidebar.title("📊 Menú de Análisis")
opcion = st.sidebar.selectbox(
    "Selecciona un análisis para explorar:",
    [
        "Mapa Interactivo de Países",
        "Análisis Económico",
        "Análisis de Gastronomía",
        "Análisis de Hospedaje",
        "Análisis de Inglés",
        "Análisis de Seguridad",
        "Análisis de Transportes",
        "Análisis Univariante",
        "Análisis de Acogida",
        "Destinos Recomendados"
    ]
)

# Ejecutar bloque según la opción seleccionada
if opcion == "Mapa Interactivo de Países":
    mapa_paises_streamlit(df_mundo_economics)

elif opcion == "Análisis Económico":
    analisis_economico_streamlit(df_mundo_economics)

elif opcion == "Análisis de Gastronomía":
    analisis_gastronomia_streamlit(df_mundo_economics)

elif opcion == "Análisis de Hospedaje":
    analisis_hospedaje_streamlit(df_mundo_economics)

elif opcion == "Análisis de Inglés":
    analisis_ingles_streamlit(df_mundo_economics)

elif opcion == "Análisis de Seguridad":
    analisis_seguridad_streamlit(df_mundo_economics)

elif opcion == "Análisis de Transportes":
    analisis_transportes_streamlit(df_mundo_economics)

elif opcion == "Análisis Univariante":
    analisis_univariante_streamlit(df_mundo_economics)

elif opcion == "Análisis de Acogida":
    analisis_acogida_streamlit(df_mundo_economics)

elif opcion == "Destinos Recomendados":
    funcion_destinos_streamlit(df_mundo_economics)

# %%



