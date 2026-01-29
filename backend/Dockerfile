# Dockerfile pour déployer l'API Flask sur Google Cloud Run
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir \
    tensorflow==2.15.0 \
    numpy==1.24.3 \
    sacrebleu==2.3.1 \
    Flask==2.3.3 \
    Flask-CORS==4.0.0 \
    google-cloud-firestore==2.13.1 \
    gTTS==2.5.4 \
    google-generativeai==0.3.2 \
    python-dotenv==1.0.0 \
    requests==2.31.0 \
    gunicorn==21.2.0

# Copier le reste du code de l'application
COPY . .

# Créer les dossiers nécessaires pour le ML
RUN mkdir -p ml/models ml/logs ml/checkpoints

# Exposer le port pour Cloud Run (8080 par défaut)
EXPOSE 8080

# Variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV PORT=8080

# Utiliser gunicorn pour la production
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
