# M0-B1 — maintenance prédictive · API REST


## 📁 Architecture

```
M0-B1-maintenance-<prenom>/
├── app/
│   ├── __init__.py
│   ├── main.py             ← FastAPI : /health (✅) + /predict 
│   └── schemas.py          ← Pydantic : MachineInput, PredictionResponse
├── data/
│   ├── generate_dataset.py ← régénération du dataset (déjà exécuté)
│   └── maintenance_data.csv ← dataset synthétique 6 500 lignes
├── model/
│   ├── train_baseline.py   ← entraînement (déjà exécuté)
│   └── model.joblib        ← modèle pré-entraîné ~5,7 Mo (chargé au démarrage)
├── tests/
│   ├── __init__.py
│   └── test_health.py      ← test pytest fonctionnel au clone (✅)
│   └── test_predict.py 
├── ressources/             ← 📚 mini-cours d'appui 
│   ├── 01_FastAPI_essentiel.md
│   ├── 02_Docker_essentiel.md
│   ├── 03_Loguru_essentiel.md
│   ├── 04_Pytest_API_essentiel.md
│   ├── liens_officiels.md
│   └── README.md           ← ordre de mobilisation + objectifs
├── Dockerfile              
├─|
─── .dockerignore requirements.txt        ← dépendances figées
├── .gitignore
└── README.md 
```


## Comment lancer
Pour lancer l'environnement virtuel 
```bash
python -m venv .venv 
.venv\Scripts\activate
#source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt

# Lancer l'API (rechargement auto) — dans un premier terminal
uvicorn app.main:app --reload

# Lancer les tests — dans un second terminal (réactive d'abord l'environnement)
.venv\bin\activate
```
et pour lancer l'image Docker (il faut d'abord que Docker soi lancé)
```bash
docker build -t fastia-maintenance:dev .
docker run --rm -p 8000:8000 fastia-maintenance:dev
```

## Comment tester
Il suffit de lancer la commande ```pytest -v ```, 9 tests sont lancés.


## Résultats
### Tests
Résultats de 
```bash
pytest -v
```

```
collected 9 items                                                                                                              

tests/test_health.py::test_health_returns_200 PASSED                                                                     [ 11%]
tests/test_health.py::test_health_response_schema PASSED                                                                 [ 22%]
tests/test_predict.py::test_cas_valide PASSED                                                                            [ 33%]
tests/test_predict.py::test_cas_invalide PASSED                                                                          [ 44%]
tests/test_predict.py::test_diff_type_machine[pompe] PASSED                                                              [ 55%]
tests/test_predict.py::test_diff_type_machine[compresseur] PASSED                                                        [ 66%]
tests/test_predict.py::test_diff_type_machine[convoyeur] PASSED                                                          [ 77%]
tests/test_predict.py::test_diff_type_machine[presse] PASSED                                                             [ 88%]
tests/test_predict.py::test_diff_type_machine[four] PASSED                                                               [100%]
```

### Curl
```bash
curl http://localhost:8000/health
```

```
{"status":"ok","model_loaded":true}
```

### Docker
```bash
 docker images
```

``` 
                                                                                                                                                               i Info →   U  In Use
IMAGE                             ID             DISK USAGE   CONTENT SIZE   EXTRA        
fastia-maintenance:dev            be9eb10c1024        791MB          180MB        
```   
 