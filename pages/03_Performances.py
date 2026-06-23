import numpy as np
import pandas as pd
import streamlit as st
from utils.plots import scatter_plot, mean_plot, median_plot


st.set_page_config(page_title="Performances",page_icon="🥅")

@st.fragment
def players_by_continuous(data: pd.DataFrame, var: str):
    """
    Fonction qui affiche la liste des joueuses selon une caractéristique de performance (continue). 

    Entrées
        data: données à utiliser
        var: nom de la caractéristique de performance
    """
    with st.container(horizontal=True):
        min_value, max_value = data[var].min(), data[var].max()
        st.session_state.min_value = st.number_input("Borne inférieure",min_value=min_value,max_value=max_value,help=f"Afficher les joueuses dont {var} est supérieur ou égal à X.")
        st.session_state.max_value = st.number_input("Borne supérieure",min_value=min_value,max_value=max_value,value=max_value,help=f"Afficher les joueuses dont {var} est inférieur ou égal à X.")
    temp = data[(data[var]>=st.session_state.min_value)*(data[var]<=st.session_state.max_value)].sort_values("Salaire de base 2025-2026",ascending=False)
    temp[" "] = range(1,temp.shape[0]+1)
    temp.set_index(" ",drop=True,inplace=True)
    st.dataframe(temp[["Nom complet","Équipe",var,"Salaire de base 2025-2026"]],column_config={"Salaire de base 2025-2026": st.column_config.NumberColumn(format="accounting")})

@st.fragment
def players_by_categorical(data: pd.DataFrame, var: str):
    """
    Fonction qui affiche la liste des joueuses selon une caractéristique de performance (catégorique). 

    Entrées
        data: données à utiliser
        var: nom de la caractéristique de performance
    """
    st.session_state.category = st.multiselect("Valeur(s)",options=np.sort(data[var].unique()),help=f"Afficher les joueuses dont {var} est égale à X.")
    temp = data[data[var].isin(st.session_state.category)].sort_values("Salaire de base 2025-2026",ascending=False)
    temp[" "] = range(1,temp.shape[0]+1)
    temp.set_index(" ",drop=True,inplace=True)
    st.dataframe(temp[["Nom complet","Équipe",var,"Salaire de base 2025-2026"]],column_config={"Salaire de base 2025-2026": st.column_config.NumberColumn(format="accounting")})

st.title("Par performances")
st.text("Cette page présente la répartition des salaires de base de la LPHF selon les performances des joueuses.")

df = pd.read_csv("./data/PWHL_player_salaries_2025-2026.csv")
df["Nombre de joueuses"] = 1

min_games = st.number_input("Nombre minimal de parties jouées lors de la saison régulière 2025-2026",min_value=15,max_value=20,step=1,help="Exclure les joueuses qui ont joué moins de X parties durant la saison régulière 2025-2026.")

df = df[df["Parties jouées"]>=min_games].copy()

features = {
    "Position": {
        "type": "cat",
        "label_rot": 0,
    },
    "Recrue": {
        "type": "cat",
        "label_rot": 0,
    },
    "Numéro": {
        "type": "cont",
        "label_rot": "auto",
    },
}
feature_names = list(features.keys())

feature = st.selectbox("Caractéristique de performance",options=feature_names,help="Nom de la caractéristique de performance")
feature_params = features[feature]
corr_mean = df[df[feature].notna()]["Salaire de base 2025-2026"].mean()
corr_median = df[df[feature].notna()]["Salaire de base 2025-2026"].median()

with st.container():
    st.subheader(f"Distribution du salaire de base 2025-2026 selon {feature}")
    fig = scatter_plot(df[df[feature].notna()],feature,feature_params["type"],comparison={"mean": corr_mean, "median": corr_median},label_rot=feature_params["label_rot"])
    st.pyplot(fig)

with st.container():
    st.subheader("Salaire moyen selon "+feature)
    fig = mean_plot(df[df[feature].notna()],feature,feature_params["type"],comparison={"mean": corr_mean, "median": corr_median},label_rot=feature_params["label_rot"])
    st.pyplot(fig)

with st.container():
    st.subheader("Salaire médian selon "+feature)
    fig = median_plot(df[df[feature].notna()],feature,feature_params["type"],comparison={"mean": corr_mean, "median": corr_median},label_rot=feature_params["label_rot"])
    st.pyplot(fig)

with st.container():
    st.subheader("Joueuses selon "+feature)
    if feature_params["type"]=="cont":
        players_by_continuous(df[df[feature].notna()],feature)
    elif feature_params["type"]=="cat":
        players_by_categorical(df[df[feature].notna()],feature)
    else:
        st.error("Il y a un problème avec cette caractéristique...")
