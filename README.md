# Prédiction de la Gravité des Accidents  
Application Flask + Machine Learning

Ce projet a pour objectif de **prédire la gravité d’un accident** (*léger* ou *grave*) à partir des données du fichier national d’accidents.  
Il comprend :

- un **dashboard interactif** (page d’accueil),
- plusieurs **modèles de machine learning** entraînés,
- une **application web Flask** permettant de tester des prédictions en direct.

---

## Démo en ligne
L’application est accessible ici : <br>
[(https://predicgravacc.onrender.com)](https://predicgravacc.onrender.com)

---

## Organisation du projet

├── data/ <br>
│   ├── raw/ # Données brutes <br>
│   └── processed/    # Données nettoyées et prêtes pour le ML <br>
│ <br>
├── notebooks/ <br>
│   ├── notebook_machine_learning.ipynb <br>
│   └── notebook_visualisations.ipynb <br>
│ <br>
├── src/ <br>
│   └── train.py      # Script d'entraînement des modèles <br>
│ <br>
├── models/ # Tous les modèles sauvegardés <br>
│   ├── features.pkl <br>
│   ├── model_gb.pkl <br>
│   ├── model_lr.pkl <br>
│   ├── model_rf.pkl <br>
│ <br>
├── app/ <br>
│   ├── app.py        # Application Flask <br>
│   ├── templates/ # Pages HTML <br>
│   │     ├── index.html <br>
│   │     ├── predict.html <br>
│   │     ├── resultats.html <br>
│   │     ├── random_forest.html <br>
│   │     ├── logistic_regression.html <br>
│   │     └── gradient_boosting.html <br>
│   │     <br>
│   ├── static/ # Apparence générale <br>
│         ├── style.css   <br>
│         ├── script_box.js     <br>   
│         └── script_matrice.js  <br>         
│ <br>
├── README.md <br>
├── runtime.txt <br>
├── requirements.txt <br>
└── Procfile

---

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Mkozxnzi/Science_des_donnees_4.git
cd Science_des_donnees_4
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

## Utilisation
Une fois l’application lancée, ouvrir un navigateur et accéder à :

**http://127.0.0.1:5000/** <br>
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

## Fonctionnement du projet

### Prétraitement des données

- Nettoyage et harmonisation des colonnes

- Gestion des valeurs manquantes et des catégories particulières

- Encodage des variables catégorielles avec `pandas.get_dummies`

Conversion des heures en format numérique (ex : `17:30 → 1730`)

Les données brutes sont stockées dans `data/raw/` et les données prêtes pour le machine learning dans `data/processed/`.

### Entraînement des modèles

Les modèles utilisés sont :

- **Random Forest**

- **Logistic Regression**

- **Gradient Boosting**

L’entraînement est géré par le script :

```bash
python src/train.py
```

Les modèles entraînés sont sauvegardés dans le dossier `models/` au format `.pkl`, accompagnés de la liste des colonnes utilisées pour l’inférence (afin de garantir la cohérence entre entraînement et prédiction).

### Application web (Flask)

- L’application Flask se trouve dans `app/app.py`.

- Le formulaire de prédiction permet de saisir toutes les informations nécessaires au modèle.

- L’utilisateur peut sélectionner le modèle qu’il souhaite utiliser.

- Une fois le formulaire validé, l’utilisateur est redirigé vers une page de résultats qui affiche la gravité prédite (*léger* ou *grave*) de manière claire.

Les fichiers statiques (`static/`) gèrent :

- le style général de l’application (`style.css`),

- l'affichage des matrices de confusion (`script_matrice.js`)',

- l'affichage des encadrés (`script_box.js`).

---

## Remarques

- Les colonnes non renseignées sont automatiquement gérées par le modèle.

- L’application est pensée pour être simple, intuitive et pédagogique.

- Le projet sépare clairement :

    - le traitement des données,

    - l’entraînement des modèles,

    - l’interface web.

---

Le projet contient également des fichiers (`runtime.txt`, `Procfile`) utilisés uniquement pour le déploiement sur Render. Ils ne sont pas nécessaires pour une exécution locale.

---

## Sources et outils utilisés
Dans le cadre de ce projet, nous avons ponctuellement utilisé des outils d’assistance tels que Microsoft Copilot, Gemini et ChatGPT pour nous documenter, explorer différentes approches de code et obtenir des pistes de résolution lors de certaines étapes techniques. <br>
L’ensemble du développement, des choix méthodologiques et de l’intégration des modèles a été réalisé et validé par les membres du groupe.

## Auteurs

Projet réalisé par Camille Seveyrat, Melissa Boccaccio et Maxime Bouteyre dans le cadre d’un projet pour l'UE Science des Données 4.
