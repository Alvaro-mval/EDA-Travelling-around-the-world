# %%
import streamlit as st
import pandas as pd
from scipy.stats import pearsonr
from analisis_transportes import *

# %%
#TRANSPORTES>>>>>>>>>>>
def analisis_transportes_streamlit(df_mundo_economics):
    # st.set_page_config(page_title="Análisis de Transportes", layout="wide")
    st.title("🚗 Análisis de Transporte y Seguridad Vial por País")

    # --- Carga y preparación ---
    df_transportes = data_frame_transportes(df_mundo_economics)
    st.subheader("Tabla de Transporte por País")
    st.dataframe(df_transportes)

    # --- Barras individuales ---
    st.subheader("Nivel de Transporte por País")
    fig_transporte = plot_transportes_bar(df_transportes, "Pais", "Transportes", "Opinión sobre el Transporte por País")
    st.pyplot(fig_transporte)

    st.subheader("Total de Fallecidos al Año")
    fig_fallecidos = plot_transportes_bar(df_transportes, "Pais", "Total fallecidos al año", "Total de Fallecidos al Año por País")
    st.pyplot(fig_fallecidos)

    st.markdown("""
    **Observaciones:**  
    - En términos de transporte, muchos países comparten los primeros puestos (Malasia, Argentina, China, Nueva Zelanda, Australia…).  
    - Sin embargo, vemos países donde el transporte es mucho peor que la media, como Bolivia, Laos, Camboya o Filipinas.  
    - En cuanto a las muertes totales en carretera, claramente está condicionado por la población total de los países, con China, Indonesia y Brasil ocupando los primeros puestos.
    """)

    # --- Gráficos comparativos ---
    st.subheader("Carreteras, PIB y Mortalidad Vial")
    fig_melt_transportes = plot_transportes_melt(df_transportes)
    st.pyplot(fig_melt_transportes)

    st.markdown("""
    **Observaciones:**  
    - El PIB está intrínsecamente relacionado con el número total de km de carretera, aunque también se podría vincular al tamaño del país y número de habitantes.  
    - Los países más pobres (Camboya, Bolivia y Laos) son los que menos kilómetros de carretera tienen.  
    - En la gráfica derecha, relacionamos muertes en carretera por vehículo y por habitante.  
    - Los países pobres como Bolivia y Camboya ocupan los primeros puestos.  
    - Es curioso ver a China tan arriba en cuanto a muertes por vehículo siendo un país “rico” con alto PIB y bastantes carreteras.  
    - Otros países montañosos como Perú y Colombia también aparecen arriba en el ranking de más muertes.  
    - En muertes por habitante, Tailandia y Vietnam lideran, quizás por el uso masivo de motos.
    """)

    # --- Heatmap inicial ---
    st.subheader("Matriz de Correlación (Con China)")
    corr_matrix_transportes, fig_heat_transportes = plot_transportes_heatmap(df_transportes)
    st.dataframe(corr_matrix_transportes.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat_transportes)

    # --- Lmplots con y sin China ---
    st.subheader("Relación entre Transporte y Km de Carretera")
    fig_lm1_transportes, corr1_transportes, pval1_transportes = plot_transportes_lm(df_transportes, "Transportes", "Total Km carreteras")
    st.pyplot(fig_lm1_transportes)
    st.markdown(f"- **Con China:** Corr={corr1_transportes:.2f}, p-valor={pval1_transportes:.4f}")

    st.markdown("""
    **Observación:**  
    Una vez más, China vuelve a ser un outlier en cuanto a PIB y km totales por carretera.  
    Suprimimos los datos de China y repetimos el análisis.
    """)

    df_transportes1 = df_transportes.drop(index=[9])
    fig_lm2_transportes, corr2_transportes, pval2_transportes = plot_transportes_lm(df_transportes1, "Transportes", "Total Km carreteras")
    st.pyplot(fig_lm2_transportes)
    st.markdown(f"- **Sin China:** Corr={corr2_transportes:.2f}, p-valor={pval2_transportes:.4f}")

    # --- Heatmap sin China ---
    st.subheader("Matriz de Correlación (Sin China)")
    corr_matrix2_transportes, fig_heat2_transportes = plot_transportes_heatmap(df_transportes1)
    st.dataframe(corr_matrix2_transportes.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat2_transportes)
    st.markdown("""
    **Observaciones:**  
    - Vemos correlaciones negativas al comparar la opinión de los turistas sobre el transporte con las muertes por habitante y muertes totales.  
    """)

    # --- Análisis detallado ---
    st.subheader("Relación entre Transporte y Mortalidad")
    fig_muertes1_transportes, corr3_transportes, pval3_transportes = plot_transportes_lm(df_transportes1, "Transportes", "muertes en carretera por cada 100.000 habitantes")
    st.pyplot(fig_muertes1_transportes)
    st.markdown("""
    Tailandia lidera el ranking de países con más muertes por habitante, y sin embargo está muy bien puntuado entre los turistas.
    """)

    fig_muertes2_transportes, corr4_transportes, pval4_transportes = plot_transportes_lm(df_transportes1, "Transportes", "Total fallecidos al año")
    st.pyplot(fig_muertes2_transportes)
    st.markdown("""
    Países con “pocos” fallecidos al año como Filipinas, Bolivia, Camboya y Laos tienen notas bajas.  
    Otros como Brasil, con más fallecidos, presentan notas altas.  
    La opinión de los turistas podría estar más influenciada por la comodidad del transporte que por la cifra real de accidentes.
    """)

    # --- Pairplot ---
    st.subheader("Pairplot de variables de Transporte")
    fig_pairplot = plot_pairplot_transportes(df_transportes1)
    st.pyplot(fig_pairplot.figure)

    # --- Correlaciones finales ---
    st.subheader("Correlaciones finales numéricas")
    corr_a_transportes = pearsonr(df_transportes1["Transportes"], df_transportes1["Total Km carreteras"])
    corr_b_transportes = pearsonr(df_transportes1["Transportes"], df_transportes1["muertes en carretera por cada 100.000 habitantes"])
    corr_c_transportes = pearsonr(df_transportes1["Transportes"], df_transportes1["muertes en carretera por cada 100.000 vehiculos"])
    corr_d_transportes = pearsonr(df_transportes1["Transportes"], df_transportes1["Total fallecidos al año"])

    st.markdown(f"""
    - **Transportes vs Km Carreteras:** Corr={corr_a_transportes[0]:.2f}, p-valor={corr_a_transportes[1]:.4f}  
    - **Transportes vs Muertes /100k hab.:** Corr={corr_b_transportes[0]:.2f}, p-valor={corr_b_transportes[1]:.4f}  
    - **Transportes vs Muertes /100k veh.:** Corr={corr_c_transportes[0]:.2f}, p-valor={corr_c_transportes[1]:.4f}  
    - **Transportes vs Total Fallecidos:** Corr={corr_d_transportes[0]:.2f}, p-valor={corr_d_transportes[1]:.4f}
    """)

    st.markdown("""
    **Conclusiones:**  
    - Los p-valores que relacionan las opiniones de los turistas con variables de transporte son bastante elevados.  
    - En ninguno de los parámetros podemos decir que haya una correlación entre la opinión de los turistas y la situación real del país en cuanto a transportes, accidentes y fallecimientos.
    """)


