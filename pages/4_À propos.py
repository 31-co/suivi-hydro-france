import streamlit as st

st.title("À propos")

st.write("""
Les données sont exprimées en débit afin de permettre des comparaisons entre stations. Toutefois, certaines stations ne disposent pas de relevés de débit et ne seront donc pas accessibles dans ce programme.
L'historique des débits est limité à 30 ans afin d'optimiser le chargement des données. Certaines stations peuvent ne pas disposer d’un historique aussi étendu.

**Outils utilisés :**
- Langage : Python
- Bibliothèques : Streamlit, Pandas, Requests, Plotly  
*(L’interactivité des graphiques Plotly a été désactivée pour une meilleure fluidité, notamment sur smartphone.)*
""")

st.write("""
**Sources des données** :
- Vigicrues : [https://www.vigicrues.gouv.fr/](https://www.vigicrues.gouv.fr/)
- Hubeau : [https://hubeau.eaufrance.fr/](https://hubeau.eaufrance.fr/)
""")

st.write("""
**Avertissement** :
Aucune vérification de la plausibilité des données n'a été effectuée. Toute responsabilité quant à leur utilisation est déclinée.
""")      





st.write("""
**Pour plus d'informations :**
[LinkedIn](https://www.linkedin.com/in/yohan-germain-068320346/)
""")
