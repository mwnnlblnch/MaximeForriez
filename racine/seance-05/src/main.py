import pandas as pd
import numpy as np
from scipy.stats import shapiro
import math

# 1. Théorie de l’échantillonnage

# Fonction pour ouvrir un fichier CSV local
def ouvrirUnFichier(chemin_fichier):
    return pd.read_csv(chemin_fichier)

# Charger le fichier des 100 échantillons
fichier_echantillons = "./data/Echantillonnage-100-Echantillons.csv"
df_echantillons = ouvrirUnFichier(fichier_echantillons)

# Calcul des moyennes par colonne et arrondi
moyennes = df_echantillons.mean().round(0)
print("Moyennes arrondies des échantillons :")
print(moyennes)

# Fréquences des moyennes des échantillons
somme_moyennes = moyennes.sum()
freq_echantillons = (moyennes / somme_moyennes).round(2)
print("\nFréquences des échantillons :")
print(freq_echantillons)

# Fréquences de la population mère
population_mere = pd.Series({'Pour': 852, 'Contre': 911, 'Sans opinion': 422})
freq_population = (population_mere / population_mere.sum()).round(2)
print("\nFréquences de la population mère :")
print(freq_population)

# Intervalle de fluctuation à 95 % (z = 1.96)
z = 1.96
n_total = somme_moyennes
intervalle_fluctuation = {}
for opinion, f in freq_population.items():
    ecart_type = math.sqrt(f * (1 - f) / n_total)
    borne_inf = round(f - z * ecart_type, 2)
    borne_sup = round(f + z * ecart_type, 2)
    intervalle_fluctuation[opinion] = (borne_inf, borne_sup)
print("\nIntervalle de fluctuation à 95 % :")
print(intervalle_fluctuation)

# 2. Théorie de l’estimation

# Prendre le premier échantillon
premier_echantillon = list(df_echantillons.iloc[0])
total_premier = sum(premier_echantillon)

# Calcul des fréquences
freq_premier = [round(x / total_premier, 2) for x in premier_echantillon]
print("\nFréquences du premier échantillon :")
print(freq_premier)

# Intervalle de confiance pour le premier échantillon
intervalle_confiance = []
for f in freq_premier:
    ecart_type = math.sqrt(f * (1 - f) / total_premier)
    borne_inf = round(f - z * ecart_type, 2)
    borne_sup = round(f + z * ecart_type, 2)
    intervalle_confiance.append((borne_inf, borne_sup))
print("\nIntervalle de confiance du premier échantillon à 95 % :")
print(intervalle_confiance)

# 3. Théorie de la décision

# Tester la normalité de deux fichiers
fichier_test1 = "./data/Loi-normale-Test-1.csv"
fichier_test2 = "./data/Loi-normale-Test-2.csv"

df_test1 = ouvrirUnFichier(fichier_test1)
df_test2 = ouvrirUnFichier(fichier_test2)

# Shapiro-Wilk test
stat1, p1 = shapiro(df_test1.iloc[:,0])
stat2, p2 = shapiro(df_test2.iloc[:,0])

print("\nTest de normalité Shapiro-Wilk :")
print(f"Fichier Test 1 -> Stat={stat1:.3f}, p={p1:.3f} -> {'Normale' if p1 > 0.05 else 'Non normale'}")
print(f"Fichier Test 2 -> Stat={stat2:.3f}, p={p2:.3f} -> {'Normale' if p2 > 0.05 else 'Non normale'}")

