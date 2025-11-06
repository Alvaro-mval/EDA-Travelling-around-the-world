# %%
import streamlit as st
from mapa_paises_funcion import *
from streamlit_folium import st_folium

# %%
#MAPA PAISES>>>>>>>
def mapa_paises_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Mapa Interactivo de Países", layout="wide")

    st.title("🌍 Mapa Interactivo de Parámetros Turísticos")
    st.markdown("""
    Este mapa interactivo permite visualizar distintos **indicadores turísticos y económicos**
    por país.  
    Selecciona un parámetro en el menú desplegable para ver cómo varía geográficamente.
    """)


    df_mundo_economics = preparar_coordenadas(df_mundo_economics)
    st.success("Datos cargados y coordenadas añadidas correctamente ✅")

    # === Selector de parámetro ===
    columnas_parametros = obtener_parametros()
    parametro = st.selectbox("Selecciona el parámetro a visualizar:", columnas_parametros, index=0)

    # === Mostrar mapa ===
    mapa = crear_mapa(df_mundo_economics, parametro)
    st_data = st_folium(mapa, width=900, height=600)

    # === Texto explicativo ===
    st.markdown("---")
    st.markdown(f"""
    **Interpretación:**  
    Cada marcador representa un país.  
    Al hacer clic, se muestra su **valor de {parametro}** según los datos cargados.  
    Esto permite comparar visualmente la percepción turística y económica entre países.
    """)


