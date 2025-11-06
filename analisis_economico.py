# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df_mundo_economics = pd.read_csv('merge.csv', encoding='utf-8')
# %%
def data_frame_economico(df_mundo_economics):
    """
    Prepara el DataFrame económico seleccionando columnas relevantes
    y convirtiendo a numérico donde corresponda.
    """
    df_economico = df_mundo_economics.loc[:, [
        "Pais", "Presupuesto", "Affluencia turistica", "PIB (U.S. dollars)",
        "Ahorro nacional bruto (% de PIB)", "% Inflacion anual",
        "Poblacion (Millones)", "Inversion (% de PIB)", "% paro"
    ]]

    cols_numeric = [
        "Ahorro nacional bruto (% de PIB)", "% Inflacion anual",
        "Poblacion (Millones)", "Inversion (% de PIB)", "% paro"
    ]

    for col in cols_numeric:
        df_economico[col] = pd.to_numeric(df_economico[col], errors='coerce')

    return df_economico.reset_index(drop=True)

# %%
def plot_economico(df_economico):
    
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(data=df_economico, x="Pais", y="Presupuesto", estimator='mean', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title("Presupuesto medio por país")
    plt.tight_layout()
    return fig

# %%
def data_frame_economico_2(df_economico):
    
    columnas1 = ["Ahorro nacional bruto (% de PIB)", "Inversion (% de PIB)", "% paro"]
    df_melt1_economico = df_economico.melt(id_vars="Pais", value_vars=columnas1,
                            var_name="Variable", value_name="Valor")

    columnas2 = ["% Inflacion anual"]
    df_melt2_economico = df_economico.melt(id_vars="Pais", value_vars=columnas2,
                            var_name="Variable", value_name="Valor")

    columnas3 = ["PIB (U.S. dollars)"]
    df_melt3_economico = df_economico.melt(id_vars="Pais", value_vars=columnas3,
                            var_name="Variable", value_name="Valor")

    columnas4 = ["Poblacion (Millones)"]
    df_melt4_economico = df_economico.melt(id_vars="Pais", value_vars=columnas4,
                            var_name="Variable", value_name="Valor")

    return df_melt1_economico, df_melt2_economico, df_melt3_economico, df_melt4_economico

# %%
def plot_economico2(df_melt1_economico, df_melt2_economico, df_melt3_economico, df_melt4_economico):
    """
    Grafica en un layout 2x2 las variables económicas
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    sns.barplot(data=df_melt1_economico, x="Pais", y="Valor", hue="Variable", ax=axes[0][0])
    axes[0][0].set_title("% de inversión, % de ahorro, % paro")
    axes[0][0].set_xticklabels(axes[0][0].get_xticklabels(), rotation=90)

    sns.barplot(data=df_melt2_economico, x="Pais", y="Valor", hue="Variable", ax=axes[0][1])
    axes[0][1].set_title("% Inflación anual")
    axes[0][1].set_xticklabels(axes[0][1].get_xticklabels(), rotation=90)

    sns.barplot(data=df_melt3_economico, x="Pais", y="Valor", hue="Variable", ax=axes[1][0])
    axes[1][0].set_title("PIB (U.S. dollars)")
    axes[1][0].set_xticklabels(axes[1][0].get_xticklabels(), rotation=90)

    sns.barplot(data=df_melt4_economico, x="Pais", y="Valor", hue="Variable", ax=axes[1][1])
    axes[1][1].set_title("Población (Millones)")
    axes[1][1].set_xticklabels(axes[1][1].get_xticklabels(), rotation=90)

    plt.tight_layout()
    return fig

# %%
def data_frame_economico3(df_economico):
    """
    Devuelve la matriz de correlación y la figura heatmap
    """
    corr_matrix = df_economico[df_economico.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(8,8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                cbar=True, square=True, linewidths=.5, ax=ax, annot_kws={"size": 5})
    ax.set_title("Matriz de correlación económica")
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix, fig

# %%
def data_frame_economico4(url="https://es.numbeo.com/coste-de-vida/clasificaciones-por-pa%C3%ADs", paises_seleccionados=None):
    """
    Web Scrapping del costo de vida y limpieza de nombres.
    """
    if paises_seleccionados is None:
        paises_seleccionados = ["Australia","Peru","Mexico","Brasil","Tailandia","Chile","Argentina","China","Colombia",
                                "Indonesia", "Bolivia", "Nueva Zelanda", "Laos","Filipinas", "Vietnam","Malasia", "Camboya"]
    
    r = requests.get(url)
    soup = bs(r.text, "lxml")

    Pais, Indice_Costo_Vida, Indice_comestibles, Indice_precios_restaurantes = [], [], [], []

    rows = soup.find_all("tr", attrs={"style": "width: 100%"})
    for item in rows:
        pais_tag = item.find(class_="cityOrCountryInIndicesTable")
        Pais.append(pais_tag.get_text(strip=True) if pais_tag else None)
        tds = item.find_all("td")
        Indice_Costo_Vida.append(float(tds[2].get_text(strip=True).replace(",", ".")) if len(tds)>2 else None)
        Indice_comestibles.append(float(tds[6].get_text(strip=True).replace(",", ".")) if len(tds)>6 else None)
        Indice_precios_restaurantes.append(float(tds[7].get_text(strip=True).replace(",", ".")) if len(tds)>7 else None)

    df_costo_vida = pd.DataFrame({
        "Pais": Pais,
        "Indice_Costo_Vida": Indice_Costo_Vida,
        "Indice_comestibles": Indice_comestibles,
        "Indice_precios_restaurantes": Indice_precios_restaurantes
    })

    df_costo_vida = df_costo_vida[df_costo_vida["Pais"].isin(paises_seleccionados)]
    df_costo_vida["Pais"] = df_costo_vida["Pais"].replace({'Perú': 'Peru','México': 'Mexico'})
    df_costo_vida = df_costo_vida.reset_index(drop=True)
    
    return df_costo_vida

# %%
def data_frame_economico5(df_costo_vida, df_economico):
    
    df_economico_1 = pd.merge(df_economico, df_costo_vida, how="left", on="Pais")
    df_economico_1 = df_economico_1.dropna(subset=["Indice_Costo_Vida"])  # eliminar países sin datos

    columnas = ["Indice_Costo_Vida", "Indice_comestibles", "Indice_precios_restaurantes"]
    df_melt = df_economico_1.melt(id_vars="Pais", value_vars=columnas, var_name="Variable", value_name="Valor")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df_melt, x="Pais", y="Valor", hue="Variable", ax=ax)
    ax.set_title("Índices de costo de vida por país")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()

    return fig, df_economico_1

# %%
def plot_economico3(df_economico_1):
    
    fig = sns.pairplot(
        df_economico_1[df_economico_1.columns.to_list()[1:]], 
        diag_kind="hist", 
        diag_kws={"bins": 10}
    )
    return fig

# %%
def data_frame_economico6(df_economico_1):
    
    figs = []
    correlaciones = []

    for col in ["Indice_Costo_Vida", "Indice_comestibles", "Indice_precios_restaurantes"]:
        
        # Crear el gráfico (guardamos el FacetGrid, no la figura directamente)
        g = sns.lmplot(
            x="Presupuesto",
            y=col,
            data=df_economico_1,
            fit_reg=False,
            hue="Pais",
            height=2,
            aspect=1.5
        )

        # Hacer la leyenda (índice de países) más pequeña
        if g._legend is not None:
            g._legend.set_title('País')
            for text in g._legend.get_texts():
                text.set_fontsize(3)  

        # Calcular correlación de Pearson
        corr, pval = pearsonr(df_economico_1["Presupuesto"], df_economico_1[col])
        correlaciones.append([col, corr, pval])
        
        # Agregar la figura al listado
        figs.append(g.figure)

    return figs, correlaciones


