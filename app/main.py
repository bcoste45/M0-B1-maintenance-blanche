"""API FastAPI — service de classification de criticité (M0-B1).

Expose un modèle scikit-learn pré-entraîné (cf. `model/train_baseline.py`) via
deux routes :

- `GET /health`  : santé du service (déjà fonctionnel)
- `POST /predict` : prédiction de criticité (🎯 à compléter par l'apprenant)

Le modèle est chargé une seule fois au démarrage via le `lifespan` FastAPI puis
réutilisé pour chaque requête.

Lancement local :
    uvicorn app.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import joblib
from fastapi import FastAPI, HTTPException
from loguru import logger

from app.schemas import HealthResponse, MachineInput, PredictionResponse

import pandas as pd
import time

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "model.joblib"

# Mémoire d'application — peuplée par le lifespan
state: dict[str, Any] = {}

logger.add(
    "logs/api.log",
    rotation="5 MB",
    retention="7 days",
    compression="zip",
    level="INFO",
    enqueue=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle au démarrage, libère à l'arrêt.

    Args:
        app: instance FastAPI.
    """
    if not MODEL_PATH.is_file():
        logger.error(
            f"Modèle introuvable : {MODEL_PATH}. "
            f"Lance d'abord : python model/train_baseline.py"
        )
        raise RuntimeError(f"Modèle introuvable : {MODEL_PATH}")

    logger.info(f"Chargement du modèle depuis {MODEL_PATH}")
    state["model"] = joblib.load(MODEL_PATH)
    logger.info("Modèle chargé.")

    yield

    state.clear()
    logger.info("Service arrêté, état libéré.")


app = FastAPI(
    title="FastIA — Service de criticité maintenance prédictive",
    description=(
        "API d'exposition d'un modèle scikit-learn de classification de criticité "
        "d'incidents machine (3 classes : basse, moyenne, haute)."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Retourne le statut du service et du modèle.

    Returns:
        HealthResponse — `status="ok"` si le modèle est chargé, `degraded` sinon.
    """
    is_loaded = "model" in state
    return HealthResponse(
        status="ok" if is_loaded else "degraded",
        model_loaded=is_loaded,
    )


"""Prédit la criticité d'une machine à partir de ses caractéristiques.

Args:
    item: caractéristiques de la machine (cf. `schemas.MachineInput`).

Returns:
    PredictionResponse avec la classe prédite et les probabilités.
 """
@app.post("/predict", response_model=PredictionResponse)
def predict(item: MachineInput) -> PredictionResponse:
    t0 = time.perf_counter()
    #1. Construit DataFrame
    df = pd.DataFrame([item.model_dump()])

    #2. Charge le modele
    model = state.get('model')

    #3. Classe predite
    cl_pr = model.predict(df)[0]    
    logger.info("Prédiction = {}",cl_pr)
    logger.info("Temps mis pour la prédiction = {} {}",(time.perf_counter()-t0)*1000," ms")

    #4. Probabilités
    probas = model.predict_proba(df)[0]
    classes = model.classes_

    #5. Construction du PredictionResponse
    probabilites = {}
    for c,p in zip(classes,probas):
        probabilites[c] = p

    return PredictionResponse(
            criticite=cl_pr,
            probabilites= probabilites
        )

