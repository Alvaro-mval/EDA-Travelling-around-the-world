# %%
import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from bootcampviztools import plot_categorical_relationship_fin, pinta_distribucion_categoricas, plot_grouped_histograms,\
    plot_grouped_boxplots, plot_combined_graphs, plot_categorical_numerical_relationship, bubble_plot,\
        grafico_dispersion_con_correlacion
from scipy.stats import chi2_contingency, mannwhitneyu
from scipy.stats import pearsonr

df_mundo_economics = pd.read_csv('merge.csv', encoding='utf-8')
# %%
def data_frame_acogida1(df_mundo_economics):

    df_acogida = df_mundo_economics.loc[:, ["Pais", "Acogida", "Ranking amabilidad", "Ranking facilidad de adaptación", "Ranking bienvenida calurosa","Ranking amigos locales","Ranking facilidad amigos"]]

    df_acogida["Ranking amabilidad"] = pd.to_numeric(df_acogida["Ranking amabilidad"], errors='coerce')
    df_acogida["Ranking facilidad de adaptación"] = pd.to_numeric(df_acogida["Ranking facilidad de adaptación"], errors='coerce')
    df_acogida["Ranking bienvenida calurosa"] = pd.to_numeric(df_acogida["Ranking bienvenida calurosa"], errors='coerce')
    df_acogida["Ranking amigos locales"] = pd.to_numeric(df_acogida["Ranking amigos locales"], errors='coerce')
    df_acogida["Ranking facilidad amigos"] = pd.to_numeric(df_acogida["Ranking facilidad amigos"], errors='coerce')

    #invertimos los rankings para que sea a mayor acogida/amabilidad un valor mas alto. 
    df_acogida["Ranking amabilidad"] = 100 - df_acogida["Ranking amabilidad"]
    df_acogida["Ranking facilidad de adaptación"] = 100 - df_acogida["Ranking facilidad de adaptación"]
    df_acogida["Ranking bienvenida calurosa"] = 100 - df_acogida["Ranking bienvenida calurosa"]
    df_acogida["Ranking amigos locales"] = 100 - df_acogida["Ranking amigos locales"]
    df_acogida["Ranking facilidad amigos"] = 100 - df_acogida["Ranking facilidad amigos"]

    return df_acogida

# %%
def plot_acogida1(df_acogida):
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(data=df_acogida, x="Pais", y="Acogida", estimator='mean', ax=ax)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return fig

#Los datos de acogida suelen ser buenos en general salvo excepciones como Bolivia y China.
#No parece haber una tendencia clara entre Oceania, latinoamerica y sudeste asiatico con paises mejor y peor puntuados.
#El pais con mejor nota de acogida es Colombia seguido de Indonesia

# %%
def data_frame_acogida2(df_acogida):
    """
    Prepara los DataFrames transformados para las visualizaciones de acogida.
    Devuelve df_melt y df_melt1 listos para plot_acogida2.
    """
    # Primer grupo de columnas
    columnas = ["Ranking amabilidad", "Ranking facilidad de adaptación", "Ranking bienvenida calurosa"]
    df_melt_acogida2 = df_acogida.melt(
        id_vars="Pais",
        value_vars=columnas,
        var_name="Variable",
        value_name="Valor"
    )

    # Segundo grupo de columnas
    columnas1 = ["Ranking amigos locales", "Ranking facilidad amigos"]
    df_melt1_acogida2 = df_acogida.melt(
        id_vars="Pais",
        value_vars=columnas1,
        var_name="Variable",
        value_name="Valor"
    )

    return df_melt_acogida2, df_melt1_acogida2

# %%
def plot_acogida2(df_melt_acogida2, df_melt1_acogida2):
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # --- Gráfico 1 ---
    sns.barplot(data=df_melt_acogida2, x="Pais", y="Valor", hue="Variable", ax=axes[0])
    axes[0].set_title("Amabilidad, adaptación y bienvenida")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
    axes[0].set_ylim(0, 125)

    # --- Gráfico 2 ---
    sns.barplot(data=df_melt1_acogida2, x="Pais", y="Valor", hue="Variable", ax=axes[1])
    axes[1].set_title("Facilidad para hacer amigos y amigos locales")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)

    plt.tight_layout()
    return fig

# %%
def plot_acogida4(df_acogida):
    corr_matrix_acogida1 = df_acogida[df_acogida.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(corr_matrix_acogida1, annot=True, fmt=".2f", cmap="coolwarm",
                cbar=True, square=True, linewidths=.5, ax=ax)
    ax.set_title('Matriz de Correlación')
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix_acogida1, fig

#Como comentamos, los rankings de amistad, bienvenida y adaptación parecen bastante correlacionados entre si. Algo menos esta el ranking de amabilidad y la nota de acogida de los turistas. 

# %%
# Pairplot

def plot_acogida5(df_acogida):
    
    fig = sns.pairplot(df_acogida[df_acogida.columns.to_list()[1:]],
                       diag_kind="hist", diag_kws={"bins": 10})
    return fig

# %%
def plot_acogida6(df_acogida):
    
    # --- Gráfico ---
    g = sns.lmplot(
        x="Acogida",
        y="Ranking amabilidad",
        data=df_acogida,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    
    if g._legend is not None:
        g._legend.set_title('País')
        for text in g._legend.get_texts():
            text.set_fontsize(3) 

    # --- Correlación de Pearson ---
    corr, pval = pearsonr(df_acogida["Acogida"], df_acogida["Ranking amabilidad"])

    return g.figure, corr, pval

# %%
def plot_acogida7(df_acogida):
    
    # --- Eliminamos los outliers ---
    df_acogida1 = df_acogida.drop(index=[3, 8, 10], errors="ignore")

    # --- Gráfico de dispersión ---
    g = sns.lmplot(
        x="Acogida",
        y="Ranking amabilidad",
        data=df_acogida1,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    if g._legend is not None:
        g._legend.set_title('País')
        for text in g._legend.get_texts():
            text.set_fontsize(3) 

    # --- Correlación de Pearson ---
    corr, pval = pearsonr(df_acogida1["Acogida"], df_acogida1["Ranking amabilidad"])

    return g.figure, corr, pval, df_acogida1

# %%
def plot_acogida8(df_acogida):
    
    # --- Gráfico de dispersión ---
    g = sns.lmplot(
        x="Acogida",
        y="Ranking bienvenida calurosa",
        data=df_acogida,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    if g._legend is not None:
        g._legend.set_title('País')
        for text in g._legend.get_texts():
            text.set_fontsize(3)

    # --- Correlación de Pearson ---
    corr, pval = pearsonr(df_acogida["Acogida"], df_acogida["Ranking bienvenida calurosa"])

    return g.figure, corr, pval

# %%
def plot_acogida9(df_acogida):
    
    # --- Eliminamos Chile ---
    df_acogida2 = df_acogida.drop(index=[2], errors="ignore")

    # --- Gráfico 1 ---
    g1 = sns.lmplot(
        x="Acogida",
        y="Ranking amigos locales",
        data=df_acogida2,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )
    if g1._legend is not None:
        g1._legend.set_title("País")
        for text in g1._legend.get_texts():
            text.set_fontsize(6)
    corr1, pval1 = pearsonr(df_acogida2["Acogida"], df_acogida2["Ranking amigos locales"])

    # --- Gráfico 2 ---
    g2 = sns.lmplot(
        x="Acogida",
        y="Ranking facilidad de adaptación",
        data=df_acogida2,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )
    if g2._legend is not None:
        g2._legend.set_title("País")
        for text in g2._legend.get_texts():
            text.set_fontsize(6)
    corr2, pval2 = pearsonr(df_acogida2["Acogida"], df_acogida2["Ranking facilidad de adaptación"])

    # --- Gráfico 3 ---
    g3 = sns.lmplot(
        x="Acogida",
        y="Ranking facilidad amigos",
        data=df_acogida2,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )
    if g3._legend is not None:
        g3._legend.set_title("País")
        for text in g3._legend.get_texts():
            text.set_fontsize(2)
    corr3, pval3 = pearsonr(df_acogida2["Acogida"], df_acogida2["Ranking facilidad amigos"])

    return (g1.figure, corr1, pval1), (g2.figure, corr2, pval2), (g3.figure, corr3, pval3), df_acogida2


