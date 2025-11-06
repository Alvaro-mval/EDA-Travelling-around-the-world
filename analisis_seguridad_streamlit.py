# %%
import streamlit as st
import pandas as pd
from scipy.stats import pearsonr
from analisis_seguridad import *

# %%
#SEGURIDAD>>>>>>
def analisis_seguridad_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Análisis de Seguridad", layout="wide")
    st.title("🛡️ Análisis de Seguridad, Tranquilidad y Corrupción por País")

    # --- Carga y preparación ---
    df_seguridad = data_frame_seguridad(df_mundo_economics)
    st.subheader("Tabla de Seguridad por País")
    st.dataframe(df_seguridad)

    # --- Gráficos individuales ---
    st.subheader("Seguridad por País")
    fig_seguridad = plot_seguridad_bar(df_seguridad, "Pais", "Seguridad", "Nivel de Seguridad por País")
    st.pyplot(fig_seguridad)

    st.subheader("Tranquilidad por País")
    fig_tranquilidad = plot_seguridad_bar(df_seguridad, "Pais", "Tranquilidad", "Nivel de Tranquilidad por País")
    st.pyplot(fig_tranquilidad)

    st.markdown("""
    **Observaciones:**  
    - Claramente los países anglófonos (Australia y Nueva Zelanda) ocupan los primeros puestos tanto en seguridad como en tranquilidad.  
    - Brasil es claramente el país menos seguro mientras que los menos tranquilos son China y Vietnam.  
    - En general, las medias de seguridad y tranquilidad son más altas para países del sudeste asiático que para los países latinoamericanos.
    """)

    # --- Gráficos comparativos ---
    st.subheader("Índices de Criminalidad, Seguridad y Corrupción")
    fig_melt = plot_seguridad_melt(df_seguridad)
    st.pyplot(fig_melt)
    st.markdown("""
    **Observaciones:**  
    - Los países de Latinoamérica son, por lo general, más inseguros que los asiáticos.  
    - China aparece como el país más seguro y con menor índice de criminalidad.  
    - Al contrario, países latinos como Perú, Bolivia y Brasil tienen los índices de criminalidad más altos y de seguridad más bajos.  
    - En cuanto a corrupción son los países de Oceanía los que tienen índices más bajos, mientras que Camboya parece ser el país más corrupto, seguido por Bolivia y México.
    """)

    # --- Heatmap ---
    st.subheader("Matriz de Correlación")
    corr_matrix_seguridad, fig_heat_seguridad = plot_seguridad_heatmap(df_seguridad)
    st.dataframe(corr_matrix_seguridad.style.background_gradient(cmap="coolwarm"))
    st.pyplot(fig_heat_seguridad)
    st.markdown("""
    **Observaciones:**  
    - Observamos una moderada correlación entre seguridad y tranquilidad, igualmente que entre seguridad y PIB.  
    - Igualmente la sensación de inseguridad de los turistas parece ser correspondida con los datos reales de índices de seguridad y criminalidad.  
    - De igual manera, los índices de corrupción parecen estar ligados a la tranquilidad en los países y en menor medida a la corrupción.
    """)

    # --- Relaciones individuales ---
    st.subheader("Relaciones individuales entre variables de seguridad")
    pairs_to_plot_segu = [
        ("Seguridad", "Tranquilidad"),
        ("Seguridad", "Indice de Criminalidad"),
        ("Seguridad", "Indice de Seguridad"),
        ("Seguridad", "Indice de Corrupcion")
    ]

    for x_col, y_col in pairs_to_plot_segu:
        fig_lm_segu, corr_val_segu, pval_val_segu = plot_seguridad_lm(df_seguridad, x_col, y_col)
        st.pyplot(fig_lm_segu)
        st.markdown(f"- **{x_col} vs {y_col}:** Corr={corr_val_segu:.2f}, p-valor={pval_val_segu:.4f}")

    st.markdown("""
    **Conclusiones intermedias:**  
    - Vemos efectivamente una cierta correlación a la vista para las variables de seguridad y tranquilidad.  
    - Veamos ahora numéricamente donde parece no existir tal correlación con un p valor de 0.11.  
    - En el caso de la correlación sobre cómo se sienten de seguros los turistas y el índice de criminalidad/seguridad, sí observamos una correlación existente (p= 0.03).  
    - Vemos igualmente una clara correlación entre seguridad e índice de corrupción (p= 0.021).
    """)



    # --- Pairplot ---
    st.subheader("Pairplot de variables de seguridad")
    fig_pairplot_seguridad = plot_pairplot_seguridad(df_seguridad)
    st.pyplot(fig_pairplot_seguridad.figure)

    # --- Correlaciones finales ---
    st.subheader("Correlaciones adicionales")
    corr1 = pearsonr(df_seguridad["Seguridad"], df_seguridad["Ranking Corrupcion"])
    corr2 = pearsonr(df_seguridad["Tranquilidad"], df_seguridad["Indice de Criminalidad"])
    corr3 = pearsonr(df_seguridad["Tranquilidad"], df_seguridad["Indice de Seguridad"])
    corr4 = pearsonr(df_seguridad["Tranquilidad"], df_seguridad["Indice de Corrupcion"])

    st.markdown(f"""
    - **Seguridad vs Ranking Corrupción:** Corr={corr1[0]:.2f}, p-valor={corr1[1]:.4f}  
    - **Tranquilidad vs Índice de Criminalidad:** Corr={corr2[0]:.2f}, p-valor={corr2[1]:.4f}  
    - **Tranquilidad vs Índice de Seguridad:** Corr={corr3[0]:.2f}, p-valor={corr3[1]:.4f}  
    - **Tranquilidad vs Índice de Corrupción:** Corr={corr4[0]:.2f}, p-valor={corr4[1]:.4f}  
    """)

    st.markdown("""
    **Conclusiones finales:**  
    - Vemos también que la seguridad y el ranking de países más corruptos se relacionan con un p valor de 0.029.  
    - De igual forma, la tranquilidad parece estar más relacionada con la corrupción, y no así con los índices de criminalidad y seguridad.  
    - En conjunto, se observa que los países más tranquilos y seguros tienden a tener menores índices de corrupción y criminalidad.
    """)


