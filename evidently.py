from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd

# Charger les datasets
reference_data = pd.read_csv('reference_data.csv')
production_data = pd.read_csv('production_data.csv')

# Créer un tableau Evidently
dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference_data, production_data)
dashboard.save("reports/data_drift_report.html")
