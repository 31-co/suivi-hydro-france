import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta
from choix_st import choix_station  # Import de la fonction

# Configuration de la page Streamlit
st.set_page_config(page_title="Suivi Hydro", layout="wide")
st.title("Débits en temps réel")

# Récupérer la liste des stations avec la fonction importée
station_info_df = choix_station()

# Sélection de la station
selected_station = st.selectbox("", station_info_df['Rivière'])

# Si une station est sélectionnée
if selected_station != "Sélectionner/écrire le nom de la station":
    # Récupérer le code de la station sélectionnée
    station_code = station_info_df[station_info_df['Rivière'] == selected_station]['Code station'].values[0]
    
    # URL de l'API pour les données de débit
    url_debit = f"http://www.vigicrues.gouv.fr/services/observations.json?CdStationHydro={station_code}"
    params = {'GrdSerie': 'Q', 'FormatDate': 'iso'}
    
    try:
        # Récupérer les données de débit
        response = requests.get(url_debit, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Convertir les données en DataFrame
        observations = data["Serie"]["ObssHydro"]
        df = pd.DataFrame(observations)
        
        # Vérifier si la clé 'DtObsHydro' existe dans les données
        if 'DtObsHydro' not in df.columns:
            st.error("Pas de donnée en débit pour cette station. Veuillez sélectionner une autre station.")
            st.stop()
        
        df["DtObsHydro"] = pd.to_datetime(df["DtObsHydro"], errors="coerce")
        
        # Sélection de la période d'affichage
        st.subheader("Filtrer par période")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            all_time = st.button("Tout afficher")
        with col2:
            last_7_days = st.button("Derniers 7 jours")
        with col3:
            last_2_days = st.button("Derniers 2 jours")
        
        # Filtrer les données selon le choix
        if last_7_days:
            df = df[df["DtObsHydro"] >= (datetime.now().astimezone() - timedelta(days=7))]
        elif last_2_days:
            df = df[df["DtObsHydro"] >= (datetime.now().astimezone() - timedelta(days=2))]
        
        # Créer un graphique avec Plotly
        fig = px.line(
            df, x="DtObsHydro", y="ResObsHydro",
            title=f"Évolution du débit, station : {data['Serie']['LbStationHydro']} ({data['Serie']['CdStationHydro']})",
            labels={"DtObsHydro": "Date", "ResObsHydro": "Débit (m³/s)"}
        )
        fig.update_layout(
        xaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe X
        yaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe Y
        dragmode=False,               # Désactive le drag
        hovermode=False               # Désactive le hover
        )
        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        st.stop()
    except KeyError as e:
        st.error("Pas de donnée en débit pour cette station. Veuillez sélectionner une autre station.")
        st.stop()

else:
    st.write("Aucune station sélectionnée.")
