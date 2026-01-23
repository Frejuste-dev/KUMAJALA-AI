# ML Module for Kumajala Translation

This directory contains the machine learning components for the custom TensorFlow translation model.

## Structure

- `config.py` - Configuration centralisée (hyperparamètres, chemins, constantes)
- `vocabulary.py` - Gestion des vocabulaires multilingues
- `data_augmentation.py` - Augmentation de données
- `data_preparation.py` - Préparation et création des datasets
- `model_architecture.py` - Architecture Seq2Seq avec attention
- `training.py` - Script d'entraînement
- `evaluation.py` - Évaluation et métriques
- `model_utils.py` - Utilitaires pour les modèles

## Directories

- `models/` - Modèles entraînés et vocabulaires sauvegardés
- `logs/` - Logs TensorBoard
- `checkpoints/` - Checkpoints d'entraînement

## Usage

### Préparer les données

```bash
python -m ml.data_preparation
```

### Entraîner un modèle

```bash
python -m ml.training --target-language bété --epochs 100
```

### Évaluer un modèle

```bash
python -m ml.evaluation --model-path ml/models/bete_model
```
