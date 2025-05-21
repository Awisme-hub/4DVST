import os
import pandas as pd

os.makedirs("data", exist_ok=True)

df = pd.read_csv("data/temperature_paris.csv")

df = df.rename(columns={'date': 'Date', 'nom': 'Station', 'tmax': 'Tmax'})

# Garder uniquement les données de PARIS-MONTSOURIS
df_paris = df[df['Station'] == 'PARIS-MONTSOURIS'].copy()

df_paris['Date'] = pd.to_datetime(df_paris['Date'])
df_paris['Année'] = df_paris['Date'].dt.year
df_paris['Mois'] = df_paris['Date'].dt.month

df_paris['Jour_de_chaleur'] = df_paris['Tmax'] > 35

# Calcul du nombre de jours > 35°C par année
jours_chaleur = df_paris[df_paris['Jour_de_chaleur']].groupby('Année').size().reset_index(name='Nb_jours_>35C')

df_ete = df_paris[df_paris['Mois'].isin([6, 7, 8])]
moyennes_ete = df_ete.groupby('Année')['Tmax'].mean().reset_index(name='Moyenne_été_Tmax')

df_final = pd.merge(jours_chaleur, moyennes_ete, on='Année', how='outer').sort_values('Année')

# Sauvegarde dans le fichier final
df_final.to_csv("data/data_paris_temperature.csv", index=False)

print("✅ Données traitées avec succès → `data/data_paris_temperature.csv` prêt pour Metabase.")
