# %%
import streamlit as st
from analisis_hospedaje import *

# %%
#Hospedaje>>>>>
def analisis_hospedaje_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis de Hospedaje", layout="wide")
    st.title("🏨 Análisis de Hospedaje y Turismo por País")

    # Cargar y preparar datos
    df_hospedaje = data_frame_hospedaje(df_mundo_economics)
    st.subheader("Tabla de Hospedaje por País")
    st.dataframe(df_hospedaje)

    # Gráficos individuales
    st.subheader("Hoteles por País")
    fig_hoteles = plot_hospedaje_bar(df_hospedaje, "Pais", "Hoteles", "Número de Hoteles por País")
    st.pyplot(fig_hoteles)

    st.subheader("Aflluencia turística por País")
    fig_affluencia = plot_hospedaje_bar(df_hospedaje, "Pais", "Affluencia turistica", "Aflluencia Turística por País")
    st.pyplot(fig_affluencia)
    st.markdown("""
    **Observaciones:**  
    - Las notas de los hoteles suelen ser buenas en general, salvo para los casos de Bolivia y Filipinas.  
    - Los mejores puntuados son Indonesia y Tailandia.  
    - Los países con mayor nota de afluencia turística: Bolivia, Laos, Colombia y Malasia.  
    - Los países más masificados: China, Indonesia y sobre todo Tailandia.
    """)

    # Gráficos comparativos 2x2
    st.subheader("Variables de Hospedaje")
    fig_melt = plot_hospedaje_melt(df_hospedaje)
    st.pyplot(fig_melt)
    st.markdown("""
    **Observaciones:**  
    #Existe una correlación clara entre el numero de camas y habitaciones. En estos datos hay que tener en cuenta de igual manera la pobración local.
    #En este contexto, se entiende que Brasil o China esten en el top de numero de camas y habitaciones. 
    #Sin embargo, la afluencia turistica se refleja en paises como Colombia y Vietnam que son los paises con mas numero de hoteles. 
    #Paises menos turisticos como Bolivia o Camboya ocupan los ultimos puestos en las tres categorias (hoteles, habitaciones y camas)

    #Es curioso ver como Malasia, sin ser un destino predilecto de turismo, tiene el mayor % de la poblacion en ese sector (10%) seguido de Camboya, Laos y Peru
    #En cuanto al ratio de ocupación hotelera, los paises oceanicos se situan en las primeras posiciones junto con Colombia. 
    """)

    # Heatmap correlaciones
    st.subheader("Matriz de Correlación")
    corr_matrix_hospedaje, fig_heat_hospedaje = plot_hospedaje_heatmap(df_hospedaje)
    st.dataframe(corr_matrix_hospedaje.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat_hospedaje)
    st.markdown("""
    **Observaciones:**  
    #Existe obvias correlaciones entre numero de hoteles, habitaciones y camas 
    #De igual manera existe entre numer de camas/habitaciones y el numero de personas que trabajan en el sector turistico.
    #Tambien una correlacion negativa entre la afluencia turistica y la puntuacion de los hoteles por parte de los turistas. 
    #El ratio de ocupacion y la afluencia turistica tambien parecen ligeramente correlacionados.
    """)

    # Pairplot
    st.subheader("Pairplot de variables de hospedaje")
    fig_pairplot_hospedaje = plot_pairplot_hospedaje(df_hospedaje)
    st.pyplot(fig_pairplot_hospedaje.figure)

    # Análisis individual de relaciones
    st.subheader("Relaciones individuales entre variables")
    pairs_to_plot_hospedaje = [
        ("Affluencia turistica", "Hoteles"),
        ("Affluencia turistica", "Numero de turistas"),
        ("Affluencia turistica", "Numero de camas"),
        ("Affluencia turistica", "Numero de personas en sector turismo"),
        ("Affluencia turistica", "% poblacion en turismo"),
        ("Affluencia turistica", "Ratio de ocupacion"),
        ("Hoteles", "Ratio de ocupacion"),
        ("Hoteles", "Numero de personas en sector turismo"),
        ("Hoteles", "% poblacion en turismo"),
        ("Hoteles", "Numero de turistas"),
        ("Hoteles", "Numero de camas")
    ]

    for x_col, y_col in pairs_to_plot_hospedaje:
        fig_lm_hospedaje, corr_val_hospedaje, pval_val_hospedaje = plot_hospedaje_lm(df_hospedaje, x_col, y_col)
        st.pyplot(fig_lm_hospedaje)
        st.markdown(f"- **{x_col} vs {y_col}:** Corr={corr_val_hospedaje:.2f}, p-valor={pval_val_hospedaje:.4f}")

    st.markdown("""
    **Conclusiones:**  
    #Podria existir una ligera correlacion entre una mayor afluenciaturistica y el menor puntuaje de hoteles con un p valor de 0.078
    #Claramente existe una correlación entre el numero oficial de turistas y el mayor numero de camas/hoteles y un menor puntaje de afluencia turistica por parte de los turistas.
    #Sin embargo, cuando comparamos la afluencia turistica con las otras variables (Numero de personas en sector turismo,% poblacion en turismo y ratio de ocupacion hotelera)
    #no encontramos ninguna correlacion con p valores bastante altos.
    #Aqui podemos observar que no existe ninguna gran correlacion entre la nota otorgada a hoteles y variables hoteleras que a priori podrian tener cierta relacion.
    #La explicacion que podria ser que la nota de hoteles tiene mas que ver con otros parametros subjetivos dentro del hotel que al hecho de tener facilidad de encontrar hoteles. 
    """)


