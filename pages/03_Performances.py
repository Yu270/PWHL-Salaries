import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import pearsonr
from utils.plots import scatter_plot, mean_plot, median_plot


st.set_page_config(page_title="Performances",page_icon="🥅")

@st.fragment
def players_by_continuous(data: pd.DataFrame, var: str, dtype: str):
    """
    Fonction qui affiche la liste des joueuses selon une caractéristique de performance (continue). 

    Entrées
        data: données à utiliser
        var: nom de la caractéristique de performance
        dtype: type de données de la caractéristique de performance ('int' ou 'float')
    """
    assert dtype in ["int","float"], "dtype doit être 'int' ou 'float'"
    data[var] = data[var].astype(dtype)
    with st.container(horizontal=True):
        min_value, max_value = data[var].min(), data[var].max()
        st.session_state.min_value = st.number_input("Borne inférieure",min_value=min_value,max_value=max_value,help=f"Afficher les joueuses dont {var} est supérieur ou égal à X.")
        st.session_state.max_value = st.number_input("Borne supérieure",min_value=min_value,max_value=max_value,value=max_value,help=f"Afficher les joueuses dont {var} est inférieur ou égal à X.")
    temp = data[(data[var]>=st.session_state.min_value)*(data[var]<=st.session_state.max_value)].sort_values("Salaire de base 2025-2026",ascending=False)
    temp[" "] = range(1,temp.shape[0]+1)
    temp.set_index(" ",drop=True,inplace=True)
    st.dataframe(temp[["Nom complet","Équipe",var,"Salaire de base 2025-2026"]],column_config={"Salaire de base 2025-2026": st.column_config.NumberColumn(format="accounting")})

st.title("Par performances")
st.text("Cette page présente la répartition des salaires de base de la LPHF selon les performances des joueuses.")

df = pd.read_csv("./data/PWHL_player_salaries_2025-2026.csv")
df["Nombre de joueuses"] = 1

min_games = st.number_input("Nombre minimal de parties jouées lors de la saison régulière 2025-2026",min_value=15,max_value=20,step=1,help="Exclure les joueuses qui ont joué moins de X parties durant la saison régulière 2025-2026.")

df = df[df["Parties jouées"]>=min_games].copy()

# 'Parties jouées', 'Buts', 'Tirs', 'Mises en échec', 'Tirs bloqués', 'Aides', 'Points', 'Minutes de pénalité', 'Points en AN', 
# 'Points en DN', 'Mises au jeu', '% de mises au jeu', 'Temps de jeu moyen', 'Minutes pour point', 'Minutes pour tir', 
# 'Moyenne de buts', 'Moyenne de tirs', 'Moyenne de mises en échec', 'Moyenne de tirs bloqués', 'Moyenne d'aides', 
# 'Moyenne de points', 'Moyenne de minutes de pénalité', '% de buts', 'Arrêts', 'Buts alloués', 'Jeux blancs', 'Victoires', 
# 'Moyenne d'arrêts', 'Moyenne de buts alloués', '% d'arrêts', '% de victoires'
features = {
    "Parties jouées": {
        "dtype": "int",
    },
    "Buts": {
        "dtype": "int",
    },
    "Tirs": {
        "dtype": "int",
    },
    "Mises en échec": {
        "dtype": "int",
    },
    "Tirs bloqués": {
        "dtype": "int",
    },
    "Aides": {
        "dtype": "int",
    },
    "Points": {
        "dtype": "int",
    },
    "Minutes de pénalité": {
        "dtype": "int",
    },
    "Points en AN": {
        "dtype": "int",
    },
}
feature_names = list(features.keys())

feature = st.selectbox("Caractéristique de performance",options=feature_names,help="Nom de la caractéristique de performance")
corr_df = df[df[feature].notna()]
corr_mean = corr_df["Salaire de base 2025-2026"].mean()
corr_median = corr_df["Salaire de base 2025-2026"].median()

with st.container():
    st.subheader(f"Distribution du salaire de base 2025-2026 selon {feature}")
    fig = scatter_plot(corr_df,feature,"cont",comparison={"mean": corr_mean, "median": corr_median},label_rot="auto")
    st.pyplot(fig)
    r, p = pearsonr(corr_df[feature],corr_df["Salaire de base 2025-2026"])
    if p<0.05:
        st.text(f"Coefficient de corrélation linéaire : {r**2:.4f}")

with st.container():
    st.subheader("Salaire moyen selon "+feature)
    fig = mean_plot(corr_df,feature,"cont",comparison={"mean": corr_mean, "median": corr_median},label_rot="auto")
    st.pyplot(fig)

with st.container():
    st.subheader("Salaire médian selon "+feature)
    fig = median_plot(corr_df,feature,"cont",comparison={"mean": corr_mean, "median": corr_median},label_rot="auto")
    st.pyplot(fig)

with st.container():
    st.subheader("Joueuses selon "+feature)
    players_by_continuous(corr_df,feature,features[feature]["dtype"])
