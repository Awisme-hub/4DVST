import os
import pandas as pd

# Assurer que le dossier "data" existe
os.makedirs("data", exist_ok=True)

# Lecture du fichier source brut
df = pd.read_csv("data/temperature_paris.csv")

# Nettoyage
df = df.rename(columns={'date': 'Date', 'nom': 'Station', 'tmax': 'Tmax'})

# Garder uniquement les données de PARIS-MONTSOURIS
df_paris = df[df['Station'] == 'PARIS-MONTSOURIS'].copy()

# Transformation des dates
df_paris['Date'] = pd.to_datetime(df_paris['Date'])
df_paris['Année'] = df_paris['Date'].dt.year
df_paris['Mois'] = df_paris['Date'].dt.month

# Identifier les jours où Tmax > 35°C
df_paris['Jour_de_chaleur'] = df_paris['Tmax'] > 35

# Calcul du nombre de jours > 35°C par année
jours_chaleur = df_paris[df_paris['Jour_de_chaleur']].groupby('Année').size().reset_index(name='Nb_jours_>35C')

# Moyenne des Tmax en été (juin, juillet, août)
df_ete = df_paris[df_paris['Mois'].isin([6, 7, 8])]
moyennes_ete = df_ete.groupby('Année')['Tmax'].mean().reset_index(name='Moyenne_été_Tmax')

# Fusion des deux indicateurs
df_final = pd.merge(jours_chaleur, moyennes_ete, on='Année', how='outer').sort_values('Année')

# Sauvegarde dans le fichier final
df_final.to_csv("data/data_paris_temperature.csv", index=False)

print("✅ Données traitées avec succès → `data/data_paris_temperature.csv` prêt pour Metabase.")
