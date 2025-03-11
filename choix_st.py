import requests
import pandas as pd
import streamlit as st

def choix_station():
    # URL de l'API pour la liste des stations
    url_stations = "http://www.vigicrues.gouv.fr/services/v1.1/StaEntVigiCru.json"

    # Récupérer la liste des stations
    try:
        response = requests.get(url_stations)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        stations = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des stations : {e}")  # Affichage Streamlit
        st.stop()  # Arrêt Streamlit
        return None  # Retourne None en cas d'erreur (optionnel, selon votre usage)

    # Extraire les informations des stations
    stations_info = stations['ListEntVigiCru']
    station_info_df = pd.DataFrame({
        "Rivière": [f"{station['LbCoursEau']} à {station['LbEntVigiCru']}" for station in stations_info],
        "Code station": [station['CdEntVigiCru'] for station in stations_info]
    })

    # Ajouter une option vide au début de la liste
    station_info_df = pd.concat([
        pd.DataFrame({"Rivière": ["Sélectionner/écrire le nom de la station"], "Code station": [""]}),
        station_info_df
    ], ignore_index=True)

    return station_info_df

# Exemple d'utilisation
if __name__ == "__main__":
    df = choix_station()
    if df is not None:
        print(df.head())  # Afficher les 5 premières lignes pour tester