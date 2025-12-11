#coding:utf8

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

DATA_DIR = "data"
IMG_DIR = "img"
os.makedirs(IMG_DIR, exist_ok=True)

# Etape 4 - Lire le CSV des résultats (with + détection du séparateur) et sélectionner colonnes quantitatives
with open(os.path.join(DATA_DIR, "resultats-elections-presidentielles-2022-1er-tour.csv"), "r", encoding="utf-8") as f:
    contenu = pd.read_csv(f, sep=None, engine="python")

colonnes_quanti = ["Inscrits", "Votants", "Blancs", "Nuls", "Exprimés", "Abstentions"]
num = contenu[colonnes_quanti].copy()

# Définir cols pour les boucles suivantes
cols = num.columns

# Etape 5 - Calculer moyennes, médianes, modes, écart-type, écart absolu à la moyenne, étendue
moyennes = num.mean().round(2)
medianes = num.median().round(2)
modes = num.mode().iloc[0].round(2)                            # première ligne = mode principal
ecarts_type = num.std(ddof=0).round(2)                         # ddof=0 -> population
ecarts_abs_moy = num.apply(lambda s: np.abs(s - s.mean()).mean()).round(2)  # écart absolu moyen
etendues = (num.max() - num.min()).round(2)                    # étendue = max - min

# (affichage facultatif pour contrôle)
print("\nMoyennes :\n", moyennes)
print("\nMédianes :\n", medianes)
print("\nModes :\n", modes)
print("\nÉcarts type :\n", ecarts_type)
print("\nÉcarts absolus moyens :\n", ecarts_abs_moy)
print("\nÉtendues :\n", etendues)

# Etape 6 - Afficher la liste des paramètres
print("\n--- Paramètres (par colonne quantitative) ---\n")
for c in cols:
    print(f"{c} : Moyenne={moyennes[c]}, Médiane={medianes[c]}, Mode={modes[c]}, "
          f"Écart-type={ecarts_type[c]}, Écart abs. moy.={ecarts_abs_moy[c]}, Étendue={etendues[c]}")

# Etape 7 - Calculer IQR et interdécile (avec quantile())
q1 = num.quantile(0.25)
q3 = num.quantile(0.75)
d1 = num.quantile(0.10)
d9 = num.quantile(0.90)

iqr = (q3 - q1).round(2)
idr = (d9 - d1).round(2)

print("\n--- IQR et Interdécile (par colonne) ---\n")
for c in cols:
    print(f"{c} : IQR={iqr[c]}, Interdécile={idr[c]}")

# Etape 8 - Boîte à moustache par colonne quantitative
for col in cols:
    plt.figure()
    plt.title(f"Boxplot : {col}")
    plt.boxplot(num[col].dropna(), labels=[col])
    plt.tight_layout()
    safe_name = col.replace(" ", "_").replace("/", "_")
    plt.savefig(os.path.join(IMG_DIR, f"boxplot_{safe_name}.png"))
    plt.close()
print(f"\nBoxplots sauvegardés dans '{IMG_DIR}/'")

# Etape 9 - Lire island-index.csv
island_path = os.path.join(DATA_DIR, "island-index.csv")
with open(island_path, "r", encoding="utf-8") as f:
    islands = pd.read_csv(f, sep=None, engine="python")

# Etape 10 - Sélectionner la colonne 'Surface (km2)' et catégoriser selon les intervalles demandés
col_name = next((c for c in islands.columns if "Surface" in c and "km" in c), None)
if col_name is None:
    raise ValueError("Colonne 'Surface (km2)' introuvable dans island-index.csv")

surface = pd.to_numeric(islands[col_name], errors="coerce")  # convertir proprement en float

bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, np.inf]
labels = [
    "0-10", "10-25", "25-50", "50-100",
    "100-2500", "2500-5000", "5000-10000", ">=10000"
]
cats = pd.cut(surface, bins=bins, labels=labels, right=True, include_lowest=True)
counts = cats.value_counts().reindex(labels).fillna(0).astype(int)

print("\n--- Décompte des îles par intervalle de surface (km²) ---\n")
print(counts)

# Etape 11 Bonus - Sortie des paramètres statistiques au format CSV et Excel
parametres = pd.DataFrame({
    "Moyenne": moyennes,
    "Médiane": medianes,
    "Mode": modes,
    "Écart type": ecarts_type,
    "Écart absolu moyen": ecarts_abs_moy,
    "Étendue": etendues,
    "IQR": iqr,
    "IDR": idr
}, index=num.columns)

os.makedirs("exports", exist_ok=True)

parametres.to_csv("exports/parametres_statistiques.csv", sep=";", encoding="utf-8")
parametres.to_excel("exports/parametres_statistiques.xlsx")

print("→ Exports réalisés dans le dossier /exports")
