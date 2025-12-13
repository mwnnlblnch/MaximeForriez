# coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import math

# FONCTIONS LOCALES

def ouvrirUnFichier(nom):
    """Ouvre un fichier CSV et renvoie un DataFrame"""
    with open(nom, "r", encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier, low_memory=False) 
    return contenu

def conversionLog(liste):
    """Convertit une liste de valeurs en logarithme naturel"""
    return [math.log(x) for x in liste if x > 0]

def ordreDecroissant(liste):
    """Trie une liste en ordre décroissant"""
    liste.sort(reverse=True)
    return liste

def ordrePopulation(pop, etat):
    """Classe une liste de populations avec les états correspondants"""
    ordrepop = []
    for i in range(len(pop)):
        if not np.isnan(pop[i]):
            ordrepop.append([float(pop[i]), etat[i]])
    ordrepop = ordreDecroissant(ordrepop)
    for i in range(len(ordrepop)):
        ordrepop[i] = [i + 1, ordrepop[i][1]]
    return ordrepop

def classementPays(ordre1, ordre2):
    """Prépare la comparaison entre deux classements"""
    classement = []
    if len(ordre1) <= len(ordre2):
        for e1 in range(len(ordre2)):
            for e2 in range(len(ordre1)):
                if ordre2[e1][1] == ordre1[e2][1]:
                    classement.append([ordre1[e2][0], ordre2[e1][0], ordre1[e2][1]])
    else:
        for e1 in range(len(ordre1)):
            for e2 in range(len(ordre2)):
                if ordre2[e2][1] == ordre1[e1][1]:
                    classement.append([ordre1[e1][0], ordre2[e2][0], ordre1[e1][1]])
    return classement

# PARTIE 1 : ÎLES

iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

# ➤ Diagnostic : afficher les colonnes pour savoir leur nom exact
print("Colonnes trouvées dans island-index.csv :")
print(list(iles.columns))

# ➤ Détection automatique de la colonne contenant “Surface”
col_surface = [col for col in iles.columns if "urface" in col.lower()]
if len(col_surface) == 0:
    raise KeyError("Aucune colonne contenant 'surface' n’a été trouvée dans le fichier island-index.csv.")
col_surface = col_surface[0]
print(f"Colonne détectée pour la surface : {col_surface}")

# Isoler la colonne et convertir en float
surface = list(pd.to_numeric(iles[col_surface], errors="coerce").dropna())

# Ajouter les surfaces supplémentaires
surface.extend([85545323, 37856841, 7768030, 7605049])

# Ordonner
surface_ord = ordreDecroissant(surface.copy())

# Visualiser la loi rang-taille
rangs = list(range(1, len(surface_ord) + 1))
plt.figure(figsize=(8, 5))
plt.plot(rangs, surface_ord, marker='o', linestyle='none')
plt.title("Loi rang-taille des îles")
plt.xlabel("Rang")
plt.ylabel("Surface (km²)")
plt.show()

# Convertir en log
log_rangs = conversionLog(rangs)
log_surface = conversionLog(surface_ord)
plt.figure(figsize=(8, 5))
plt.plot(log_rangs, log_surface, marker='o', linestyle='none')
plt.title("Loi rang-taille (log-log)")
plt.xlabel("log(Rang)")
plt.ylabel("log(Surface)")
plt.show()

# Test sur les rangs :
# Non, on ne peut pas faire de test de rang simple ici, car la variable n’est pas issue d’un échantillon aléatoire.

# PARTIE 2 : POPULATIONS DES ÉTATS

monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))

# Diagnostic : afficher les colonnes
print("Colonnes trouvées dans Le-Monde-HS-Etats-du-monde-2007-2025.csv :")
print(list(monde.columns))

# Identifier les noms exacts (peuvent varier selon le CSV)
col_etat = [col for col in monde.columns if "état" in col.lower() or "state" in col.lower()][0]
col_pop2007 = [col for col in monde.columns if "2007" in col and "Pop" in col][0]
col_pop2025 = [col for col in monde.columns if "2025" in col and "Pop" in col][0]
col_dens2007 = [col for col in monde.columns if "2007" in col and "Dens" in col][0]
col_dens2025 = [col for col in monde.columns if "2025" in col and "Dens" in col][0]

etats = list(monde[col_etat])
pop2007 = list(pd.to_numeric(monde[col_pop2007], errors="coerce"))
pop2025 = list(pd.to_numeric(monde[col_pop2025], errors="coerce"))
dens2007 = list(pd.to_numeric(monde[col_dens2007], errors="coerce"))
dens2025 = list(pd.to_numeric(monde[col_dens2025], errors="coerce"))

# Ordonner les populations et densités
classement_pop2007 = ordrePopulation(pop2007, etats)
classement_dens2007 = ordrePopulation(dens2007, etats)

# Comparaison et corrélation
comparaison2007 = classementPays(classement_pop2007, classement_dens2007)
comparaison2007.sort()

rangs_pop = [elem[0] for elem in comparaison2007]
rangs_dens = [elem[1] for elem in comparaison2007]

spearman, p_spearman = scipy.stats.spearmanr(rangs_pop, rangs_dens)
kendall, p_kendall = scipy.stats.kendalltau(rangs_pop, rangs_dens)

print("\n Corrélation des rangs 2007 :")
print(f"Spearman = {spearman:.3f} (p = {p_spearman:.3f})")
print(f"Kendall  = {kendall:.3f} (p = {p_kendall:.3f})")

# Commentaire pour le rapport :
# Les deux coefficients indiquent la corrélation entre le classement des États selon population et selon densité.
# Spearman proche de 1 ou -1 → forte corrélation monotone
# Kendall proche de 1 ou -1 → forte concordance des rangs
