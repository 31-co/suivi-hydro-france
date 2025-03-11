import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import requests
import io
import plotly.graph_objects as go
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("api_key1")

# Fonction principale
def main():
    st.title("Précipitations et évolution du débit")

    # Calcul des dates
    now = datetime.now().astimezone()
    now = now - timedelta(hours=1)

    now_30 = now - timedelta(days=30)
    now_30_str = now_30.strftime('%Y-%m-%dT%H:%M:%SZ')
    now = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    time.sleep(1)

    # Récupérer les données de précipitations
    api_url = "https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/quotidienne"
    
    headers = {
        "apikey": api_key, 
        "Accept": "application/json"
    }
    params = {
        "id-station": "19272001", 
        "date-deb-periode": now_30_str,
        "date-fin-periode": now
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    pluie = response.json()
    pluie_code = pluie['elaboreProduitAvecDemandeResponse']['return']

    api_url_base = "https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier"
    params = {"id-cmde": pluie_code}

    response = requests.get(api_url_base, headers=headers, params=params)
    fichier = io.BytesIO(response.content)
    pluie_tulle = pd.read_csv(fichier, sep=";", quotechar='"', skipinitialspace=True, engine="python")

    pluie_t = pluie_tulle[['DATE', 'RR']]
    pluie_t['DATE'] = pluie_t['DATE'].astype(str)
    pluie_t['DATE'] = pd.to_datetime(pluie_t['DATE'], format='%Y%m%d', errors='coerce')
    pluie_t['RR'] = pluie_t['RR'].str.replace(',', '.').astype(float)

    # Calcul du total des précipitations
    total_precipitation = pluie_t['RR'].sum()

    # Affichage du total dans Streamlit
    st.write(f"### 🌧️ Total des précipitations sur la période : **{total_precipitation:.1f} mm**")
    
    # Récupérer les données de débit
    url_debit = f"http://www.vigicrues.gouv.fr/services/observations.json?CdStationHydro=P350251001"
    params = {'GrdSerie': 'Q', 'FormatDate': 'iso'}
    response = requests.get(url_debit, params=params)
    data = response.json()
    observations = data["Serie"]["ObssHydro"]
    df = pd.DataFrame(observations)
    df["DtObsHydro"] = pd.to_datetime(df["DtObsHydro"], errors="coerce")

    # Créer le graphique linéaire pour l'évolution du débit (en bleu foncé, sur l'axe y gauche)
    line = go.Scatter(
        x=df['DtObsHydro'],
        y=df['ResObsHydro'],
        mode='lines',
        name="Évolution du débit",
        line=dict(color='navy'),
        zorder=2
    )

    # Créer le graphique à barres pour les précipitations (en bleu clair, sur l'axe y droit)
    bar = go.Bar(
        x=pluie_t['DATE'].dt.strftime('%Y-%m-%d'),
        y=pluie_t['RR'],
        name="Précipitations",
        marker=dict(color='skyblue'),
        zorder=1,
        yaxis='y2'
    )

    # Créer la figure
    fig = go.Figure(data=[line, bar])

    # Ajouter les axes et les titres
    fig.update_layout(
        title='Précipitations et évolution du débit à Tulle',
        xaxis_title='Date',
        yaxis_title='Débit (m³/s)',  
        yaxis2=dict(
            title='Précipitation (mm)', 
            overlaying='y', 
            side='right', 
            showgrid=False
        ),
        barmode='group',
        template='plotly_white'
    )

    # Afficher le graphique avec Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
