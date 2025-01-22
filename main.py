from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset
import pandas as pd
import numpy as np
from api import app
import joblib

# Charger le dataset Iris
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Diviser les données en entraînement et test
X = df.drop(columns=['target'])
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entraîner un modèle de Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle entraîné dans un fichier pickle
joblib.dump(model, "model.pkl")
print("Modèle entraîné et sauvegardé sous 'model.pkl'.")

# Générer les prédictions pour le jeu de test
y_pred = model.predict(X_test)

# Calculer la précision
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision du modèle : {accuracy}")

# Dataset de référence (entraînement original)
reference_data = pd.concat([X_train, y_train.reset_index(drop=True)], axis=1)

# Simuler un dataset de production avec drift
production_data = X_test.copy()
production_data['sepal length (cm)'] += np.random.normal(0, 0.5, production_data.shape[0])  # Ajouter du bruit
production_data['target'] = y_pred  # Ajouter les prédictions comme "target"

# Créer une suite de tests avec Evidently
test_suite = TestSuite(tests=[DataStabilityTestPreset()])

# Exécuter les tests pour analyser la stabilité des données
test_suite.run(reference_data=reference_data, current_data=production_data)

# Sauvegarder le rapport Evidently en HTML
test_suite.save_html("reports/data_stability_report.html")

print("Rapport de stabilité des données généré : data_stability_report.html")
# Sauvegarder reference_data
reference_data = pd.concat([X_train, y_train.reset_index(drop=True)], axis=1)
reference_data.to_csv("reference_data.csv", index=False)
print("reference_data sauvegardé dans 'reference_data.csv'.")

# Sauvegarder X_test pour simuler des données de production
X_test.to_csv("X_test.csv", index=False)
print("X_test sauvegardé dans 'X_test.csv'.")