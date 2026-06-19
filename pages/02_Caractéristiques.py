import datetime
import numpy as np
import pandas as pd
import streamlit as st
from utils.plots import scatter_plot, mean_plot, median_plot


st.set_page_config(page_title="Caractéristiques",page_icon="📊")

st.title("Par caractéristique")
st.text("Cette page présente la répartition des salaires de base de la LPHF selon différentes caractéristiques des joueuses.")

df = pd.read_csv("./data/PWHL_player_salaries_2025-2026.csv")
df["Âge"] = datetime.datetime.now().year-df["Année de naissance"]
df["Province de naissance"] = np.where(df["Pays de naissance"]=="Canada",df["Province/état de naissance"],None)
df["État de naissance"] = np.where(df["Pays de naissance"]=="United States",df["Province/état de naissance"],None)
df["Nombre de joueuses"] = 1

min_games = st.number_input("Nombre minimal de parties jouées lors de la saison régulière 2025-2026",min_value=15,max_value=20,step=1,help="Exclure les joueuses qui ont joué moins de X parties durant la saison régulière 2025-2026.")

df = df[df["Parties jouées"]>=min_games].copy()
GLOBAL_MEAN = df["Salaire de base 2025-2026"].mean()
GLOBAL_MEDIAN = df["Salaire de base 2025-2026"].median()

features = {
    "Âge": {
        "type": "cont",
        "comparison": "local",
        "label_rot": "auto",
    },
}
feature_names = list(features.keys())
feature_names.sort()

feature = st.selectbox("Caractéristique",options=["Âge"],help="Nom de la caractéristique")
feature_params = features[feature]

with st.container():
    st.subheader(f"Distribution du salaire de base 2025-2026 selon {feature}")
    fig = scatter_plot(df,feature,feature_params["type"],comparison=feature_params["comparison"],label_rot=feature_params["label_rot"])
    st.pyplot(fig)

with st.container():
    st.subheader("Salaire moyen selon "+feature)
    fig = mean_plot(df,feature,feature_params["type"],comparison=feature_params["comparison"],label_rot=feature_params["label_rot"])
    st.pyplot(fig)

with st.container():
    st.subheader("Salaire médian selon "+feature)
    fig = median_plot(df,feature,feature_params["type"],comparison=feature_params["comparison"],label_rot=feature_params["label_rot"])
    st.pyplot(fig)
