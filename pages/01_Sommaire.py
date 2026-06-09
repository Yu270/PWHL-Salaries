import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


st.set_page_config(page_title="Sommaire",page_icon="📊")

st.title("Sommaire")
st.text("Cette page présente un sommaire à haut niveau des salaires de base de la LPHF.")

df = pd.read_csv("./data/PWHL_player_salaries_2025-2026.csv")
st.dataframe(df)
