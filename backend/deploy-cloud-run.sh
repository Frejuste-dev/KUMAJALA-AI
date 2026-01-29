# Script de déploiement Cloud Run pour KUMAJALA-AI Backend

# 1. Authentification (à faire une seule fois)
# gcloud auth login

# 2. Définir le projet Firebase/GCP
gcloud config set project gen-lang-client-0195661235

# 3. Activer les APIs nécessaires
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 4. Build et déploiement sur Cloud Run
gcloud run deploy kumajala-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars "GEMINI_API_KEY=AIzaSyDhNnN4Z9cFl3FZT6DbO1iKWSefrYyDXD8"

# Note: Remplacez la clé API Gemini par votre vraie clé si différente
# Pour les variables d'environnement sensibles, utilisez plutôt Secret Manager:
# gcloud secrets create gemini-api-key --data-file=- < echo "VOTRE_CLE"
# Puis dans le déploiement:
# --set-secrets="GEMINI_API_KEY=gemini-api-key:latest"
