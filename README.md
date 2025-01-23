# 🤖 Projet ML Monitoring - Iris Dataset

## 📋 Description

Système de prédiction sur le dataset Iris avec monitoring complet intégrant FastAPI, Prometheus, Grafana et détection de drift des données.

## 🏗 Architecture

### Services

-   **API FastAPI** : Service de prédiction (port 8000)
-   **Prometheus** : Collecte de métriques (port 9090)
-   **Grafana** : Visualisation des métriques (port 3000)
-   **Node Exporter** : Métriques système (port 9100)

## 🚀 Installation

### Prérequis

-   Docker et Docker Compose
-   Python 3.10+
-   Git

### Configuration

1. Cloner le repository :

2. Créer l'environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# ou
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## 🎮 Utilisation

### Démarrer les services

```bash
docker-compose up --build
```

### Accès aux interfaces

-   API ML : http://localhost:8000
-   Documentation API : http://localhost:8000/docs
-   Prometheus : http://localhost:9090
-   Grafana : http://localhost:3000 (admin/pass@123)

### Test de l'API

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}'
```

## 📊 Monitoring

### Métriques disponibles

#### API Metrics

-   Temps de réponse
-   Nombre de requêtes
-   Taux d'erreur

#### ML Metrics

-   Précision du modèle
-   Drift des données
-   Distribution des prédictions

#### System Metrics

-   CPU Usage
-   Mémoire
-   Disk I/O
-   Network

### Configuration réseau

Le projet utilise un réseau Docker dédié (172.16.238.0/24) avec les services suivants :

-   API : 172.16.238.10
-   Prometheus : 172.16.238.11
-   Grafana : 172.16.238.12
-   Node Exporter : 172.16.238.13

## 📁 Structure du projet

```
.
├── api.py                          # API FastAPI
├── main.py                         # Script d'entraînement
├── Dockerfile                      # Configuration Docker
├── docker-compose.yaml            # Configuration services
├── requirements.txt               # Dépendances Python
├── prometheus.yml                 # Config Prometheus
├── reports/                      # Rapports de drift
├── grafana/
│   ├── provisioning/            # Config dashboards
│   └── config.monitoring        # Config Grafana
└── README.md
```

## 🔍 Fonctionnalités

### ML

-   Prédiction sur dataset Iris
-   Détection de drift
-   Monitoring des performances

### Monitoring

-   Dashboards Grafana préconfigurés
-   Alertes personnalisables
-   Métriques en temps réel

## 🛠 Développement

### Environnement local

```bash
# Lancer l'API seule
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Tests

```bash
pytest tests/
```

## 🔐 Sécurité

-   Réseau Docker isolé
-   Authentification Grafana
-   Volumes Docker sécurisés

## 📝 Logs

Les logs sont disponibles via :

```bash
docker-compose logs -f [service]
```


## 📫 Support

Pour toute question ou problème, ouvrez une issue sur le repository.