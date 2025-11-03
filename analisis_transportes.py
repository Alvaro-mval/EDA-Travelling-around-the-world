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
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

# %%
def data_frame_transportes(df_mundo_economics):
    df_transportes = df_mundo_economics.loc[:, [
        "Pais", "PIB (U.S. dollars)", "Transportes",
        "Total Km carreteras",
        "muertes en carretera por cada 100.000 habitantes",
        "muertes en carretera por cada 100.000 vehiculos",
        "Total fallecidos al año"
    ]]

    df_transportes["Total Km carreteras"] = pd.to_numeric(df_transportes["Total Km carreteras"], errors='coerce')
    df_transportes["muertes en carretera por cada 100.000 habitantes"] = pd.to_numeric(df_transportes["muertes en carretera por cada 100.000 habitantes"], errors='coerce')
    df_transportes["muertes en carretera por cada 100.000 vehiculos"] = pd.to_numeric(df_transportes["muertes en carretera por cada 100.000 vehiculos"], errors='coerce')
    df_transportes["Total fallecidos al año"] = pd.to_numeric(df_transportes["Total fallecidos al año"], errors='coerce')

    df_transportes = df_transportes.reset_index(drop=True)

    cols_int = [
        "Total Km carreteras",
        "muertes en carretera por cada 100.000 habitantes",
        "muertes en carretera por cada 100.000 vehiculos",
        "Total fallecidos al año"
    ]

    for col in cols_int:
        df_transportes[col] = pd.to_numeric(df_transportes[col], errors="coerce").round(0).astype("Int64")

    return df_transportes

# %%
def plot_transportes_bar(df_transportes, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_transportes, x=x_col, y=y_col, estimator='mean', ax=ax)
    ax.set_title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.tight_layout()
    return fig

# %%
def plot_transportes_melt(df_transportes):
    columnas = ["Total Km carreteras", "PIB (U.S. dollars)"]
    df_melt = df_transportes.melt(id_vars="Pais", value_vars=columnas,
                                  var_name="Variable", value_name="Valor")

    columnas1 = ["muertes en carretera por cada 100.000 habitantes",
                 "muertes en carretera por cada 100.000 vehiculos"]
    df_melt1 = df_transportes.melt(id_vars="Pais", value_vars=columnas1,
                                   var_name="Variable", value_name="Valor")

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    sns.barplot(data=df_melt, x="Pais", y="Valor", hue="Variable", ax=axes[0])
    axes[0].set_title("Carreteras y PIB")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)

    sns.barplot(data=df_melt1, x="Pais", y="Valor", hue="Variable", ax=axes[1])
    axes[1].set_title("Muertes por habitante y por vehículo")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)

    plt.tight_layout()
    return fig

# %%
def plot_transportes_heatmap(df_transportes):
    corr_matrix = df_transportes[df_transportes.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                cbar=True, square=True, linewidths=.5, ax=ax,annot_kws={"size": 5})
    ax.set_title("Matriz de Correlación")
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix, fig

# %%
def plot_transportes_lm(df_transportes, x_col, y_col):
    
    g = sns.lmplot(x=x_col, y=y_col, data=df_transportes, fit_reg=False, hue="Pais", height=2, aspect=1.5)

    if g._legend is not None:
        g._legend.set_title("País")
        for text in g._legend.get_texts():
            text.set_fontsize(3)

    corr, pval = pearsonr(df_transportes[x_col], df_transportes[y_col])
    return g.figure, corr, pval

# %%
def plot_pairplot_transportes(df_transportes):
    fig = sns.pairplot(df_transportes[df_transportes.columns.to_list()[1:]],
                       diag_kind="hist", diag_kws={"bins": 10})
    return fig


