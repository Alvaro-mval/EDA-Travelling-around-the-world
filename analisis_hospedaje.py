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
def data_frame_hospedaje(df_mundo_economics):
    df_hospedaje = df_mundo_economics.loc[:, ["Pais", "Affluencia turistica", "Hoteles", 
                                              "Numero de turistas", "Numero de camas",
                                              "Numero de hoteles","Numero de habitaciones",
                                              "Ratio de ocupacion","Numero de personas en sector turismo",
                                              "% poblacion en turismo"]].copy()
    
    cols_to_numeric = ["Numero de turistas","Numero de camas","Numero de hoteles",
                       "Numero de habitaciones","Ratio de ocupacion",
                       "Numero de personas en sector turismo","% poblacion en turismo"]
    
    for col in cols_to_numeric:
        df_hospedaje[col] = pd.to_numeric(df_hospedaje[col], errors='coerce')
        
    df_hospedaje = df_hospedaje.reset_index(drop=True)
    return df_hospedaje

# %%
def plot_hospedaje_bar(df_hospedaje, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10,4))
    sns.barplot(data=df_hospedaje, x=x_col, y=y_col, estimator='mean', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title(title)
    plt.tight_layout()
    return fig

# %%
def plot_hospedaje_melt(df_hospedaje):
    columnas = ["Numero de camas","Numero de habitaciones"]
    df_melt = df_hospedaje.melt(id_vars="Pais", value_vars=columnas, var_name="Variable", value_name="Valor")

    columnas1 = ["Numero de hoteles"]
    df_melt1 = df_hospedaje.melt(id_vars="Pais", value_vars=columnas1, var_name="Variable", value_name="Valor")

    columnas2 = ["% poblacion en turismo"]
    df_melt2 = df_hospedaje.melt(id_vars="Pais", value_vars=columnas2, var_name="Variable", value_name="Valor")

    columnas3 = ["Ratio de ocupacion"]
    df_melt3 = df_hospedaje.melt(id_vars="Pais", value_vars=columnas3, var_name="Variable", value_name="Valor")

    # Figura 2x2
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    
    sns.barplot(data=df_melt, x="Pais", y="Valor", hue="Variable", ax=axes[0][0])
    axes[0][0].set_title("Número de camas y habitaciones")
    axes[0][0].set_xticklabels(axes[0][0].get_xticklabels(), rotation=90)
    
    sns.barplot(data=df_melt1, x="Pais", y="Valor", hue="Variable", ax=axes[0][1])
    axes[0][1].set_title("Número de hoteles")
    axes[0][1].set_xticklabels(axes[0][1].get_xticklabels(), rotation=90)
    
    sns.barplot(data=df_melt2, x="Pais", y="Valor", hue="Variable", ax=axes[1][0])
    axes[1][0].set_title("% población en turismo")
    axes[1][0].set_xticklabels(axes[1][0].get_xticklabels(), rotation=90)
    
    sns.barplot(data=df_melt3, x="Pais", y="Valor", hue="Variable", ax=axes[1][1])
    axes[1][1].set_title("Ratio de ocupación")
    axes[1][1].set_xticklabels(axes[1][1].get_xticklabels(), rotation=90)
    
    plt.tight_layout()
    return fig

# %%
def plot_hospedaje_heatmap(df_hospedaje):
    corr_matrix = df_hospedaje[df_hospedaje.columns.to_list()[1:]].corr()
    fig, ax = plt.subplots(figsize=(7,7))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, linewidths=.5,ax=ax,annot_kws={"size": 5})
    ax.set_title("Matriz de Correlación")
    ax.set_yticklabels(ax.get_yticklabels(),rotation=45)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    plt.tight_layout()
    return corr_matrix, fig

# %%
def plot_pairplot_hospedaje(df_hospedaje):
    
    fig = sns.pairplot(
        df_hospedaje[df_hospedaje.columns.to_list()[1:]], 
        diag_kind="hist", 
        diag_kws={"bins": 10}
    )
    return fig

# %%
def plot_hospedaje_lm(df_hospedaje, x_col, y_col):
  
    g = sns.lmplot(
        x=x_col,
        y=y_col,
        data=df_hospedaje,
        fit_reg=False,
        hue="Pais",
        height=2,
        aspect=1.5
    )

    # --- Ajustar la leyenda ---
    if g._legend is not None:
        g._legend.set_title("País")          
        for text in g._legend.get_texts():   
            text.set_fontsize(3)             
       
    # --- Calcular correlación ---
    corr, pval = pearsonr(df_hospedaje[x_col], df_hospedaje[y_col])

    return g.figure, corr, pval


