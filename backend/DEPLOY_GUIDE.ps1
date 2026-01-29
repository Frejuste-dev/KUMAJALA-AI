# ========================================
# GUIDE DE DÉPLOIEMENT KUMAJALA BACKEND
# ========================================

# ÉTAPE 1 : Vérifier l'installation de gcloud
# --------------------------------------------
gcloud --version

# ÉTAPE 2 : Authentification
# ---------------------------
gcloud auth login

# ÉTAPE 3 : Configurer le projet
# -------------------------------
gcloud config set project gen-lang-client-0195661235

# ÉTAPE 4 : Activer les APIs nécessaires
# ---------------------------------------
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# ÉTAPE 5 : Déployer sur Cloud Run
# ---------------------------------
# Assurez-vous d'être dans le dossier backend avant d'exécuter cette commande
cd "C:\Users\SINFORMATIQUE\OneDrive - SIBM\Documents\Dev\kumajala-main\KUMAJALA-AI\backend"

gcloud run deploy kumajala-backend `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --max-instances 10 `
  --set-env-vars "GEMINI_API_KEY=AIzaSyDhNnN4Z9cFl3FZT6DbO1iKWSefrYyDXD8"

# ÉTAPE 6 : Récupérer l'URL du service
# -------------------------------------
gcloud run services describe kumajala-backend --region us-central1 --format="value(status.url)"

# ========================================
# NOTES IMPORTANTES
# ========================================
# 1. Le déploiement peut prendre 5-10 minutes
# 2. L'URL du backend sera affichée à la fin
# 3. Vous devrez mettre à jour cette URL dans le frontend (axiosConfig.js)
# 4. Pour les logs : gcloud run logs read kumajala-backend --region us-central1
# 5. Pour redéployer : relancez simplement la commande de l'ÉTAPE 5
