-- Crée la base (dans pgAdmin ou CLI)
CREATE DATABASE meteo_france;

-- Se connecter à la base puis exécuter :
CREATE TABLE temperatures_paris (
  annee INTEGER PRIMARY KEY,
  nb_jours_sup_30C INTEGER,
  moyenne_ete_tmax FLOAT
);

-- Exemple d'insertion (automatisée via Metabase sinon)
-- INSERT INTO temperatures_paris VALUES (2003, 13, 29.8);
