import os
import pandas as pd
import matplotlib.pyplot as plt

# 2. Définition des chemins
data_path = os.path.join("data", "resultats-elections-presidentielles-2022-1er-tour.csv")
images_dir = os.path.join("images")

# Création du dossier images s’il n’existe pas déjà
os.makedirs(images_dir, exist_ok=True)

# 3. Lecture du fichier CSV
with open(data_path, "r", encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier, sep=",", quotechar='"')

# 4. Affichage du DataFrame
print("\n Aperçu du contenu du CSV")
print(contenu.head())

# 5. Nombre de lignes et colonnes
n_lignes = len(contenu)
n_colonnes = len(contenu.columns)
print(f"\nNombre de lignes : {n_lignes}")
print(f"Nombre de colonnes : {n_colonnes}")

# 6. Types des variables
print("\n Types de données des colonnes")
types_colonnes = contenu.dtypes
print(types_colonnes)

# Création d'une liste de types simples (int, float, str, bool)
types_simplifies = []
for col in contenu.columns:
    t = contenu[col].dtype
    if pd.api.types.is_integer_dtype(t):
        types_simplifies.append("int")
    elif pd.api.types.is_float_dtype(t):
        types_simplifies.append("float")
    elif pd.api.types.is_bool_dtype(t):
        types_simplifies.append("bool")
    else:
        types_simplifies.append("str")

# Association nom/type
types_variables = dict(zip(contenu.columns, types_simplifies))
print("\nListe des types simplifiés :")
for k, v in types_variables.items():
    print(f"{k} : {v}")

# 7. Nom des colonnes (premières lignes)
print("\n Nom des colonnes")
print(contenu.columns)

# 8. Sélection du nombre d’inscrits
if "Inscrits" in contenu.columns:
    inscrits = contenu["Inscrits"]
else:
    # Parfois le nom diffère légèrement selon la source du CSV
    inscrits = contenu.filter(like="Inscrit").iloc[:, 0]
print("\n Exemple de valeurs d'inscrits")
print(inscrits.head())

# 9. Somme des colonnes quantitatives
print("\n Somme des colonnes quantitatives")
somme_colonnes = []
for col in contenu.columns:
    if types_variables[col] in ["int", "float"]:
        somme = contenu[col].sum()
        somme_colonnes.append((col, somme))
        print(f"{col} : {somme}")
    else:
        print(f"{col} : non numérique (ignoré)")

# 10. Diagrammes en barres : inscrits et votants par département
print("\n Création des diagrammes en barres")

# On vérifie les noms de colonnes probables
cols_departement = [c for c in contenu.columns if "Département" in c or "Code" in c][0]
cols_inscrits = [c for c in contenu.columns if "Inscrit" in c][0]
cols_votants = [c for c in contenu.columns if "Votant" in c][0]

for _, row in contenu.iterrows():
    dep = str(row[cols_departement])
    inscrits = row[cols_inscrits]
    votants = row[cols_votants]

    plt.figure()
    plt.bar(["Inscrits", "Votants"], [inscrits, votants])
    plt.title(f"Inscrits et votants - {dep}")
    plt.xlabel("Catégories")
    plt.ylabel("Nombre de personnes")
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, f"bar_{dep}.png"))
    plt.close()

print("Diagrammes en barres enregistrés dans src/images/")

# 11. Diagrammes circulaires (votes blancs, nuls, exprimés, abstention)
print("\n Création des diagrammes circulaires")
cols_blancs = [c for c in contenu.columns if "Blanc" in c][0]
cols_nuls = [c for c in contenu.columns if "Nul" in c][0]
cols_exprimes = [c for c in contenu.columns if "Exprim" in c][0]
cols_abstention = [c for c in contenu.columns if "Abstention" in c][0]

for _, row in contenu.iterrows():
    dep = str(row[cols_departement])
    valeurs = [row[cols_blancs], row[cols_nuls], row[cols_exprimes], row[cols_abstention]]
    labels = ["Blancs", "Nuls", "Exprimés", "Abstention"]

    plt.figure()
    plt.pie(valeurs, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title(f"Répartition des votes - {dep}")
    plt.axis("equal")
    plt.savefig(os.path.join(images_dir, f"pie_{dep}.png"))
    plt.close()

print("Diagrammes circulaires enregistrés dans src/images/")

# 12. Histogramme de la distribution des inscrits
print("\n Création de l'histogramme de la distribution des inscrits")

plt.figure()
plt.hist(contenu[cols_inscrits], bins=10, density=True, edgecolor='black')
plt.title("Distribution statistique des inscrits (histogramme normalisé)")
plt.xlabel("Nombre d'inscrits")
plt.ylabel("Densité")
plt.tight_layout()
plt.savefig(os.path.join(images_dir, "histogramme_inscrits.png"))
plt.close()

print("Histogramme enregistré dans src/images/")
