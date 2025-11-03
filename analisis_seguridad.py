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
def data_frame_seguridad(df_mundo_economics):
    df_seguridad = df_mundo_economics.loc[:, [
        "Pais", "PIB (U.S. dollars)", "Seguridad", "Tranquilidad",
        "Indice de Criminalidad", "Indice de Seguridad",
        "Ranking Corrupcion", "Indice de Corrupcion"
    ]]
    df_seguridad = df_seguridad.reset_index(drop=True)

    df_seguridad["Indice de Corrupcion"] = pd.to_numeric(df_seguridad["Indice de Corrupcion"], errors='coerce')
    df_seguridad["Ranking Corrupcion"] = pd.to_numeric(df_seguridad["Ranking Corrupcion"], errors='coerce')

    return df_seguridad

# %%
def plot_seguridad_bar(df_seguridad, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_seguridad, x=x_col, y=y_col, estimator='mean', ax=ax)
    ax.set_title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig

# %%
def plot_seguridad_melt(df_seguridad):
    columnas = ["Indice de Criminalidad", "Indice de Seguridad"]
    df_melt = df_seguridad.melt(id_vars="Pais", value_vars=columnas,
                                var_name="Variable", value_name="Valor")

    columnas1 = ["Ranking Corrupcion", "Indice de Corrupcion"]
    df_melt1 = df_seguridad.melt(id_vars="Pais", value_vars=columnas1,
                                 var_name="Variable", value_name="Valor")

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    sns.barplot(data=df_melt, x="Pais", y="Valor", hue="Variable", ax=axes[0])
    axes[0].set_title("Índices de Criminalidad y Seguridad")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)

    sns.barplot(data=df_melt1, x="Pais", y="Valor", hue="Variable", ax=axes[1])
    axes[1].set_title("Ranking y Corrupción")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

    plt.tight_layout()
    return fig

# %%
def plot_seguridad_heatmap(df_seguridad):
    corr_matrix = df_seguridad[df_seguridad.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                cbar=True, square=True, linewidths=.5, ax=ax,annot_kws={"size": 5})
    ax.set_title('Matriz de Correlación')
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix, fig

# %%
def plot_seguridad_lm(df_seguridad, x_col, y_col):
    g = sns.lmplot(x=x_col, y=y_col, data=df_seguridad, fit_reg=False, hue="Pais", height=2, aspect=1.5)
    
    # Ajustar leyenda
    if g._legend is not None:
        g._legend.set_title("País")
        for text in g._legend.get_texts():
            text.set_fontsize(3)
    corr, pval = pearsonr(df_seguridad[x_col], df_seguridad[y_col])
    return g.figure, corr, pval

# %%
def plot_pairplot_seguridad(df_seguridad):
    fig = sns.pairplot(df_seguridad[df_seguridad.columns.to_list()[1:]],
                       diag_kind="hist", diag_kws={"bins": 10})
    return fig


