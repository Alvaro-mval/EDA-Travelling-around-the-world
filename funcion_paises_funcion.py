# %%

import pandas as pd



df_mundo_economics = pd.read_csv('merge.csv', encoding='utf-8')
# %%
def preparar_datos_destinos(df_mundo_economics):
    """Prepara el dataframe con las columnas relevantes."""
    df_funcion = df_mundo_economics.loc[:, [
        "Pais", "Presupuesto", "Acogida", "Comunicacion", "Cultura",
        "Affluencia turistica", "Gastronomia", "Hoteles", "Paisajes",
        "Limpieza", "Seguridad", "Tranquilidad", "Transportes", "Ciudades"
    ]]
    df_funcion = df_funcion.rename(columns={'Affluencia turistica': 'Afluencia Turistica'})
    df_funcion = df_funcion.reset_index(drop=True)
    return df_funcion

# %%
def obtener_criterios():
    """Devuelve la lista de criterios disponibles."""
    return [
        "Presupuesto", "Acogida", "Comunicacion", "Cultura", "Afluencia Turistica",
        "Gastronomia", "Hoteles", "Paisajes", "Limpieza", "Seguridad",
        "Tranquilidad", "Transportes", "Ciudades"
    ]

# %%
def calcular_puntajes(df_funcion, criterios_elegidos):
    """Calcula las notas globales según los tres criterios más importantes del usuario."""

    # Ratio adaptado según si un criterio fue elegido o no
    def ratio(criterio):
        return 0.1233 if criterio in criterios_elegidos else 0.07

    # Cálculo ponderado
    df_funcion["Nota Global"] = (
        df_funcion["Presupuesto"] * ratio("Presupuesto") +
        df_funcion["Acogida"] * ratio("Acogida") +
        df_funcion["Comunicacion"] * ratio("Comunicacion") +
        df_funcion["Cultura"] * ratio("Cultura") +
        df_funcion["Afluencia Turistica"] * ratio("Afluencia Turistica") +
        df_funcion["Gastronomia"] * ratio("Gastronomia") +
        df_funcion["Hoteles"] * ratio("Hoteles") +
        df_funcion["Paisajes"] * ratio("Paisajes") +
        df_funcion["Limpieza"] * ratio("Limpieza") +
        df_funcion["Seguridad"] * ratio("Seguridad") +
        df_funcion["Tranquilidad"] * ratio("Tranquilidad") +
        df_funcion["Transportes"] * ratio("Transportes") +
        df_funcion["Ciudades"] * ratio("Ciudades")
    ).round(2)

    df_funcion_ordenado = df_funcion.sort_values("Nota Global", ascending=False)
    df_resultado = df_funcion_ordenado.loc[:, ["Pais", "Nota Global"]].reset_index(drop=True)
    df_resultado.index = df_resultado.index + 1
    return df_resultado.head(3)


