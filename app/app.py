from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import sklearn
import os

app = Flask(__name__)

# =============================
# LOAD MODELS + FEATURES (lazy loading + chemins Render)
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

_loaded_models = {}

def load_model(name):
    """Charge un modèle uniquement quand il est demandé (évite OOM sur Render)."""
    if name not in _loaded_models:
        path = os.path.join(MODEL_DIR, f"model_{name}.pkl")
        _loaded_models[name] = joblib.load(path)
    return _loaded_models[name]

features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))


# =============================
# ROUTES DE NAVIGATION
# =============================
@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")


@app.route("/gradient_boosting.html")
def gb_page():
    return render_template("gradient_boosting.html")


@app.route("/random_forest.html")
def rf_page():
    return render_template("random_forest.html")


@app.route("/logistic_regression.html")
def lr_page():
    return render_template("logistic_regression.html")


@app.route("/pred.html")
def form():
    return render_template("predict.html")


@app.route("/test.html")
def test():
    return render_template("test.html")


# =============================
# ROUTE DE PRÉDICTION (POST)
# =============================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.to_dict()

    # DataFrame initialisé avec toutes les features à 0
    input_df = pd.DataFrame(0, index=[0], columns=features)

    # =========================
    # VARIABLES NUMÉRIQUES
    # =========================
    if "an_nais" in data and data["an_nais"]:
        input_df.at[0, "an_nais"] = int(data["an_nais"])

    if "mois" in data and data["mois"]:
        input_df.at[0, "mois"] = int(data["mois"])

    if "hrmn" in data and data["hrmn"]:
        h, m = data["hrmn"].split(":")
        input_df.at[0, "hrmn"] = int(h) * 100 + int(m)

    # =========================
    # VARIABLES CATÉGORIELLES
    # =========================
    categorical_vars = ["sexe", "catu", "lum", "col", "plan", "obs", "catv"]

    for key in categorical_vars:
        if key in data and data[key]:
            col = f"{key}_{data[key]}"
            if col in input_df.columns:
                input_df.at[0, col] = 1

    # =========================
    # CHOIX DU MODÈLE
    # =========================
    model_choice = data.get("model", "rf")

    model_names = {
        "rf": "Random Forest",
        "lr": "Logistic Regression",
        "gb": "Gradient Boosting"
    }

    # LAZY LOADING ICI
    model = load_model(model_choice)
    model_display = model_names.get(model_choice, "Random Forest")

    # =========================
    # MAPPINGS (inchangés)
    # =========================
    sexe_map = {
        "1": "Masculin",
        "2": "Féminin"
    }

    catu_map = {
        "1": "Conducteur",
        "2": "Passager",
        "3": "Piéton"
    }

    mois_map = {
        "1": "Janvier",
        "2": "Février",
        "3": "Mars",
        "4": "Avril",
        "5": "Mai",
        "6": "Juin",
        "7": "Juillet",
        "8": "Août",
        "9": "Septembre",
        "10": "Octobre",
        "11": "Novembre",
        "12": "Décembre"
    }

    lum_map = {
        "1": "Plein jour",
        "2": "Crépuscule ou aube",
        "3": "Nuit sans éclairage public",
        "4": "Nuit avec éclairage public non allumé",
        "5": "Nuit avec éclairage public allumé"
    }

    catv_map = {
        "0": "Indéterminable",
        "1": "Bicyclette",
        "2": "Cyclomoteur < 50 cm³",
        "7": "Voiture légère (VL)",
        "10": "Véhicule utilitaire 1,5T à 3,5T",
        "13": "Poids lourd 3,5T à 7,5T",
        "14": "Poids lourd > 7,5T",
        "16": "Tracteur routier",
        "20": "Engin spécial",
        "21": "Tracteur agricole",
        "30": "Scooter < 50 cm³",
        "31": "Moto 50 à 125 cm³",
        "32": "Scooter 50 à 125 cm³",
        "33": "Moto > 125 cm³",
        "34": "Scooter > 125 cm³",
        "35": "Quad léger",
        "36": "Quad lourd",
        "37": "Autobus",
        "38": "Autocar",
        "39": "Train",
        "40": "Tramway",
        "50": "EDP à moteur",
        "60": "EDP sans moteur",
        "80": "Vélo électrique (VAE)",
        "99": "Autre véhicule"
    }

    col_map = {
        "-1": "Non renseigné",
        "1": "Deux véhicules - frontale",
        "2": "Deux véhicules - par l'arrière",
        "3": "Deux véhicules - par le côté",
        "4": "Trois véhicules et plus - en chaîne",
        "5": "Trois véhicules et plus - collisions multiples",
        "6": "Autre collision",
        "7": "Sans collision"
    }

    obs_map = {
        "-1": "Non renseigné",
        "0": "Sans objet",
        "1": "Véhicule en stationnement",
        "2": "Arbre",
        "3": "Glissière métallique",
        "4": "Glissière béton",
        "5": "Autre glissière",
        "6": "Bâtiment, mur, pile de pont",
        "7": "Support de signalisation / poste d'appel",
        "8": "Poteau",
        "9": "Mobilier urbain",
        "10": "Parapet",
        "11": "Ilot, refuge, borne haute",
        "12": "Bordure de trottoir",
        "13": "Fossé, talus, paroi rocheuse",
        "14": "Autre obstacle fixe sur chaussée",
        "15": "Autre obstacle fixe sur trottoir / accotement",
        "16": "Sortie de chaussée sans obstacle",
        "17": "Buse / tête d’aqueduc"
    }

    plan_map = {
        "-1": "Non renseigné",
        "1": "Partie rectiligne",
        "2": "Courbe à gauche",
        "3": "Courbe à droite",
        "4": "En S"
    }

    # transformer les valeurs en labels
    form_data = {
        "model": model_names.get(data.get("model"), "Non sélectionné"),
        "sexe": sexe_map.get(data.get("sexe"), "Non renseigné"),
        "an_nais": data.get("an_nais", ""),
        "catu": catu_map.get(data.get("catu"), "Non renseigné"),
        "mois": mois_map.get(data.get("mois"), "Non renseigné"),
        "hrmn": data.get("hrmn", ""),
        "dep": data.get("dep", ""),
        "lum": lum_map.get(data.get("lum"), "Non renseigné"),
        "catv": catv_map.get(data.get("catv"), "Non renseigné"),
        "col": col_map.get(data.get("col"), "Non renseigné"),
        "obs": obs_map.get(data.get("obs"), "Non renseigné"),
        "plan": plan_map.get(data.get("plan"), "Non renseigné")
    }

    # =========================
    # PRÉDICTION
    # =========================
    prediction = model.predict(input_df)[0]

    return render_template(
        "resultats.html",
        prediction=prediction,
        model=form_data["model"],
        form_data=form_data
    )


# =============================
# Lancer l'application
# =============================
if __name__ == "__main__":
    app.run(debug=True)
