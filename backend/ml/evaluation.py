"""
Évaluation et métriques pour le modèle de traduction
"""
import tensorflow as tf
import numpy as np
from typing import List, Dict, Tuple
import argparse
import json
from datetime import datetime

from ml.config import MODEL_DIR, SUPPORTED_LANGUAGES
from ml.vocabulary import Vocabulary
from ml.model_architecture import Seq2SeqModel
from ml.data_preparation import DatasetBuilder


def calculate_bleu_score(references: List[str], hypotheses: List[str], max_order: int = 4) -> Dict[str, float]:
    """
    Calcule le score BLEU
    
    Args:
        references: Liste de traductions de référence
        hypotheses: Liste de traductions générées
        max_order: Ordre maximum des n-grammes (4 pour BLEU-4)
    
    Returns:
        Dictionnaire avec les scores BLEU
    """
    try:
        import sacrebleu
        
        # sacrebleu attend une liste de listes pour les références
        refs = [[ref] for ref in references]
        
        # Calculer BLEU
        bleu = sacrebleu.corpus_bleu(hypotheses, list(zip(*refs)))
        
        return {
            'bleu': bleu.score,
            'bleu_1': bleu.precisions[0],
            'bleu_2': bleu.precisions[1],
            'bleu_3': bleu.precisions[2],
            'bleu_4': bleu.precisions[3],
        }
    except ImportError:
        print("⚠️ sacrebleu non installé, utilisation d'une implémentation simple")
        return _simple_bleu(references, hypotheses, max_order)


def _simple_bleu(references: List[str], hypotheses: List[str], max_order: int = 4) -> Dict[str, float]:
    """Implémentation simple du BLEU score"""
    from collections import Counter
    
    def get_ngrams(tokens: List[str], n: int) -> Counter:
        """Extrait les n-grammes"""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngrams.append(tuple(tokens[i:i+n]))
        return Counter(ngrams)
    
    precisions = []
    
    for n in range(1, max_order + 1):
        matches = 0
        total = 0
        
        for ref, hyp in zip(references, hypotheses):
            ref_tokens = ref.split()
            hyp_tokens = hyp.split()
            
            ref_ngrams = get_ngrams(ref_tokens, n)
            hyp_ngrams = get_ngrams(hyp_tokens, n)
            
            # Compter les matches
            for ngram in hyp_ngrams:
                if ngram in ref_ngrams:
                    matches += min(hyp_ngrams[ngram], ref_ngrams[ngram])
            
            total += max(len(hyp_tokens) - n + 1, 0)
        
        precision = matches / total if total > 0 else 0
        precisions.append(precision * 100)
    
    # Calculer le score BLEU géométrique
    if min(precisions) > 0:
        bleu = np.exp(np.mean([np.log(p) for p in precisions]))
    else:
        bleu = 0
    
    return {
        'bleu': bleu,
        'bleu_1': precisions[0] if len(precisions) > 0 else 0,
        'bleu_2': precisions[1] if len(precisions) > 1 else 0,
        'bleu_3': precisions[2] if len(precisions) > 2 else 0,
        'bleu_4': precisions[3] if len(precisions) > 3 else 0,
    }


class ModelEvaluator:
    """Classe pour évaluer un modèle de traduction"""
    
    def __init__(self, target_language: str, model_path: str = None):
        self.target_language = target_language
        
        # Charger les vocabulaires
        self.source_vocab = Vocabulary.load(language='fr')
        self.target_vocab = Vocabulary.load(language=target_language)
        
        # Charger le modèle
        if model_path is None:
            model_path = f"{MODEL_DIR}/{target_language}_model"
        
        print(f"📂 Chargement du modèle depuis {model_path}...")
        self.model = tf.keras.models.load_model(model_path, compile=False)
        print(f"✅ Modèle chargé")
    
    def translate_text(self, text: str) -> Tuple[str, np.ndarray]:
        """
        Traduit un texte
        
        Args:
            text: Texte source (français)
        
        Returns:
            Tuple de (traduction, attention_weights)
        """
        # Encoder le texte source
        source_ids = self.source_vocab.encode(text, add_special_tokens=True)
        
        # Traduire
        translation, attention_weights = self.model.translate(
            source_ids, self.source_vocab, self.target_vocab
        )
        
        return translation, attention_weights
    
    def evaluate_on_dataset(self, test_ds) -> Dict:
        """
        Évalue le modèle sur un dataset de test
        
        Args:
            test_ds: Dataset de test TensorFlow
        
        Returns:
            Dictionnaire de métriques
        """
        print(f"\n{'='*60}")
        print(f"📊 ÉVALUATION SUR LE DATASET DE TEST")
        print(f"{'='*60}\n")
        
        references = []
        hypotheses = []
        total_time = 0
        num_samples = 0
        
        for (source_batch, _), target_batch in test_ds:
            batch_size = source_batch.shape[0]
            
            for i in range(batch_size):
                # Décoder la référence
                reference = self.target_vocab.decode(
                    target_batch[i].numpy().tolist(),
                    skip_special_tokens=True
                )
                
                # Traduire
                import time
                start_time = time.time()
                
                hypothesis, _ = self.model.translate(
                    source_batch[i].numpy().tolist(),
                    self.source_vocab,
                    self.target_vocab
                )
                
                elapsed = time.time() - start_time
                total_time += elapsed
                
                references.append(reference)
                hypotheses.append(hypothesis)
                num_samples += 1
        
        # Calculer les métriques
        bleu_scores = calculate_bleu_score(references, hypotheses)
        avg_time = total_time / num_samples if num_samples > 0 else 0
        
        results = {
            'num_samples': num_samples,
            'avg_inference_time': avg_time,
            **bleu_scores
        }
        
        # Afficher les résultats
        print(f"\n📈 RÉSULTATS:")
        print(f"   Échantillons: {num_samples}")
        print(f"   BLEU Score: {bleu_scores['bleu']:.2f}")
        print(f"   BLEU-1: {bleu_scores['bleu_1']:.2f}")
        print(f"   BLEU-2: {bleu_scores['bleu_2']:.2f}")
        print(f"   BLEU-3: {bleu_scores['bleu_3']:.2f}")
        print(f"   BLEU-4: {bleu_scores['bleu_4']:.2f}")
        print(f"   Temps moyen d'inférence: {avg_time*1000:.2f}ms")
        
        return results
    
    def evaluate_on_examples(self, examples: List[Tuple[str, str]]) -> Dict:
        """
        Évalue le modèle sur des exemples spécifiques
        
        Args:
            examples: Liste de paires (source, target)
        
        Returns:
            Dictionnaire de résultats
        """
        print(f"\n{'='*60}")
        print(f"🔍 ÉVALUATION SUR DES EXEMPLES")
        print(f"{'='*60}\n")
        
        results = []
        
        for i, (source, reference) in enumerate(examples, 1):
            # Traduire
            translation, attention = self.translate_text(source)
            
            # Calculer BLEU pour cet exemple
            bleu = calculate_bleu_score([reference], [translation])
            
            result = {
                'source': source,
                'reference': reference,
                'translation': translation,
                'bleu': bleu['bleu']
            }
            results.append(result)
            
            # Afficher
            print(f"Exemple {i}:")
            print(f"   Source: {source}")
            print(f"   Référence: {reference}")
            print(f"   Traduction: {translation}")
            print(f"   BLEU: {bleu['bleu']:.2f}")
            print()
        
        return results
    
    def generate_report(self, results: Dict, output_path: str = None):
        """
        Génère un rapport d'évaluation
        
        Args:
            results: Résultats de l'évaluation
            output_path: Chemin de sauvegarde du rapport
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{MODEL_DIR}/evaluation_report_{self.target_language}_{timestamp}.json"
        
        report = {
            'language': self.target_language,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Rapport sauvegardé: {output_path}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Évaluer un modèle de traduction')
    parser.add_argument(
        '--target-language',
        type=str,
        choices=SUPPORTED_LANGUAGES,
        required=True,
        help='Langue cible'
    )
    parser.add_argument(
        '--model-path',
        type=str,
        help='Chemin vers le modèle (optionnel)'
    )
    parser.add_argument(
        '--examples-only',
        action='store_true',
        help='Évaluer seulement sur des exemples prédéfinis'
    )
    
    args = parser.parse_args()
    
    # Créer l'évaluateur
    evaluator = ModelEvaluator(args.target_language, args.model_path)
    
    if args.examples_only:
        # Exemples prédéfinis
        examples = [
            ("bonjour", "Akwaba"),
            ("merci", "Akpé"),
            ("comment allez-vous?", "Bi ye né?"),
            ("au revoir", "Kan na"),
        ]
        
        results = evaluator.evaluate_on_examples(examples)
    else:
        # Évaluer sur le dataset de test
        builder = DatasetBuilder(args.target_language)
        builder.load_data_from_json()
        builder.augment_data()
        builder.build_vocabularies()
        _, _, test_ds = builder.create_tf_datasets()
        
        results = evaluator.evaluate_on_dataset(test_ds)
        
        # Générer un rapport
        evaluator.generate_report(results)


if __name__ == "__main__":
    main()
