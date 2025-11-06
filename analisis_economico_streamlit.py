# %%
import streamlit as st
from analisis_economico import *

# %%
#ECONOMICO>>>>>>>>>>>
def analisis_economico_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis Económico", layout="wide")
    st.title("💰 Análisis Económico y Turismo por País")

    # --- DataFrame base ---
    df_economico = data_frame_economico(df_mundo_economics)
    st.subheader("Tabla de Datos Económicos")
    st.dataframe(df_economico)

    # --- Presupuesto por país ---
    st.subheader("Presupuesto medio por país")
    fig_presupuesto = plot_economico(df_economico)
    st.pyplot(fig_presupuesto)
    st.markdown("""
    **Observaciones:**  #Vemos que mucha diferencia los paises de oceania son los mas caros de visitar. En el lado opuesto se encuentra Bolivia, Laos, Mexico y Peru. 
    """)

    # --- Gráficos económicos múltiples ---
    df_melt1_economico, df_melt2_economico, df_melt3_economico, df_melt4_economico = data_frame_economico_2(df_economico)
    st.subheader("Comparación de variables económicas")
    fig_multi = plot_economico2(df_melt1_economico, df_melt2_economico, df_melt3_economico, df_melt4_economico)
    st.pyplot(fig_multi)
    st.markdown("""
    **Observaciones:**  
    #En cuanto a las variables económicas, vemos que China es claramente la mejor opción para invertir en el sector turismo. Con un porcentaje bajo de paro, baja inflacción y alto % de inversion y ahorro. 
    #En general, el paro es bastante bajo en casi todos los paises, aunque algo mas bajo en el SA que en LA. 
    #Los % de ahorro e inversión tambien son algo mas altos en el sudeste asiatico, lo que da ideas de economias algo mejores que en latinoamerica. 
    #En caso de querer invertir en el sector turistico, paises mas inestables como Argentina, Bolivia y Laos parecen peores opciones con tasas de inflaccion que van hasta EL 22%.
    #Cualquiera de los otros destinos parece adecuado, incluso Tailandia presenta inflacción negativa.
    #Vemos tambien como el PIB esta intrinsecamente relaccionado con la población del pais. En este sentido, China, Indonesia, Brasil y Mexico se colocan en las primeras posiciones. 
    """)

    # --- Matriz de correlación ---
    st.subheader("Matriz de Correlación")
    corr_matrix_eco, fig_corr_eco = data_frame_economico3(df_economico)
    st.dataframe(corr_matrix_eco.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_corr_eco)
    st.markdown("""
    **Observaciones:**  
    #Vemos mucha correlacion entre % de ahorro e inversion, entre población y PIB, entre paro e inversión, etc
    #Sin embargo no parece que la opinión de los turistas sobre el presupuesto tenga relación con estas variables macroeconomicas.
    #Se podria ver alguna ligera correlación entre el resto de variables y la afluencia turistica pero las conclusiones tampoco son claras.
    """)

    # --- Scraping y merge costo de vida ---
    st.subheader("Datos de Costo de Vida")
    df_costo_vida = data_frame_economico4()
    fig_costo,df_economico_1 = data_frame_economico5(df_costo_vida, df_economico)
    st.dataframe(df_economico_1)

    # --- Índices de costo ---
    st.subheader("Índices de costo por país")
    st.pyplot(fig_costo)
    st.markdown("""
    **Observaciones:**  
    #Vemos que los paises mas caros son los dos de Oceania seguido de China y Malasia en cuanto a precios de restaurantes.
    #Para los indices de coste de vida y de comestibles la cosa se iguala mucho mas, aunque Australia y Nueva Zelanda siguen en cabeza, se reduce la brecha con los demas paises.
    #Vemos que los paises mas baratos son Bolivia e Indonesia
    """)

    # --- Pairplot ---
    st.subheader("Pairplot de variables económicas y costo de vida")
    fig_pairplot = plot_economico3(df_economico_1)
    st.pyplot(fig_pairplot.figure)
    st.markdown("""
    **Observaciones:**  
    - A simple vista, correlaciones claras entre PIB y población, ahorro e inversión.  
    - Variables de costo de vida más relacionadas con la percepción del presupuesto turístico.
    """)

    # --- Presupuesto vs costos ---
    st.subheader("Relación entre Presupuesto y Costos de Vida")
    figs_costos, corrs_costos = data_frame_economico6(df_economico_1)
    for i, fig in enumerate(figs_costos):
        st.pyplot(fig)
        st.markdown(f"**Correlación Presupuesto vs {corrs_costos[i][0]}:** {corrs_costos[i][1]:.2f}, p-valor: {corrs_costos[i][2]:.4f}")
    st.markdown("""
    **Observaciones:**  
    #Aqui vemos claramente como estas variables estan mucho mas relaccioandas con la opinion turistica, la correlación es alta ya que el p valor es bastante pequeño.
    """)


