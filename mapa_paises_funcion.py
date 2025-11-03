# %%
import folium
from folium import plugins 
import numpy as np          
import pandas as pd         
from streamlit_folium import st_folium

# %%
from merge_df import df_mundo_economics

# %%
def preparar_coordenadas(df_mundo_economics):
    """Añade columnas de latitud y longitud a cada país."""
    coordenadas = [
        (-36.534031, -65.708371), (-8.328507, -52.524777), (-30.913992, -71.165713),
        (-16.9111, -64.747245), (4.454379, -72.877128), (21.372343, -101.578096),
        (-6.699112, -76.836457), (-26.562118, 133.440443), (-43.629211, 171.108792),
        (34.040778, 100.367678), (20.121538, 102.298219), (-2.332454, 102.023558),
        (17.296928, 121.139136), (16.541012, 100.940730), (13.543676, 108.553142),
        (4.576173, 101.938473), (13.435875, 104.303494)
    ]
    df_mundo_economics['Latitud'] = [lat for lat, lon in coordenadas]
    df_mundo_economics['Longitud'] = [lon for lat, lon in coordenadas]
    df_mundo_economics['Nota Global'] = df_mundo_economics['Nota Global'].astype(str)
    return df_mundo_economics

# %%
def crear_mapa(df_mundo_economics, parametro):
    """Crea un mapa folium interactivo basado en el parámetro seleccionado."""
    mapa = folium.Map(location=[10, 20], zoom_start=2)

    # Título en HTML
    title_html = f'''
        <h3 align="center" style="font-size:20px"><b>{parametro} en destinos turísticos</b></h3>
    '''
    mapa.get_root().html.add_child(folium.Element(title_html))

    # Añadir marcadores por país
    for _, row in df_mundo_economics.iterrows():
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=f"{row['Pais']}: {row[parametro]}",
            icon=folium.Icon(color='orange', icon='plane', prefix='fa')
        ).add_to(mapa)
    return mapa

# %%
def obtener_parametros():
    """Lista de parámetros disponibles para visualizar en el mapa."""
    return [
        "Nota Global", "Presupuesto", "Acogida", "Comunicacion", "Cultura",
        "Affluencia turistica", "Gastronomia", "Hoteles", "Paisajes", "Limpieza",
        "Seguridad", "Tranquilidad", "Transportes", "Ciudades"
    ]


