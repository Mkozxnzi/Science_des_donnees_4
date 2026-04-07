# =============================
# IMPORTS
# =============================
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import os


# =============================
# FONCTION DATA
# =============================
def charger_preparer_donnees(annee):
    df = pd.read_csv(f"../data/processed/{annee}.csv", sep=";", na_values=["", " ", "NULL"])

    int_cols = ["hrmn", "mois", "an_nais", "grav"]
    str_cols = ["lum", "col", "catu", "sexe", "dep", "plan", "obs", "catv"]

    df[int_cols] = df[int_cols].astype("Int64")
    df[str_cols] = df[str_cols].astype("string")
    df["Num_Acc"] = df["Num_Acc"].astype("int64")

    # Corse
    corse_mapping_old = {"201": "2A", "202": "2B"}
    if annee in [2014, 2015, 2016, 2017, 2018]:
        df["dep"] = df["dep"].astype(str)
        df["dep"] = df["dep"].replace(corse_mapping_old)
        df.loc[~df["dep"].isin(corse_mapping_old.values()), "dep"] = df.loc[
            ~df["dep"].isin(corse_mapping_old.values()), "dep"
        ].str[:-1]

    # Nettoyer toutes les colonnes catégorielles
    for col in str_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .replace("<NA>", "-1")
        )

    # Remplacer catu=4
    if 2014 <= annee <= 2018:
        df.loc[df['catu'] == 4, 'catu'] = 3
        df.loc[df['catu'] == 3, 'catv'] = 99

    # Supprimer catu=4 si l'année est après 2018
    if annee > 2018:
        df = df[df['catu'] != 4]

    df["gravite"] = df["grav"].apply(lambda x: 1 if x in [2, 3] else 0)

    X = df.drop(columns=["Num_Acc", "grav", "gravite", "num_veh"])
    y = df["gravite"]

    X = pd.get_dummies(X, drop_first=True)

    return X, y


# =============================
# CHARGEMENT GLOBAL
# =============================
annees = [2014, 2015, 2016, 2017, 2018, 2020]

colonnes_globales = set()
for annee in annees:
    X, _ = charger_preparer_donnees(annee)
    colonnes_globales.update(X.columns)

data = {}
for annee in annees:
    X, y = charger_preparer_donnees(annee)
    X = X.reindex(columns=sorted(colonnes_globales), fill_value=0)
    data[annee] = (X, y)


# =============================
# TRAIN / TEST
# =============================
annees_train = annees[:-1]
annee_test = annees[-1]

X_train = pd.concat([data[a][0] for a in annees_train])
y_train = pd.concat([data[a][1] for a in annees_train])


# =============================
# MODELE
# =============================
pipeline_rf = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
        ("model", RandomForestClassifier(
        n_estimators=120,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=4,
        max_features='sqrt',
        n_jobs=-1,
        random_state=42
    ))
])

pipeline_rf.fit(X_train, y_train)


pipeline_lr = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        C=0.0011114927138446643,
        solver='liblinear',
        max_iter=1000
    ))
])

pipeline_lr.fit(X_train, y_train)



pipeline_gb = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("model", GradientBoostingClassifier(
        n_estimators=130,
        learning_rate=0.08123939920988694,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=1,
        subsample=0.825602123505447,
        random_state=42
    ))
])

pipeline_gb.fit(X_train, y_train)


# =============================
# SAUVEGARDE
# =============================
features = sorted(colonnes_globales)

output_dir = "../models/"

joblib.dump(pipeline_rf, os.path.join(output_dir, "model_rf.pkl"), compress=3)
joblib.dump(pipeline_lr, os.path.join(output_dir, "model_lr.pkl"))
joblib.dump(pipeline_gb, os.path.join(output_dir, "model_gb.pkl"))
joblib.dump(features, os.path.join(output_dir, "features.pkl"))

print("Modèle et features sauvegardés")