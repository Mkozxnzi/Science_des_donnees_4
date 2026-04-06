# 🚦 Prédiction de la Gravité des Accidents  
Application Flask + Machine Learning

Ce projet a pour objectif de **prédire la gravité d’un accident** (*léger* ou *grave*) à partir des données du fichier national d’accidents.  
Il comprend :

- un **dashboard interactif** (page d’accueil),
- plusieurs **modèles de machine learning** entraînés,
- une **application web Flask** permettant de tester des prédictions en direct.

---

## 📂 Organisation du projet

├── data/
│   ├── raw/ # Données brutes
│   └── processed/    # Données nettoyées et prêtes pour le ML
│
├── notebooks/
│   ├── notebook_machine_learning.ipynb
│   └── notebook_visualisations.ipynb
│
├── src/
│   └── train.py      # Script d'entraînement des modèles
│
├── models/ # Tous les modèles sauvegardés
│   ├── features.pkl
│   ├── model_gb.pkl
│   ├── model_lr.pkl
│   ├── model_rf.pkl
│
├── app/
│   ├── app.py        # Application Flask
│   ├── templates/ # Pages HTML
│   │     ├── index.html
│   │     ├── predict.html
│   │     ├── resultats.html
│   │     ├── random_forest.html 
│   │     ├── logistic_regression.html
│   │     └── gradient_boosting.html 
│   │     
│   ├── static/ # Apparence générale
│         ├── style.css   
│         ├── script_box.js        
│         └── script_matrice.js           
│
├── README.md
└── requirements.txt


---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone <URL_DU_PROJET>
cd <NOM_DU_REPO>
```
### 2. Créer un environnement virtuel et installer les dépendances
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```
### 3. Lancer l'application Flask
```bash
python app/app.py
```
---

## 🌐 Utilisation
Une fois l’application lancée, ouvrir un navigateur et accéder à :

👉 **http://127.0.0.1:5000/  **
(ou **http://localhost:5000/** — c’est équivalent)

### Pages disponibles
- **Dashboard (index.html)**  <br> Vue d’ensemble du projet avec des graphiques interactifs et une présentation générale.
- **Pages modèles**  <br> Explications détaillées pour chaque modèle :
    - Random Forest
    - Logistic Regression
    - Gradient Boosting

- **Page de prédiction (predict.html)** <br> Formulaire où l’utilisateur renseigne les informations nécessaires (caractéristiques de l’usager / contexte).

- **Page de résultats (resultats.html)**  <br> Affiche la prédiction du modèle sous forme de gravité :
    - Léger
    - Grave
---

## 🧩 Fonctionnement du projet

### 🔧 Prétraitement des données

- Nettoyage et harmonisation des colonnes

- Gestion des valeurs manquantes et des catégories particulières

- Encodage des variables catégorielles avec `pandas.get_dummies`

Conversion des heures en format numérique (ex : `17:30 → 1730`)

Les données brutes sont stockées dans `data/raw/` et les données prêtes pour le machine learning dans `data/processed/`.

### 🤖 Entraînement des modèles

Les modèles utilisés sont :

- **Random Forest**

- **Logistic Regression**

- **Gradient Boosting**

L’entraînement est géré par le script :

```bash
python src/train.py
```

Les modèles entraînés sont sauvegardés dans le dossier `models/` au format `.pkl`, accompagnés de la liste des colonnes utilisées pour l’inférence (afin de garantir la cohérence entre entraînement et prédiction).

### 🌐 Application web (Flask)

- L’application Flask se trouve dans `app/app.py`.

- Le formulaire de prédiction permet de saisir toutes les informations nécessaires au modèle.

- L’utilisateur peut sélectionner le modèle qu’il souhaite utiliser (si cette option est prévue dans l’interface).

- Une fois le formulaire validé, l’utilisateur est redirigé vers une page de résultats qui affiche la gravité prédite (*léger* ou *grave*) de manière claire.

Les fichiers statiques (`static/`) gèrent :

- le style général de l’application (`style.css`),

- l'affichage des matrices de confusion (`script_matrice.js`)',

- l'affichage des encadrés (`script_box.js`).

---

## 💡 Remarques

- Les colonnes non renseignées sont automatiquement gérées par le modèle.

- L’application est pensée pour être simple, intuitive et pédagogique.

- Le projet sépare clairement :

    - le traitement des données,

    - l’entraînement des modèles,

    - l’interface web.

---

## ✨ Auteurs

Projet réalisé par Camille Seveyrat, Melissa Boccaccio et Maxime Bouteyre dans le cadre d’un projet pour l'UE Science des Données 4.