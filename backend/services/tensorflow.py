"""
Service de traduction utilisant TensorFlow
"""
import os
import tensorflow as tf
import numpy as np
from typing import Optional, Tuple, Dict
import time

from ml.config import MODEL_DIR, SUPPORTED_LANGUAGES, CONFIDENCE_THRESHOLD
from ml.vocabulary import Vocabulary


class TensorFlowTranslationService:
    """Service de traduction avec TensorFlow"""
    
    def __init__(self):
        self.models: Dict[str, tf.keras.Model] = {}
        self.source_vocabs: Dict[str, Vocabulary] = {}
        self.target_vocabs: Dict[str, Vocabulary] = {}
        self.is_available = False
        
        # Charger les modèles au démarrage
        self._load_models()
    
    def _load_models(self):
        """Charge tous les modèles disponibles"""
        print("\n🤖 Initialisation du service TensorFlow...")
        
        loaded_count = 0
        
        for language in SUPPORTED_LANGUAGES:
            try:
                model_path = os.path.join(MODEL_DIR, f"{language}_model")
                
                # Vérifier si le modèle existe
                if not os.path.exists(model_path):
                    print(f"⚠️  Modèle {language} non trouvé: {model_path}")
                    continue
                
                # Charger le modèle
                print(f"   Chargement du modèle {language}...")
                model = tf.keras.models.load_model(model_path, compile=False)
                
                # Charger les vocabulaires
                source_vocab = Vocabulary.load(language='fr')
                target_vocab = Vocabulary.load(language=language)
                
                # Stocker
                self.models[language] = model
                self.source_vocabs[language] = source_vocab
                self.target_vocabs[language] = target_vocab
                
                loaded_count += 1
                print(f"   ✅ Modèle {language} chargé")
                
            except Exception as e:
                print(f"   ❌ Erreur lors du chargement du modèle {language}: {e}")
        
        if loaded_count > 0:
            self.is_available = True
            print(f"\n✅ Service TensorFlow initialisé ({loaded_count}/{len(SUPPORTED_LANGUAGES)} modèles)")
        else:
            print(f"\n⚠️  Aucun modèle TensorFlow disponible")
            print(f"   Les modèles doivent être entraînés avec: python -m ml.training --target-language <langue>")
    
    def translate_text(self, text: str, target_language: str) -> Optional[Tuple[str, float]]:
        """
        Traduit un texte vers une langue cible
        
        Args:
            text: Texte source (français)
            target_language: Langue cible
        
        Returns:
            Tuple de (traduction, score_de_confiance) ou None si échec
        """
        if not self.is_available:
            return None
        
        if target_language not in self.models:
            print(f"⚠️  Modèle {target_language} non disponible")
            return None
        
        try:
            # Récupérer le modèle et les vocabulaires
            model = self.models[target_language]
            source_vocab = self.source_vocabs[target_language]
            target_vocab = self.target_vocabs[target_language]
            
            # Encoder le texte source
            source_ids = source_vocab.encode(text, add_special_tokens=True)
            
            # Traduire
            start_time = time.time()
            translation, attention_weights = model.translate(
                source_ids, source_vocab, target_vocab
            )
            inference_time = time.time() - start_time
            
            # Calculer un score de confiance basé sur l'attention
            # Plus l'attention est concentrée, plus on est confiant
            confidence = self._calculate_confidence(attention_weights, inference_time)
            
            print(f"🔄 TensorFlow: '{text}' → '{translation}' (confiance: {confidence:.2f})")
            
            return translation, confidence
            
        except Exception as e:
            print(f"❌ Erreur TensorFlow pour '{text}' en {target_language}: {e}")
            return None
    
    def _calculate_confidence(self, attention_weights: np.ndarray, inference_time: float) -> float:
        """
        Calcule un score de confiance basé sur les poids d'attention
        
        Args:
            attention_weights: Poids d'attention [target_len, source_len, 1]
            inference_time: Temps d'inférence en secondes
        
        Returns:
            Score de confiance entre 0 et 1
        """
        if attention_weights.size == 0:
            return 0.5
        
        # Calculer l'entropie de l'attention (plus c'est concentré, mieux c'est)
        # Normaliser les poids
        weights = attention_weights.squeeze()
        
        if weights.ndim == 1:
            weights = weights.reshape(1, -1)
        
        # Calculer l'entropie moyenne
        entropies = []
        for row in weights:
            # Normaliser
            row = row / (row.sum() + 1e-10)
            # Entropie
            entropy = -np.sum(row * np.log(row + 1e-10))
            entropies.append(entropy)
        
        avg_entropy = np.mean(entropies)
        
        # Normaliser l'entropie (0 = très confiant, log(len) = pas confiant)
        max_entropy = np.log(weights.shape[1])
        normalized_entropy = avg_entropy / (max_entropy + 1e-10)
        
        # Score de confiance (inverse de l'entropie normalisée)
        attention_confidence = 1.0 - normalized_entropy
        
        # Pénaliser si l'inférence est trop lente (> 1 seconde)
        time_penalty = 1.0 if inference_time < 1.0 else 0.8
        
        # Score final
        confidence = attention_confidence * time_penalty
        
        return float(np.clip(confidence, 0.0, 1.0))
    
    def is_service_available(self) -> bool:
        """Vérifie si le service est disponible"""
        return self.is_available
    
    def get_available_languages(self) -> list:
        """Retourne la liste des langues disponibles"""
        return list(self.models.keys())
    
    def get_model_info(self, language: str) -> Optional[Dict]:
        """Retourne des informations sur un modèle"""
        if language not in self.models:
            return None
        
        model = self.models[language]
        source_vocab = self.source_vocabs[language]
        target_vocab = self.target_vocabs[language]
        
        return {
            'language': language,
            'source_vocab_size': len(source_vocab),
            'target_vocab_size': len(target_vocab),
            'model_loaded': True
        }


# Instance globale du service
_tf_service = None


def get_tensorflow_service() -> TensorFlowTranslationService:
    """Retourne l'instance du service TensorFlow (singleton)"""
    global _tf_service
    
    if _tf_service is None:
        _tf_service = TensorFlowTranslationService()
    
    return _tf_service
