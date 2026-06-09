import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(page_title="Sommaire",page_icon="📊")

st.title("Sommaire")
st.text("Cette page présente un sommaire à haut niveau des salaires de base de la LPHF.")

df = pd.read_csv("./data/PWHL_player_salaries_2025-2026.csv")
df.rename(columns={"Province de naissance": "Province/état de naissance"},inplace=True)
df["Âge"] = 2026-df["Année de naissance"]
df["Nombre de joueuses"] = 1

min_games = st.number_input("Nombre minimal de parties jouées lors de la saison régulière 2025-2026",min_value=0,max_value=20,step=5,help="Exclure les joueuses qui ont joué moins de X parties durant la saison régulière 2025-2026.")

df = df[df["Parties jouées"]>=min_games].copy()
GLOBAL_MEAN = df["Salaire de base 2025-2026"].mean()
GLOBAL_MEDIAN = df["Salaire de base 2025-2026"].median()
# GLOBAL_Q1 = df["Salaire de base 2025-2026"].quantile(0.25)
# GLOBAL_Q3 = df["Salaire de base 2025-2026"].quantile(0.75)
# GLOBAL_MIN = df["Salaire de base 2025-2026"].min()
# GLOBAL_MAX = df["Salaire de base 2025-2026"].max()

with st.container():
    st.subheader("Distribution du salaire de base dans toute la ligue")
    fig, ax = plt.subplots()
    sns.histplot(df,x="Salaire de base 2025-2026",shrink=0.8,ax=ax)
    ax.axvline(GLOBAL_MEAN,color="blue",label=f"Moyenne {GLOBAL_MEAN:,.2f} USD")
    ax.axvline(GLOBAL_MEDIAN,color="red",label=f"Médiane {GLOBAL_MEDIAN:,.2f} USD")
    ax.set_title("Distribution du salaire de base 2025-2026")
    ax.set_ylabel("Nombre de joueuses")
    ax.set_xticks([35000,45000,55000,65000,75000,85000,95000,105000,115000,125000])
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)

with st.container():
    st.subheader("Liste des joueuses")
    temp = df.sort_values("Salaire de base 2025-2026",ascending=False)
    temp[" "] = range(1,temp.shape[0]+1)
    temp.set_index(" ",drop=True,inplace=True)
    st.dataframe(temp[["Nom complet","Équipe","Salaire de base 2025-2026"]],column_config={"Salaire de base 2025-2026": st.column_config.NumberColumn(format="accounting")})

@st.fragment
def list_players(df: pd.DataFrame):
    """
    Fonction qui affiche la liste des joueuses d'une équipe sélectionnée
    
    Entrées
        df: données à utiliser
    """
    st.session_state.team = st.selectbox("Sélectionnez une équipe",options=np.sort(df["Équipe"].unique()),help="Lister les joueuses de l'équipe X.")
    temp = df[df["Équipe"]==st.session_state.team].sort_values("Salaire de base 2025-2026",ascending=False)
    temp[" "] = range(1,temp.shape[0]+1)
    temp.set_index(" ",drop=True,inplace=True)
    st.dataframe(temp[["Nom complet","Équipe","Salaire de base 2025-2026"]],column_config={"Salaire de base 2025-2026": st.column_config.NumberColumn(format="accounting")})

with st.container():
    st.subheader("Distribution du salaire de base par équipe")
    fig, ax = plt.subplots()
    sns.boxplot(df,x="Équipe",y="Salaire de base 2025-2026",ax=ax)
    ax.axhline(GLOBAL_MEAN,color="blue",linestyle="-",alpha=0.5,label=f"Moyenne")
    ax.axhline(GLOBAL_MEDIAN,color="red",linestyle="-",alpha=0.5,label=f"Médiane")
    ax.set_title("Distribution du salaire de base 2025-2026 par équipe")
    ax.set_xlabel("Équipe")
    ax.tick_params(axis="x",labelrotation=90)
    ax.legend()
    st.pyplot(fig)
    list_players(df)
