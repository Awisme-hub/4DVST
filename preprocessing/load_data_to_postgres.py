import csv
import psycopg2

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname="meteo_france",
    user="meteo_user",
    password="meteo_pass",
    host="localhost",
    port="5434"
)
cur = conn.cursor()

with open("data/data_paris_temperature.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        annee = int(row["Année"])
        nb_jours_sup_35C = int(row["Nb_jours_>35C"])
        moyenne = float(row["Moyenne_été_Tmax"])
        
        cur.execute(
            """
            INSERT INTO temperatures_paris (annee, nb_jours_sup_35C, moyenne_ete_tmax)
            VALUES (%s, %s, %s)
            ON CONFLICT (annee) DO NOTHING;
            """,
            (annee, nb_jours_sup_35C, moyenne)
        )

conn.commit()
cur.close()
conn.close()

print("✅ Données insérées avec succès dans la base PostgreSQL.")
