import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def scatter_plot(df: pd.DataFrame, var: str, var_type: str, comparison: str | dict = "local", label_rot: str | float = "auto") -> plt.Figure:
    assert var_type in ["cont","cat"], "var_type doit être 'cont' ou 'cat'"
    df_copy = df.sort_values(var).copy()
    if comparison=="local":
        average = df_copy["Salaire de base 2025-2026"].mean()
        median = df_copy["Salaire de base 2025-2026"].median()
    else:
        average = comparison.get("mean",0)
        median = comparison.get("median",0)
    if isinstance(label_rot,str):
        if var_type=="cont":
            rotation = 0
        else:
            rotation = 90
    else:
        rotation = label_rot
    fig, ax = plt.subplots()
    sns.scatterplot(df_copy,x=var,y="Salaire de base 2025-2026",ax=ax)
    ax.axhline(average,color="Red",label="Moyenne")
    ax.axhline(median,color="Green",label="Médiane")
    ax.tick_params(axis="x",labelrotation=rotation)
    fig.legend()
    if rotation==0:
        fig.tight_layout()
    return fig


def mean_plot(df: pd.DataFrame, var: str, var_type: str, comparison: str | dict = "local", bins: int = 10, label_rot: str | float = "auto") -> plt.Figure:
    assert var_type in ["cont","cat"], "var_type doit être 'cont' ou 'cat'"
    df_copy = df.sort_values(var).copy()
    if comparison=="local":
        average = df_copy["Salaire de base 2025-2026"].mean()
    else:
        average = comparison.get("mean",0)
    if var_type=="cont":
        df_copy[var+" bin"] = pd.cut(df_copy[var],bins=bins,right=False,include_lowest=True).astype(str)
        categories = var+" bin"
    else:
        categories = var
    if isinstance(label_rot,str):
        if var_type=="cont":
            rotation = 0
        else:
            rotation = 90
    else:
        rotation = label_rot
    temp = df_copy[[categories,"Salaire de base 2025-2026","Nombre de joueuses"]].groupby(categories,observed=False,sort=False).agg({"Salaire de base 2025-2026": "mean", "Nombre de joueuses": "sum"}).reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(temp,x=categories,y="Salaire de base 2025-2026",ax=ax)
    ax.axhline(average,color="Red",label="Moyenne")
    ax2 = ax.twinx()
    sns.barplot(temp,x=categories,y="Nombre de joueuses",ax=ax2)
    for bar in ax2.containers[0]:
        bar.set_alpha(0.25)
    ax.set_xlabel(var)
    if var_type=="cont":
        ax.tick_params(axis="x",labelrotation=90)
    else:
        ax.tick_params(axis="x",labelrotation=rotation)
    fig.legend()
    if var_type!="cont" and rotation==0:
        fig.tight_layout()
    return fig


def median_plot(df: pd.DataFrame, var: str, var_type: str, comparison: str | dict = "local", bins: int = 10, label_rot: str | float = "auto") -> plt.Figure:
    assert var_type in ["cont","cat"], "var_type doit être 'cont' ou 'cat'"
    df_copy = df.sort_values(var).copy()
    if comparison=="local":
        median = df_copy["Salaire de base 2025-2026"].median()
    else:
        median = comparison.get("median",0)
    if var_type=="cont":
        df_copy[var+" bin"] = pd.cut(df_copy[var],bins=bins,right=False,include_lowest=True).astype(str)
        categories = var+" bin"
    else:
        categories = var
    if isinstance(label_rot,str):
        if var_type=="cont":
            rotation = 0
        else:
            rotation = 90
    else:
        rotation = label_rot
    temp = df_copy[[categories,"Salaire de base 2025-2026","Nombre de joueuses"]].groupby(categories,observed=False,sort=False).agg({"Salaire de base 2025-2026": "median", "Nombre de joueuses": "sum"}).reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(temp,x=categories,y="Salaire de base 2025-2026",ax=ax)
    ax.axhline(median,color="Red",label="Médiane")
    ax2 = ax.twinx()
    sns.barplot(temp,x=categories,y="Nombre de joueuses",ax=ax2)
    for bar in ax2.containers[0]:
        bar.set_alpha(0.25)
    ax.set_xlabel(var)
    if var_type=="cont":
        ax.tick_params(axis="x",labelrotation=90)
    else:
        ax.tick_params(axis="x",labelrotation=rotation)
    fig.legend()
    if var_type!="cont" and rotation==0:
        fig.tight_layout()
    return fig
