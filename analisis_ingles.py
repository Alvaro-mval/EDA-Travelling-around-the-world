# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import openpyxl
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from bootcampviztools import plot_categorical_relationship_fin, pinta_distribucion_categoricas, plot_grouped_histograms,\
    plot_grouped_boxplots, plot_combined_graphs, plot_categorical_numerical_relationship, bubble_plot,\
        grafico_dispersion_con_correlacion
from scipy.stats import chi2_contingency, mannwhitneyu
from scipy.stats import pearsonr
from merge_df import df_mundo_economics

# %%
def data_frame_ingles1(df_mundo_economics):
    df_ingles = df_mundo_economics.loc[:, ["Pais", "PIB (U.S. dollars)", "Comunicacion", "Cultura", 
                                           "Affluencia turistica","Total English speakers","% personas que hablan ingles"]]

    df_ingles = df_ingles.reset_index(drop=True)
    df_ingles["PIB log"]= round(np.log(df_ingles["PIB (U.S. dollars)"]),2)
    return df_ingles

# %%
def plot_ingles1(df_ingles):
   
    # Crear figura con dos subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    # --- Gráfico 1: Comunicación ---
    sns.barplot(data=df_ingles, x="Pais", y="Comunicacion", estimator='mean', ax=axes[0])
    axes[0].set_title("Comunicación Turista-Local por País")
    axes[0].tick_params(axis='x', rotation=45)

    # --- Gráfico 2: % que hablan inglés ---
    sns.barplot(data=df_ingles, x="Pais", y="% personas que hablan ingles", estimator='mean', ax=axes[1])
    axes[1].set_title("% de Personas que Hablan Inglés por País")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return fig

# %%
def plot_ingles2(df_ingles):
    columnas = ["Total English speakers","PIB (U.S. dollars)"]
    df_melt = df_ingles.melt(id_vars="Pais", value_vars=columnas,
                             var_name="Variable", value_name="Valor")

    fig, ax = plt.subplots(1, 1, figsize=(13, 5))
    sns.barplot(data=df_melt, x="Pais", y="Valor", hue="Variable", ax=ax)
    ax.set_title("Total English speakers y PIB por País")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.tight_layout()
    return fig

# %%
def plot_ingles3(df_ingles):
    corr_matrix = df_ingles[df_ingles.columns.to_list()[1:]].corr()

    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                cbar=True, square=True, linewidths=.5, ax=ax,annot_kws={"size": 5})
    ax.set_title('Matriz de Correlación')
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()

    return fig, corr_matrix

# %%
def plot_ingles4(df_ingles, x_col, y_col):

    # Crear gráfico
    g = sns.lmplot(
        x=x_col,
        y=y_col,
        data=df_ingles,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    # Ajustar leyenda
    if g._legend is not None:
        g._legend.set_title("País")
        for text in g._legend.get_texts():
            text.set_fontsize(3)

    # Calcular correlación
    corr, pval = pearsonr(df_ingles[x_col], df_ingles[y_col])

    return g.figure, corr, pval

# %%
def plot_pairplot_ingles(df_ingles1, diag_kind="hist", bins=10):
    
    cols = df_ingles1.columns.to_list()[1:]  # Excluye la primera columna si es no numérica/categoría
    g = sns.pairplot(
        df_ingles1[cols],
        diag_kind=diag_kind,
        diag_kws={"bins": bins}
    )
    g.figure.tight_layout()
    return g.figure


