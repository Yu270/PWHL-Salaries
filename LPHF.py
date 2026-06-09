import streamlit as st

st.set_page_config(page_title="LPHF",page_icon="🏒")

st.title("Ligue professionnelle de hockey féminin")

with st.container():
    st.subheader("Salaires de la LPHF")
    st.text("Cette application comprend x pages pour analyser les salaires de base des joueuses de la LPHF.")
    st.text("")
    st.markdown("Sources des données : PWHLPA ([référence](https://www.pwhlpa.com/salary-guide)) et API HockeyTech ([référence](https://github.com/IsabelleLefebvre97/PWHL-Data-Reference))")
    st.markdown("Récupération et traitement des données : repo GitHub [PWHL-Dashboards](https://github.com/Yu270/PWHL-Dashboards/tree/main/data)")
