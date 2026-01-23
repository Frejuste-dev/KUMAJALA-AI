# 🚀 Guide de Démarrage Rapide - Modèle TensorFlow Kumajala

## 📋 Prérequis

### Option A: Installation Locale (Recommandé si Python 3.11/3.12)
```bash
cd kumajala-backend
pip install -r requirements.txt
```

### Option B: Docker (Recommandé si Python 3.14+)
Si votre version de Python n'est pas encore supportée par TensorFlow (ex: Python 3.14), utilisez Docker pour un environnement stable.

```bash
# Construire et lancer la préparation des données
docker-compose -f docker-compose.ml.yml run training python -m ml.data_preparation

# Lancer l'entraînement pour le Bété
docker-compose -f docker-compose.ml.yml run training python -m ml.training --target-language bété --epochs 100

# Lancer TensorBoard
docker-compose -f docker-compose.ml.yml up tensorboard
```

## 🎯 Étapes pour Entraîner votre Premier Modèle

### Étape 1: Tester la Préparation des Données

```bash
# Tester la préparation des données pour toutes les langues
python -m ml.data_preparation
```

Cela va:
- ✅ Charger les données depuis `data/language.json`
- ✅ Augmenter le dataset (x5)
- ✅ Créer les vocabulaires
- ✅ Générer les datasets TensorFlow

### Étape 2: Entraîner un Modèle (Commencer par Bété)

```bash
# Entraîner le modèle pour le Bété (recommandé pour commencer)
python -m ml.training --target-language bété --epochs 50
```

**Options disponibles**:
- `--target-language`: Langue cible (bété, baoulé, mooré, agni)
- `--epochs`: Nombre d'epochs (défaut: 100)
- `--no-augment`: Désactiver l'augmentation de données
- `--learning-rate`: Learning rate (défaut: 0.001)

**Durée estimée**: 10-30 minutes selon votre machine

### Étape 3: Surveiller l'Entraînement avec TensorBoard

```bash
# Dans un autre terminal
tensorboard --logdir ml/logs
```

Ouvrez http://localhost:6006 pour voir:
- Courbes de loss
- Accuracy
- Learning rate
- Histogrammes des poids

### Étape 4: Évaluer le Modèle

```bash
# Évaluer sur des exemples prédéfinis
python -m ml.evaluation --target-language bété --examples-only

# Évaluer sur le dataset de test complet
python -m ml.evaluation --target-language bété
```

### Étape 5: Tester l'Intégration dans l'API

```bash
# Démarrer le serveur Flask
python app.py
```

Le service TensorFlow se chargera automatiquement au démarrage.

**Tester avec curl**:
```bash
curl -X POST http://localhost:5000/kumajala-api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "bonjour", "targetLanguage": "bété"}'
```

## 📊 Structure des Fichiers Générés

Après l'entraînement, vous aurez:

```
ml/
├── models/
│   ├── bété_model/          # Modèle SavedModel
│   ├── bété_weights.h5      # Poids du modèle
│   ├── vocab_fr.json        # Vocabulaire français
│   └── vocab_bété.json      # Vocabulaire bété
├── logs/
│   └── bété_YYYYMMDD_HHMMSS/  # Logs TensorBoard
└── checkpoints/
    └── bété_YYYYMMDD_HHMMSS/  # Checkpoints d'entraînement
```

## 🔄 Stratégie de Fallback

L'API utilise maintenant une stratégie progressive:

1. **TensorFlow** (si confiance ≥ 0.7)
2. **Gemini** (si TensorFlow échoue ou confiance faible)
3. **Database** (en dernier recours)

## 🎨 Entraîner pour Toutes les Langues

```bash
# Script pour entraîner tous les modèles
for lang in bété baoulé mooré agni; do
  echo "Entraînement pour $lang..."
  python -m ml.training --target-language $lang --epochs 50
done
```

## 🐛 Résolution de Problèmes

### Erreur: "Modèle non trouvé"
- Assurez-vous d'avoir entraîné le modèle d'abord
- Vérifiez que le dossier `ml/models/<langue>_model` existe

### Erreur: "TensorFlow non disponible"
- Vérifiez l'installation: `pip install tensorflow==2.15.0`
- Sur Windows, vous pourriez avoir besoin de Visual C++ Redistributable

### Performance lente
- Utilisez un GPU si disponible
- Réduisez `BATCH_SIZE` dans `ml/config.py`
- Réduisez `ENCODER_UNITS` et `DECODER_UNITS`

## 📈 Améliorer les Résultats

1. **Ajouter plus de données**:
   - Éditez `data/language.json`
   - Ajoutez plus de paires de traduction

2. **Augmenter les epochs**:
   ```bash
   python -m ml.training --target-language bété --epochs 200
   ```

3. **Ajuster les hyperparamètres**:
   - Éditez `ml/config.py`
   - Modifiez `EMBEDDING_DIM`, `ENCODER_UNITS`, etc.

## 🎯 Prochaines Étapes

- [ ] Entraîner les 4 modèles (bété, baoulé, mooré, agni)
- [ ] Collecter plus de données de traduction
- [ ] Tester avec des utilisateurs réels
- [ ] Optimiser les modèles (quantization, pruning)
- [ ] Déployer en production

## 💡 Conseils

- **Commencez petit**: Entraînez d'abord avec 50 epochs pour tester
- **Surveillez TensorBoard**: Vérifiez que la loss diminue
- **Testez régulièrement**: Utilisez `--examples-only` pour des tests rapides
- **Sauvegardez vos modèles**: Les checkpoints sont dans `ml/checkpoints/`
