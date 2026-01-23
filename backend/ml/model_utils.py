"""
Utilitaires pour les modèles de traduction
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List

from ml.config import MODEL_DIR


def plot_attention_weights(attention_weights: np.ndarray, 
                          source_tokens: List[str], 
                          target_tokens: List[str],
                          save_path: str = None):
    """
    Visualise les poids d'attention
    
    Args:
        attention_weights: Matrice d'attention [target_len, source_len]
        source_tokens: Tokens source
        target_tokens: Tokens cible
        save_path: Chemin de sauvegarde (optionnel)
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Créer la heatmap
    sns.heatmap(
        attention_weights,
        xticklabels=source_tokens,
        yticklabels=target_tokens,
        cmap='YlOrRd',
        ax=ax,
        cbar_kws={'label': 'Attention Weight'}
    )
    
    ax.set_xlabel('Source Tokens')
    ax.set_ylabel('Target Tokens')
    ax.set_title('Attention Weights Visualization')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Visualisation sauvegardée: {save_path}")
    else:
        plt.show()
    
    plt.close()


def save_model_summary(model: tf.keras.Model, filepath: str):
    """
    Sauvegarde un résumé du modèle
    
    Args:
        model: Modèle Keras
        filepath: Chemin de sauvegarde
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        model.summary(print_fn=lambda x: f.write(x + '\n'))
    
    print(f"💾 Résumé du modèle sauvegardé: {filepath}")


def convert_to_tflite(model_path: str, output_path: str = None, quantize: bool = False):
    """
    Convertit un modèle en TensorFlow Lite
    
    Args:
        model_path: Chemin vers le modèle SavedModel
        output_path: Chemin de sortie pour le modèle TFLite
        quantize: Appliquer la quantization
    """
    if output_path is None:
        output_path = model_path.replace('_model', '_model.tflite')
    
    print(f"🔄 Conversion en TFLite...")
    
    # Créer le convertisseur
    converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    
    if quantize:
        # Quantization pour réduire la taille
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        print("   Quantization activée")
    
    # Convertir
    tflite_model = converter.convert()
    
    # Sauvegarder
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    # Afficher les tailles
    original_size = os.path.getsize(model_path) if os.path.isfile(model_path) else 0
    tflite_size = os.path.getsize(output_path)
    
    print(f"✅ Modèle TFLite créé: {output_path}")
    print(f"   Taille: {tflite_size / 1024 / 1024:.2f} MB")
    
    if original_size > 0:
        reduction = (1 - tflite_size / original_size) * 100
        print(f"   Réduction: {reduction:.1f}%")


def export_vocab_to_json(vocab, output_path: str):
    """
    Exporte un vocabulaire au format JSON
    
    Args:
        vocab: Objet Vocabulary
        output_path: Chemin de sortie
    """
    import json
    
    vocab_data = {
        'language': vocab.language,
        'word2idx': vocab.word2idx,
        'idx2word': {int(k): v for k, v in vocab.idx2word.items()},
        'size': len(vocab)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Vocabulaire exporté: {output_path}")


def plot_training_history(history, save_path: str = None):
    """
    Visualise l'historique d'entraînement
    
    Args:
        history: Objet History de Keras
        save_path: Chemin de sauvegarde (optionnel)
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss
    axes[0].plot(history.history['loss'], label='Train Loss')
    axes[0].plot(history.history['val_loss'], label='Val Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # Accuracy
    if 'accuracy' in history.history:
        axes[1].plot(history.history['accuracy'], label='Train Accuracy')
        axes[1].plot(history.history['val_accuracy'], label='Val Accuracy')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Accuracy')
        axes[1].set_title('Training and Validation Accuracy')
        axes[1].legend()
        axes[1].grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Historique sauvegardé: {save_path}")
    else:
        plt.show()
    
    plt.close()


def estimate_model_size(model: tf.keras.Model) -> Dict[str, float]:
    """
    Estime la taille d'un modèle
    
    Args:
        model: Modèle Keras
    
    Returns:
        Dictionnaire avec les statistiques de taille
    """
    # Compter les paramètres
    trainable_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    non_trainable_params = sum([tf.size(w).numpy() for w in model.non_trainable_weights])
    total_params = trainable_params + non_trainable_params
    
    # Estimer la taille en MB (float32 = 4 bytes)
    size_mb = (total_params * 4) / (1024 * 1024)
    
    return {
        'trainable_params': int(trainable_params),
        'non_trainable_params': int(non_trainable_params),
        'total_params': int(total_params),
        'estimated_size_mb': size_mb
    }


def benchmark_inference_speed(model, source_vocab, target_vocab, num_samples: int = 100):
    """
    Benchmark la vitesse d'inférence
    
    Args:
        model: Modèle de traduction
        source_vocab: Vocabulaire source
        target_vocab: Vocabulaire cible
        num_samples: Nombre d'échantillons à tester
    
    Returns:
        Statistiques de performance
    """
    import time
    
    print(f"⏱️  Benchmark d'inférence ({num_samples} échantillons)...")
    
    # Générer des séquences aléatoires
    times = []
    
    for _ in range(num_samples):
        # Séquence aléatoire
        seq_len = np.random.randint(5, 20)
        source_ids = np.random.randint(4, len(source_vocab), size=seq_len).tolist()
        
        # Mesurer le temps
        start = time.time()
        _, _ = model.translate(source_ids, source_vocab, target_vocab)
        elapsed = time.time() - start
        
        times.append(elapsed)
    
    times = np.array(times)
    
    stats = {
        'mean_ms': np.mean(times) * 1000,
        'median_ms': np.median(times) * 1000,
        'std_ms': np.std(times) * 1000,
        'min_ms': np.min(times) * 1000,
        'max_ms': np.max(times) * 1000,
    }
    
    print(f"✅ Résultats:")
    print(f"   Moyenne: {stats['mean_ms']:.2f}ms")
    print(f"   Médiane: {stats['median_ms']:.2f}ms")
    print(f"   Écart-type: {stats['std_ms']:.2f}ms")
    print(f"   Min: {stats['min_ms']:.2f}ms")
    print(f"   Max: {stats['max_ms']:.2f}ms")
    
    return stats
