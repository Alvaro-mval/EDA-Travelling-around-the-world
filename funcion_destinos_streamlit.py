# %%
import streamlit as st

from funcion_paises_funcion import *

# %%
#FUNCION PAISES PREFERIDOS>>>>>
def funcion_destinos_streamlit(df_mundo_economics):
    #st.set_page_config(page_title="Destinos Turísticos Recomendados", layout="centered")

    st.title("🎯 Recomendador de Destinos Turísticos")
    st.markdown("""
    Selecciona los **tres criterios más importantes** para ti al viajar, y el sistema te mostrará los **destinos más adecuados** según tus preferencias.
    """)

    df_funcion = preparar_datos_destinos(df_mundo_economics)
    criterios = obtener_criterios()

    st.success("Datos cargados correctamente ✅")

    # === Selección de criterios ===
    st.subheader("✈️ Selecciona tus tres criterios más importantes:")
    crit1 = st.selectbox("Primer criterio", criterios, key="crit1")
    crit2 = st.selectbox("Segundo criterio", criterios, key="crit2")
    crit3 = st.selectbox("Tercer criterio", criterios, key="crit3")

    criterios_elegidos = [crit1, crit2, crit3]

    # === Botón de cálculo ===
    if st.button("🎯 Mostrar mis destinos ideales"):
        st.write(f"**Has elegido:** {', '.join(criterios_elegidos)}")
        resultado = calcular_puntajes(df_funcion, criterios_elegidos)
        st.subheader("🌟 Top 3 destinos recomendados:")
        st.dataframe(resultado, use_container_width=True)

        st.markdown("""
        ---
        **Interpretación:**
        - El ranking se basa en tus tres criterios principales.
        - Cada criterio tiene un peso mayor en el cálculo de la **Nota Global**.
        - Puedes cambiar tus criterios y recalcular en cualquier momento.
        """)


