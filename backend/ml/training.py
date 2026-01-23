"""
Script d'entraînement du modèle de traduction
"""
import tensorflow as tf
from tensorflow import keras
import os
import argparse
from datetime import datetime

from ml.config import (
    EPOCHS, LEARNING_RATE, BATCH_SIZE, MODEL_DIR, LOGS_DIR, CHECKPOINTS_DIR,
    EARLY_STOPPING_PATIENCE, REDUCE_LR_PATIENCE, REDUCE_LR_FACTOR,
    SUPPORTED_LANGUAGES, TENSORBOARD_UPDATE_FREQ
)
from ml.data_preparation import DatasetBuilder
from ml.model_architecture import create_model
from ml.vocabulary import Vocabulary


class MaskedSparseCategoricalCrossentropy(keras.losses.Loss):
    """Loss function qui ignore le padding"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loss_fn = keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction='none'
        )
    
    def call(self, y_true, y_pred):
        # Calculer la loss
        loss = self.loss_fn(y_true, y_pred)
        
        # Créer un masque pour ignorer le padding (PAD_ID = 0)
        mask = tf.cast(tf.not_equal(y_true, 0), dtype=loss.dtype)
        
        # Appliquer le masque
        loss *= mask
        
        # Retourner la moyenne (en ignorant les valeurs masquées)
        return tf.reduce_sum(loss) / tf.reduce_sum(mask)


class TranslationTrainer:
    """Classe pour gérer l'entraînement du modèle"""
    
    def __init__(self, target_language: str):
        self.target_language = target_language
        self.model = None
        self.source_vocab = None
        self.target_vocab = None
        self.history = None
        
        # Créer un timestamp pour cette session d'entraînement
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_name = f"{target_language}_{self.timestamp}"
        
        # Chemins
        self.model_path = os.path.join(MODEL_DIR, f"{target_language}_model")
        self.checkpoint_path = os.path.join(CHECKPOINTS_DIR, self.run_name)
        self.log_dir = os.path.join(LOGS_DIR, self.run_name)
    
    def prepare_data(self, augment: bool = True):
        """Prépare les données d'entraînement"""
        print(f"\n{'='*60}")
        print(f"📊 PRÉPARATION DES DONNÉES")
        print(f"{'='*60}\n")
        
        builder = DatasetBuilder(self.target_language)
        train_ds, val_ds, test_ds = builder.prepare_all(augment=augment)
        
        # Sauvegarder les vocabulaires
        self.source_vocab = builder.source_vocab
        self.target_vocab = builder.target_vocab
        
        return train_ds, val_ds, test_ds
    
    def build_model(self):
        """Construit le modèle"""
        print(f"\n{'='*60}")
        print(f"🏗️  CONSTRUCTION DU MODÈLE")
        print(f"{'='*60}\n")
        
        if self.source_vocab is None or self.target_vocab is None:
            # Charger les vocabulaires si pas déjà chargés
            self.source_vocab = Vocabulary.load(language='fr')
            self.target_vocab = Vocabulary.load(language=self.target_language)
        
        self.model = create_model(
            source_vocab_size=len(self.source_vocab),
            target_vocab_size=len(self.target_vocab)
        )
    
    def compile_model(self, learning_rate: float = LEARNING_RATE):
        """Compile le modèle"""
        print(f"\n⚙️  Compilation du modèle...")
        
        # Optimizer avec learning rate scheduling
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        
        # Loss function qui ignore le padding
        loss_fn = MaskedSparseCategoricalCrossentropy()
        
        # Métriques
        metrics = [
            keras.metrics.SparseCategoricalAccuracy(name='accuracy')
        ]
        
        self.model.compile(
            optimizer=optimizer,
            loss=loss_fn,
            metrics=metrics,
            run_eagerly=True  # Force eager execution to avoid AutoGraph/Graph issues
        )
        
        print(f"✅ Modèle compilé (lr={learning_rate})")
    
    def get_callbacks(self):
        """Crée les callbacks pour l'entraînement"""
        callbacks = []
        
        # ModelCheckpoint - sauvegarder le meilleur modèle
        checkpoint_callback = keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(self.checkpoint_path, 'best_model.h5'),
            monitor='val_loss',
            save_best_only=True,
            save_weights_only=False,
            verbose=1
        )
        callbacks.append(checkpoint_callback)
        
        # EarlyStopping - arrêter si pas d'amélioration
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1
        )
        callbacks.append(early_stopping)
        
        # ReduceLROnPlateau - réduire le learning rate
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=REDUCE_LR_FACTOR,
            patience=REDUCE_LR_PATIENCE,
            min_lr=1e-6,
            verbose=1
        )
        callbacks.append(reduce_lr)
        
        # TensorBoard - visualisation
        tensorboard = keras.callbacks.TensorBoard(
            log_dir=self.log_dir,
            update_freq=TENSORBOARD_UPDATE_FREQ,
            histogram_freq=1
        )
        callbacks.append(tensorboard)
        
        # CSV Logger - sauvegarder l'historique
        csv_logger = keras.callbacks.CSVLogger(
            os.path.join(self.log_dir, 'training_log.csv')
        )
        callbacks.append(csv_logger)
        
        return callbacks
    
    def train(self, train_ds, val_ds, epochs: int = EPOCHS):
        """Entraîne le modèle"""
        print(f"\n{'='*60}")
        print(f"🚀 ENTRAÎNEMENT DU MODÈLE")
        print(f"{'='*60}\n")
        print(f"Langue cible: {self.target_language}")
        print(f"Epochs: {epochs}")
        print(f"Logs: {self.log_dir}")
        print(f"Checkpoints: {self.checkpoint_path}\n")
        
        # Créer les dossiers
        os.makedirs(self.checkpoint_path, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Obtenir les callbacks
        callbacks = self.get_callbacks()
        
        # Entraîner
        self.history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print(f"\n✅ Entraînement terminé!")
        
        return self.history
    
    def save_model(self):
        """Sauvegarde le modèle final"""
        print(f"\n💾 Sauvegarde du modèle...")
        
        # Sauvegarder le modèle complet
        self.model.save(self.model_path)
        print(f"✅ Modèle sauvegardé: {self.model_path}")
        
        # Sauvegarder aussi les poids séparément
        weights_path = os.path.join(MODEL_DIR, f"{self.target_language}_weights.h5")
        self.model.save_weights(weights_path)
        print(f"✅ Poids sauvegardés: {weights_path}")
    
    def evaluate(self, test_ds):
        """Évalue le modèle sur le test set"""
        print(f"\n{'='*60}")
        print(f"📊 ÉVALUATION DU MODÈLE")
        print(f"{'='*60}\n")
        
        results = self.model.evaluate(test_ds, verbose=1)
        
        print(f"\n📈 Résultats sur le test set:")
        print(f"   Loss: {results[0]:.4f}")
        print(f"   Accuracy: {results[1]:.4f}")
        
        return results
    
    def run_full_training(self, epochs: int = EPOCHS, augment: bool = True):
        """Pipeline complet d'entraînement"""
        print(f"\n{'#'*70}")
        print(f"# ENTRAÎNEMENT COMPLET: FR → {self.target_language.upper()}")
        print(f"{'#'*70}\n")
        
        # 1. Préparer les données
        train_ds, val_ds, test_ds = self.prepare_data(augment=augment)
        
        # 2. Construire le modèle
        self.build_model()
        
        # 3. Compiler le modèle
        self.compile_model()
        
        # 4. Entraîner
        self.train(train_ds, val_ds, epochs=epochs)
        
        # 5. Évaluer
        self.evaluate(test_ds)
        
        # 6. Sauvegarder
        self.save_model()
        
        print(f"\n{'#'*70}")
        print(f"# ✅ ENTRAÎNEMENT TERMINÉ")
        print(f"{'#'*70}\n")
        
        print(f"📂 Fichiers générés:")
        print(f"   - Modèle: {self.model_path}")
        print(f"   - Logs: {self.log_dir}")
        print(f"   - Checkpoints: {self.checkpoint_path}")
        print(f"\n💡 Pour visualiser les logs:")
        print(f"   tensorboard --logdir {LOGS_DIR}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Entraîner un modèle de traduction')
    parser.add_argument(
        '--target-language',
        type=str,
        choices=SUPPORTED_LANGUAGES,
        required=True,
        help='Langue cible pour la traduction'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=EPOCHS,
        help=f'Nombre d\'epochs (défaut: {EPOCHS})'
    )
    parser.add_argument(
        '--no-augment',
        action='store_true',
        help='Désactiver l\'augmentation de données'
    )
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=LEARNING_RATE,
        help=f'Learning rate (défaut: {LEARNING_RATE})'
    )
    
    args = parser.parse_args()
    
    # Créer le trainer
    trainer = TranslationTrainer(args.target_language)
    
    # Lancer l'entraînement complet
    trainer.run_full_training(
        epochs=args.epochs,
        augment=not args.no_augment
    )


if __name__ == "__main__":
    main()
