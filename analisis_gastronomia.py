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
def data_frame_comida(df_mundo_economics):
    df_comida = df_mundo_economics.loc[:, ["Pais", "Gastronomia", "PIB (U.S. dollars)", 
                                           "top 50 restaurantes", "Nota gastronomica", 
                                           "Ranking Gastronomico", "Platos en top 100"]].copy()
    df_comida = df_comida.reset_index(drop=True)
    
    # Invertimos el ranking gastronómico
    df_comida["Ranking puntos"] = 100 - df_comida["Ranking Gastronomico"]
    df_comida.loc[df_comida["Pais"] == "Camboya", "Ranking puntos"] = 0
    df_comida = df_comida.drop(columns=["Ranking Gastronomico"])
    
    return df_comida

# %%
def plot_comida1(df_comida):
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(data=df_comida, x="Pais", y="Gastronomia", estimator='mean', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title("Opinión de turistas sobre gastronomía por país")
    plt.tight_layout()
    return fig

# %%
def data_frame_comida2(df_comida):
    columnas = ["top 50 restaurantes", "Ranking puntos"]
    df_melt_comida2 = df_comida.melt(id_vars="Pais", value_vars=columnas, var_name="Variable", value_name="Valor")
    
    columnas1 = ["Platos en top 100", "Nota gastronomica"]
    df_melt1_comida2 = df_comida.melt(id_vars="Pais", value_vars=columnas1, var_name="Variable", value_name="Valor")
    
    return df_melt_comida2, df_melt1_comida2

# %%
def plot_comida2(df_melt_comida2, df_melt1_comida2):
    fig, axes = plt.subplots(1, 2, figsize=(12,6))
    
    sns.barplot(data=df_melt_comida2, x="Pais", y="Valor", hue="Variable", ax=axes[0])
    axes[0].set_title("Top 50 restaurantes y Ranking puntos")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
    
    sns.barplot(data=df_melt1_comida2, x="Pais", y="Valor", hue="Variable", ax=axes[1])
    axes[1].set_title("Platos en Top 100 y Nota gastronómica")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
    
    plt.tight_layout()
    return fig

# %%
def plot_comida3_heatmap(df_comida):
    corr_matrix = df_comida[df_comida.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, linewidths=.5, ax=ax,annot_kws={"size": 5})
    ax.set_title("Matriz de Correlación")
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix, fig

# %% [markdown]
# df_mundo_economics12 = pd.merge(df_mundo_economics11,df_carreteras1, how='left')
# df_mundo_economics = pd.merge(df_mundo_economics12,df_muertes_carreteras1, how='left')
# pd.set_option('display.max_columns', None)
# display(df_mundo_economics)

# %%
def plot_comida4_lm(df_comida, x_col, y_col):
    # Crear el gráfico y conservar el objeto FacetGrid
    g = sns.lmplot(
        x=x_col,
        y=y_col,
        data=df_comida,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    # Ajustar la leyenda
    if g._legend is not None:
        g._legend.set_title("País")         
        for text in g._legend.get_texts():   
            text.set_fontsize(3)   
    

    # Calcular correlación
    corr, pval = pearsonr(df_comida[x_col], df_comida[y_col])

    return g.figure, corr, pval


