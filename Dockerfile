# Utiliser l'image officielle légère de Python
FROM python:3.12-slim

# Mise à jour des paquets système et installation des dépendances nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# Permettre l'affichage immédiat des logs
ENV PYTHONUNBUFFERED=True

# Définir le répertoire de travail
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copier les fichiers nécessaires
COPY . ./
COPY models/ ./models
COPY ./models/rf_model_0_1.pkl ./models
COPY requirements.txt ./
COPY templates ./templates
COPY main.py ./




# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Flask
EXPOSE 8080

# Définir les variables d'environnement pour Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Commande par défaut pour exécuter l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
