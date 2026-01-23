"""
Préparation des données pour l'entraînement du modèle de traduction
"""
import json
import numpy as np
import tensorflow as tf
from typing import List, Tuple, Dict
import random

from ml.config import (
    LANGUAGE_JSON_PATH, SOURCE_LANGUAGE, SUPPORTED_LANGUAGES,
    MAX_SEQUENCE_LENGTH, BATCH_SIZE, VALIDATION_SPLIT, TEST_SPLIT,
    PAD_ID, AUGMENTATION_FACTOR
)
from ml.vocabulary import Vocabulary
from ml.data_augmentation import DataAugmenter


class DatasetBuilder:
    """Classe pour construire les datasets d'entraînement"""
    
    def __init__(self, target_language: str):
        if target_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Langue non supportée: {target_language}")
        
        self.target_language = target_language
        self.source_vocab = None
        self.target_vocab = None
        self.augmenter = DataAugmenter()
        
        # Données brutes
        self.raw_pairs: List[Tuple[str, str]] = []
        self.augmented_pairs: List[Tuple[str, str]] = []
    
    def load_data_from_json(self, json_path: str = LANGUAGE_JSON_PATH):
        """
        Charge les données depuis le fichier JSON
        
        Args:
            json_path: Chemin vers le fichier language.json
        """
        print(f"\n📂 Chargement des données depuis {json_path}...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraire les paires source-target
        fr_data = data.get(SOURCE_LANGUAGE, {})
        
        for fr_phrase, translations in fr_data.items():
            target_translation = translations.get(self.target_language)
            
            if target_translation:
                self.raw_pairs.append((fr_phrase, target_translation))
        
        print(f"✅ {len(self.raw_pairs)} paires chargées pour {SOURCE_LANGUAGE} → {self.target_language}")
        
        return self.raw_pairs
    
    def augment_data(self, factor: int = AUGMENTATION_FACTOR):
        """
        Augmente les données
        
        Args:
            factor: Facteur de multiplication
        """
        print(f"\n📈 Augmentation des données (facteur x{factor})...")
        
        self.augmented_pairs = self.augmenter.augment_dataset(
            self.raw_pairs, 
            factor=factor
        )
        
        print(f"✅ Dataset augmenté: {len(self.raw_pairs)} → {len(self.augmented_pairs)} paires")
    
    def build_vocabularies(self):
        """Construit les vocabulaires source et cible"""
        print(f"\n📚 Construction des vocabulaires...")
        
        # Utiliser les données augmentées si disponibles, sinon les données brutes
        pairs = self.augmented_pairs if self.augmented_pairs else self.raw_pairs
        
        # Extraire les textes source et cible
        source_texts = [pair[0] for pair in pairs]
        target_texts = [pair[1] for pair in pairs]
        
        # Construire les vocabulaires
        self.source_vocab = Vocabulary(SOURCE_LANGUAGE)
        self.source_vocab.build_from_texts(source_texts)
        
        self.target_vocab = Vocabulary(self.target_language)
        self.target_vocab.build_from_texts(target_texts)
        
        # Sauvegarder les vocabulaires
        self.source_vocab.save()
        self.target_vocab.save()
        
        print(f"✅ Vocabulaires construits et sauvegardés")
        
        return self.source_vocab, self.target_vocab
    
    def create_tf_datasets(self) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
        """
        Crée les datasets TensorFlow (train, validation, test)
        
        Returns:
            Tuple de (train_dataset, val_dataset, test_dataset)
        """
        print(f"\n🔨 Création des datasets TensorFlow...")
        
        if not self.source_vocab or not self.target_vocab:
            raise ValueError("Les vocabulaires doivent être construits d'abord")
        
        # Utiliser les données augmentées
        pairs = self.augmented_pairs if self.augmented_pairs else self.raw_pairs
        
        # Encoder les paires
        encoded_pairs = []
        for source, target in pairs:
            source_ids = self.source_vocab.encode(source, add_special_tokens=True)
            target_ids = self.target_vocab.encode(target, add_special_tokens=True)
            
            # Filtrer les séquences trop longues
            if len(source_ids) <= MAX_SEQUENCE_LENGTH and len(target_ids) <= MAX_SEQUENCE_LENGTH:
                encoded_pairs.append((source_ids, target_ids))
        
        print(f"✅ {len(encoded_pairs)} paires encodées (filtré pour longueur max)")
        
        # Mélanger les données
        random.shuffle(encoded_pairs)
        
        # Split train/val/test
        total = len(encoded_pairs)
        test_size = int(total * TEST_SPLIT)
        val_size = int(total * VALIDATION_SPLIT)
        train_size = total - test_size - val_size
        
        train_pairs = encoded_pairs[:train_size]
        val_pairs = encoded_pairs[train_size:train_size + val_size]
        test_pairs = encoded_pairs[train_size + val_size:]
        
        print(f"📊 Split: Train={len(train_pairs)}, Val={len(val_pairs)}, Test={len(test_pairs)}")
        
        # Créer les datasets TensorFlow
        train_dataset = self._create_dataset_from_pairs(train_pairs, shuffle=True)
        val_dataset = self._create_dataset_from_pairs(val_pairs, shuffle=False)
        test_dataset = self._create_dataset_from_pairs(test_pairs, shuffle=False)
        
        return train_dataset, val_dataset, test_dataset
    
    def _create_dataset_from_pairs(self, pairs: List[Tuple[List[int], List[int]]], 
                                   shuffle: bool = True) -> tf.data.Dataset:
        """
        Crée un tf.data.Dataset depuis une liste de paires encodées
        
        Args:
            pairs: Liste de paires (source_ids, target_ids)
            shuffle: Mélanger les données
        
        Returns:
            tf.data.Dataset
        """
        # Séparer sources et targets
        sources = [pair[0] for pair in pairs]
        targets = [pair[1] for pair in pairs]
        
        # S'assurer que les séquences sont de la même longueur pour from_tensor_slices
        # On pad manuellement ici avant de créer le dataset
        padded_sources = tf.keras.preprocessing.sequence.pad_sequences(
            sources, maxlen=MAX_SEQUENCE_LENGTH, padding='post', value=PAD_ID
        )
        padded_targets = tf.keras.preprocessing.sequence.pad_sequences(
            targets, maxlen=MAX_SEQUENCE_LENGTH, padding='post', value=PAD_ID
        )
        
        # Créer le dataset (maintenant les données sont rectangulaires)
        # On passe ((sources, targets), targets) pour que le modèle ait accès 
        # aux deux en entrée pendant Model.fit (Teacher Forcing)
        dataset = tf.data.Dataset.from_tensor_slices(((padded_sources, padded_targets), padded_targets))
        
        if shuffle:
            dataset = dataset.shuffle(buffer_size=len(pairs))
        
        # Batching (plus besoin de padded_batch car c'est déjà padé, mais on peut le garder)
        dataset = dataset.batch(BATCH_SIZE)
        
        # Prefetch pour optimiser les performances
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_dataset_stats(self) -> Dict:
        """Retourne des statistiques sur le dataset"""
        pairs = self.augmented_pairs if self.augmented_pairs else self.raw_pairs
        
        source_lengths = [len(self.source_vocab.encode(p[0])) for p in pairs]
        target_lengths = [len(self.target_vocab.encode(p[1])) for p in pairs]
        
        return {
            'total_pairs': len(pairs),
            'source_vocab_size': len(self.source_vocab) if self.source_vocab else 0,
            'target_vocab_size': len(self.target_vocab) if self.target_vocab else 0,
            'avg_source_length': np.mean(source_lengths) if source_lengths else 0,
            'avg_target_length': np.mean(target_lengths) if target_lengths else 0,
            'max_source_length': max(source_lengths) if source_lengths else 0,
            'max_target_length': max(target_lengths) if target_lengths else 0,
        }
    
    def prepare_all(self, augment: bool = True) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
        """
        Pipeline complet de préparation des données
        
        Args:
            augment: Appliquer l'augmentation de données
        
        Returns:
            Tuple de (train_dataset, val_dataset, test_dataset)
        """
        print(f"\n{'='*60}")
        print(f"🚀 PRÉPARATION DES DONNÉES: {SOURCE_LANGUAGE} → {self.target_language}")
        print(f"{'='*60}")
        
        # 1. Charger les données
        self.load_data_from_json()
        
        # 2. Augmenter les données
        if augment:
            self.augment_data()
        
        # 3. Construire les vocabulaires
        self.build_vocabularies()
        
        # 4. Créer les datasets TensorFlow
        train_ds, val_ds, test_ds = self.create_tf_datasets()
        
        # 5. Afficher les statistiques
        stats = self.get_dataset_stats()
        print(f"\n📊 STATISTIQUES DU DATASET:")
        print(f"   - Paires totales: {stats['total_pairs']}")
        print(f"   - Vocab source: {stats['source_vocab_size']} mots")
        print(f"   - Vocab cible: {stats['target_vocab_size']} mots")
        print(f"   - Longueur moyenne source: {stats['avg_source_length']:.1f}")
        print(f"   - Longueur moyenne cible: {stats['avg_target_length']:.1f}")
        
        print(f"\n{'='*60}")
        print(f"✅ PRÉPARATION TERMINÉE")
        print(f"{'='*60}\n")
        
        return train_ds, val_ds, test_ds


def main():
    """Fonction principale pour tester la préparation des données"""
    import sys
    
    # Tester pour chaque langue
    for language in SUPPORTED_LANGUAGES:
        print(f"\n\n{'#'*70}")
        print(f"# LANGUE: {language.upper()}")
        print(f"{'#'*70}\n")
        
        builder = DatasetBuilder(language)
        train_ds, val_ds, test_ds = builder.prepare_all(augment=True)
        
        # Afficher un exemple
        print(f"\n🔍 EXEMPLE DE BATCH:")
        for source_batch, target_batch in train_ds.take(1):
            print(f"   Source shape: {source_batch.shape}")
            print(f"   Target shape: {target_batch.shape}")
            
            # Décoder le premier exemple
            source_text = builder.source_vocab.decode(source_batch[0].numpy().tolist())
            target_text = builder.target_vocab.decode(target_batch[0].numpy().tolist())
            
            print(f"\n   Exemple décodé:")
            print(f"   FR: {source_text}")
            print(f"   {language.upper()}: {target_text}")


if __name__ == "__main__":
    main()
