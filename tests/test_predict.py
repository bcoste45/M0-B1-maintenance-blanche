
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Fixture client
@pytest.fixture(scope="module")
def fixture_client():
    with TestClient(app) as client: #lance lifespan pour charger modele
        yield client

# 1. POST /predict avec un payload compresseur complet, attendu 200 + body["criticite"] in {"basse","moyenne","haute"} + somme des probabilites.values() ≈ 1.
def test_cas_valide(fixture_client):
    payload = {
      "type_machine": "compresseur",
      "age_machine_jours": 1500,
      "derniere_maintenance_jours": 45,
      "temperature_moyenne": 68.5,
      "vibration_moyenne": 3.2,
      "pression_moyenne": 7.8,
      "nb_incidents_3_mois": 2
    }
    r = fixture_client.post("/predict", json=payload)    
    assert r.status_code == 200
    body = r.json()
    assert (body['criticite'] in {"basse","moyenne","haute"}) is True
    assert (body['probabilites']['basse']+body['probabilites']['moyenne']+body['probabilites']['haute']) == 1

# 2. POST avec type_machine: "INCONNU", attendu 422 (validation Pydantic).
def test_cas_invalide(fixture_client):
    payload = {
      "type_machine": "INCONNU",
      "age_machine_jours": 1500,
      "derniere_maintenance_jours": 45,
      "temperature_moyenne": 68.5,
      "vibration_moyenne": 3.2,
      "pression_moyenne": 7.8,
      "nb_incidents_3_mois": 2
    }
    r = fixture_client.post("/predict", json=payload)    
    assert r.status_code == 422
    
# 3. @pytest.mark.parametrize sur les 5 types de machine (pompe, compresseur, convoyeur, presse, four), chaque cas doit renvoyer 200.
@pytest.mark.parametrize("type_machine", ["pompe","compresseur", "convoyeur", "presse", "four"])
def test_diff_type_machine(fixture_client,type_machine):
    payload = {
          "type_machine": type_machine,
          "age_machine_jours": 1500,
          "derniere_maintenance_jours": 45,
          "temperature_moyenne": 68.5,
          "vibration_moyenne": 3.2,
          "pression_moyenne": 7.8,
          "nb_incidents_3_mois": 2
        }
    r = fixture_client.post("/predict", json=payload)    
    assert r.status_code == 200