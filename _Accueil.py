import streamlit as st

# Configuration de la page principale
st.set_page_config(page_title="Suivi Hydro", layout="wide")
st.title("Outil de suivi et d'analyse hydrologique")

st.write("Bienvenue ! Utilisez le menu à gauche pour naviguer entre les pages :")
st.write("- **Temps réel** : Données hydrologiques en temps réel. Cette page réplique simplement les données fournies par le service vigicrues. Il s'agit de données en débits uniquement (m3/s).")
st.write("- **Historique** : Données historiques pour les stations françaises, associées à une analayse succinte (moyenne, min, max). Les données couvrent une période maximum de 30 ans.")
st.write("- **Données croisées** : Pour exemple, données croisées en temps réel pour la ville de Tulle. Les débits de la rivière Corrèze ont été croisé avec les relevés de précipitations.")
st.write("- **À propos** : Sources des données et informations.")

