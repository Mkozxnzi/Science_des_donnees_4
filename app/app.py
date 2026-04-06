from flask import Flask, request, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__)

# =============================
# CHEMINS ROBUSTES
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# =============================
# LAZY LOADING DES MODELES
# =============================
_loaded_models = {}

def get_model(name):
    """Charge un modèle uniquement quand il est demandé."""
    if name not in _loaded_models:
        path = os.path.join(MODEL_DIR, f"model_{name}.pkl")
        _loaded_models[name] = joblib.load(path)
    return _loaded_models[name]

# =============================
# FEATURES
# =============================
features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))

# =============================
# ROUTES
# =============================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pred.html")
def form():
    return render_template("predict.html")

# =============================
# PREDICTION
# =============================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.to_dict()

    # DataFrame initialisé avec toutes les features à 0
    input_df = pd.DataFrame(0, index=[0], columns=features)

    # NUMERIQUES
    if data.get("an_nais"):
        input_df.at[0, "an_nais"] = int(data["an_nais"])

    if data.get("mois"):
        input_df.at[0, "mois"] = int(data["mois"])

    if data.get("hrmn"):
        h, m = data["hrmn"].split(":")
        input_df.at[0, "hrmn"] = int(h) * 100 + int(m)

    # CATEGORIELLES
    categorical_vars = ["sexe", "catu", "lum", "col", "plan", "obs", "catv"]
    for key in categorical_vars:
        if data.get(key):
            col = f"{key}_{data[key]}"
            if col in input_df.columns:
                input_df.at[0, col] = 1

    # CHOIX DU MODELE
    model_choice = data.get("model", "rf")
    model = get_model(model_choice)

    # PREDICTION
    prediction = model.predict(input_df)[0]

    return render_template(
        "resultats.html",
        prediction=prediction,
        model=model_choice,
        form_data=data
    )

if __name__ == "__main__":
    app.run(debug=True)
