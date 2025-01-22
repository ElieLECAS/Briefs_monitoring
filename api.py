from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset
import joblib
import pandas as pd
import numpy as np

# Charger le modèle depuis le fichier pickle
try:
    model = joblib.load("model.pkl")
    print("Modèle chargé avec succès depuis 'model.pkl'.")
except FileNotFoundError:
    raise RuntimeError("Le fichier 'model.pkl' est introuvable. Veuillez entraîner le modèle et le sauvegarder.")

# Charger les données de référence et de test
try:
    reference_data = pd.read_csv("reference_data.csv")
    X_test = pd.read_csv("X_test.csv")
    print("Données de référence et de test chargées avec succès.")
except FileNotFoundError as e:
    raise RuntimeError(f"Fichier manquant : {str(e)}")


# Créer une application FastAPI
app = FastAPI()

# Définir un modèle de données pour l'entrée
class Features(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Mapper les colonnes aux noms attendus par le modèle
COLUMN_MAPPING = {
    "sepal_length": "sepal length (cm)",
    "sepal_width": "sepal width (cm)",
    "petal_length": "petal length (cm)",
    "petal_width": "petal width (cm)"
}

# Endpoint pour faire des prédictions
@app.post("/predict")
def predict(features: Features):
    try:
        # Créer un DataFrame avec les données envoyées
        input_data = pd.DataFrame([features.dict()])

        # Renommer les colonnes pour correspondre aux noms attendus par le modèle
        input_data = input_data.rename(columns=COLUMN_MAPPING)

        # Faire la prédiction
        prediction = model.predict(input_data)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction : {str(e)}")
    
@app.get("/analyze_drift")
def analyze_drift():
    # Simulez des données de production et analysez le drift
    production_data = X_test.copy()
    production_data['sepal length (cm)'] += np.random.normal(0, 0.5, production_data.shape[0])
    production_data['target'] = model.predict(production_data)

    test_suite = TestSuite(tests=[DataStabilityTestPreset()])
    test_suite.run(reference_data=reference_data, current_data=production_data)

    # Sauvegarder le rapport
    test_suite.save_html("data_stability_report.html")
    return {"message": "Rapport de drift généré avec succès. Consultez 'data_stability_report.html'."}