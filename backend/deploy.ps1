# Script de déploiement automatisé pour KUMAJALA Backend sur Cloud Run
# Assurez-vous d'avoir exécuté 'gcloud auth login' avant de lancer ce script

# Rafraîchir le PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "🚀 Déploiement de KUMAJALA Backend sur Google Cloud Run" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green

# Étape 1 : Vérifier le projet
Write-Host "`n📋 Étape 1/5 : Vérification du projet..." -ForegroundColor Cyan
gcloud config set project gen-lang-client-0195661235

# Étape 2 : Activer les APIs
Write-Host "`n🔧 Étape 2/5 : Activation des APIs nécessaires..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Étape 3 : Build et déploiement
Write-Host "`n🏗️  Étape 3/5 : Build et déploiement (cela peut prendre 5-10 minutes)..." -ForegroundColor Cyan
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

# Étape 4 : Récupérer l'URL du service
Write-Host "`n🌐 Étape 4/5 : Récupération de l'URL du service..." -ForegroundColor Cyan
$SERVICE_URL = gcloud run services describe kumajala-backend --region us-central1 --format="value(status.url)"

Write-Host "`n✅ Étape 5/5 : Déploiement terminé !" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host "`n📍 URL du backend : $SERVICE_URL" -ForegroundColor Yellow
Write-Host "`n⚠️  IMPORTANT : Mettez à jour cette URL dans :" -ForegroundColor Yellow
Write-Host "   frontend/src/api/axiosConfig.js" -ForegroundColor Yellow
Write-Host "`n📊 Pour voir les logs :" -ForegroundColor Cyan
Write-Host "   gcloud run logs read kumajala-backend --region us-central1" -ForegroundColor White
