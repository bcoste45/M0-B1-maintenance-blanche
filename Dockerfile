# Dockerfile — service de criticité maintenance prédictive (M0-B1)
#
# 🎯 À COMPLÉTER PAR L'APPRENANT.
#
# Indices d'implémentation (cf. mini-cours `02_Docker_essentiel.md`) :
#
#   1. Image de base : python:3.11-slim (légère, suffisante pour scikit-learn)
FROM python:3.11-slim
#
#   2. WORKDIR : choisir un répertoire de travail (/app par exemple)
WORKDIR /app
#
#   3. Installer les dépendances système si nécessaire (rare pour ce projet)

#
#   4. COPIER `requirements.txt` puis lancer `pip install --no-cache-dir -r requirements.txt`
#      → astuce : copier le requirements AVANT le code source pour profiter du
#      cache Docker (les couches de l'image ne sont reconstruites que si le fichier change).

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#
#   5. COPIER le code applicatif : `app/`, `model/`, et la donnée si nécessaire.
COPY app/ ./app/
COPY model/ ./model/
#
#   6. EXPOSE 8000 (port que uvicorn écoutera).
EXPOSE 8000
#
#   7. CMD ou ENTRYPOINT : démarrer uvicorn en production
#      → uvicorn app.main:app --host 0.0.0.0 --port 8000
#      → ne PAS utiliser --reload en image de production.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#
# Bonus (facultatif) : ajouter un HEALTHCHECK Docker qui interroge /health
#
# Commande type pour build et lancer une fois ce fichier complété :
#   docker build -t fastia-maintenance:dev . (Docker Desktop doit etre lance)
#   docker run --rm -p 8000:8000 fastia-maintenance:dev
#   curl http://localhost:8000/health