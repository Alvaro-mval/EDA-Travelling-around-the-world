# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df_mundo_economics = pd.read_csv('merge.csv', encoding='utf-8')

# %%
import warnings
warnings.filterwarnings("ignore")

# %%
# Primero dividir las variables por tipo, usando la función que programamos en los ejercicios
def card_tipo(df,umbral_categoria = 10, umbral_continua = 30):
    # Primera parte: Preparo el dataset con cardinalidades, % variación cardinalidad, y tipos
    df_temp = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad y porcentaje de variación de cardinalidad
    df_temp = df_temp.T # Como nos da los valores de las columnas en columnas, y quiero que estas sean filas, la traspongo
    df_temp = df_temp.rename(columns = {0: "Card", 1: "%_Card", 2: "Tipo"}) # Cambio el nombre de la transposición anterior para que tengan más sentido, y uso asignación en vez de inplace = True (esto es arbitrario para el tamaño de este dataset)

    # Corrección para cuando solo tengo un valor
    df_temp.loc[df_temp.Card == 1, "%_Card"] = 0.00

    # Creo la columna de sugerenica de tipo de variable, empiezo considerando todas categóricas pero podría haber empezado por cualquiera, siempre que adapte los filtros siguientes de forma correspondiente
    df_temp["tipo_sugerido"] = "Categorica"
    df_temp.loc[df_temp["Card"] == 2, "tipo_sugerido"] = "Binaria"
    df_temp.loc[df_temp["Card"] >= umbral_categoria, "tipo_sugerido"] = "Numerica discreta"
    df_temp.loc[df_temp["%_Card"] >= umbral_continua, "tipo_sugerido"] = "Numerica continua"
    # Ojo los filtros aplicados cumplen con el enunciado pero no siguen su orden y planteamiento

    return df_temp

# %%
#Vemos que en nuestro análisis todas las variables son de tipo Numérica continua, por lo tanto no haremos análisis categóricos.

card_tipo(df_mundo_economics)

# %%
numericas = ['Nota Global', 'Presupuesto', 'Acogida', 'Comunicacion',
       'Cultura', 'Affluencia turistica', 'Gastronomia', 'Hoteles', 'Paisajes',
       'Limpieza', 'Seguridad', 'Tranquilidad', 'Transportes', 'Ciudades',
       'PIB (U.S. dollars)', 'Ahorro nacional bruto (% de PIB)',
       '% Inflacion anual', 'Poblacion (Millones)', 'Inversion (% de PIB)',
       '% paro', 'top 50 restaurantes', 'Nota gastronomica', 'Ranking Gastronomico',
       'Platos en top 100', 'Indice de Criminalidad', 'Indice de Seguridad',
       'Ranking Corrupcion', 'Indice de Corrupcion', 'Ranking amabilidad',
       'Ranking facilidad de adaptación', 'Ranking bienvenida calurosa',
       'Ranking amigos locales', 'Ranking facilidad amigos',
       'Numero de turistas', 'Numero de camas', 'Numero de hoteles',
       'Numero de habitaciones', 'Ratio de ocupacion',
       'Numero de personas en sector turismo', '% poblacion en turismo',
       'Total English speakers', '% personas que hablan ingles',
       'Total Km carreteras',
       'muertes en carretera por cada 100.000 habitantes',
       'muertes en carretera por cada 100.000 vehiculos',
       'Total fallecidos al año']

# %%
def preparar_regiones(df_mundo_economics):
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Australia", "Nueva Zelanda"]), "Region"] = "Oceania"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["China"]), "Region"] = "China"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Argentina", "Mexico", "Brasil", "Colombia", "Peru", "Bolivia", "Chile"]), "Region"] = "Latinoamerica"
    df_mundo_economics.loc[df_mundo_economics["Pais"].isin(["Filipinas", "Indonesia", "Tailandia", "Vietnam", "Laos", "Malasia", "Camboya"]), "Region"] = "Sudeste asiatico"
    return df_mundo_economics

# %%
def plot_categorical_numerical_relationship(df, categorical_col, numerical_col):
    """
    Genera un barplot mostrando el valor promedio de una variable numérica por categoría.
    Convierte automáticamente la columna a numérica si no lo es y elimina NaN.
    """
    df_copy = df.copy()

    # Limpiar '%' y otros caracteres no numéricos
    df_copy[numerical_col] = df_copy[numerical_col].astype(str).str.replace('%','', regex=False)
    
    # Convertir a numérico, NaN si falla
    df_copy[numerical_col] = pd.to_numeric(df_copy[numerical_col], errors='coerce')

    # Eliminar filas con NaN
    df_clean = df_copy.dropna(subset=[numerical_col])

    # Agrupar y calcular promedio
    grouped_data = df_clean.groupby(categorical_col)[numerical_col].mean()

    # Graficar
    fig, ax = plt.subplots(figsize=(8, 4))
    grouped_data.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_xlabel(categorical_col)
    ax.set_ylabel(numerical_col)
    ax.set_title(f"{numerical_col} promedio por {categorical_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_grouped_boxplots(df, categorical_col, numerical_col):
    """Boxplot por categoría"""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x=categorical_col, y=numerical_col, ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# %% [markdown]
# 


