"""
Augmentation de données pour enrichir le dataset limité
"""
import random
import re
from typing import List, Tuple
import copy


class DataAugmenter:
    """Classe pour augmenter les données de traduction"""
    
    def __init__(self, noise_prob: float = 0.1):
        self.noise_prob = noise_prob
    
    def augment_pair(self, source: str, target: str, num_variations: int = 3) -> List[Tuple[str, str]]:
        """
        Génère des variations d'une paire source-target
        
        Args:
            source: Texte source (français)
            target: Texte cible (langue africaine)
            num_variations: Nombre de variations à générer
        
        Returns:
            Liste de paires (source, target) augmentées
        """
        variations = [(source, target)]  # Inclure l'original
        
        for _ in range(num_variations):
            # Appliquer différentes techniques d'augmentation
            aug_source, aug_target = self._apply_random_augmentation(source, target)
            variations.append((aug_source, aug_target))
        
        return variations
    
    def _apply_random_augmentation(self, source: str, target: str) -> Tuple[str, str]:
        """Applique une technique d'augmentation aléatoire"""
        techniques = [
            self._add_punctuation_variation,
            self._add_case_variation,
            self._add_spacing_variation,
            self._add_character_noise,
        ]
        
        technique = random.choice(techniques)
        return technique(source, target)
    
    def _add_punctuation_variation(self, source: str, target: str) -> Tuple[str, str]:
        """Ajoute ou modifie la ponctuation"""
        punctuations = ['.', '!', '?', '']
        
        # Retirer la ponctuation existante à la fin
        source = source.rstrip('.!?')
        target = target.rstrip('.!?')
        
        # Ajouter une ponctuation aléatoire
        punct = random.choice(punctuations)
        
        return source + punct, target + punct
    
    def _add_case_variation(self, source: str, target: str) -> Tuple[str, str]:
        """Varie la casse (majuscules/minuscules)"""
        variations = [
            lambda x: x.lower(),
            lambda x: x.capitalize(),
            lambda x: x.upper() if len(x.split()) == 1 else x.capitalize(),
        ]
        
        variation = random.choice(variations)
        
        return variation(source), variation(target)
    
    def _add_spacing_variation(self, source: str, target: str) -> Tuple[str, str]:
        """Ajoute des variations d'espacement"""
        # Normaliser les espaces multiples
        source = re.sub(r'\s+', ' ', source).strip()
        target = re.sub(r'\s+', ' ', target).strip()
        
        # Parfois ajouter des espaces supplémentaires (pour robustesse)
        if random.random() < 0.3:
            source = re.sub(r'\s', '  ', source)
            target = re.sub(r'\s', '  ', target)
        
        return source, target
    
    def _add_character_noise(self, source: str, target: str) -> Tuple[str, str]:
        """Ajoute un bruit de caractères léger (pour robustesse)"""
        # Ne pas ajouter de bruit trop souvent
        if random.random() > self.noise_prob:
            return source, target
        
        # Ajouter du bruit seulement au source (français)
        # Cela aide le modèle à être robuste aux fautes de frappe
        noisy_source = self._add_char_noise_to_text(source)
        
        return noisy_source, target
    
    def _add_char_noise_to_text(self, text: str) -> str:
        """Ajoute du bruit à un texte"""
        chars = list(text)
        
        if len(chars) < 3:
            return text
        
        # Choisir une position aléatoire (pas au début/fin)
        pos = random.randint(1, len(chars) - 2)
        
        noise_type = random.choice(['swap', 'duplicate', 'delete'])
        
        if noise_type == 'swap' and pos < len(chars) - 1:
            # Échanger deux caractères adjacents
            chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
        elif noise_type == 'duplicate':
            # Dupliquer un caractère
            chars.insert(pos, chars[pos])
        elif noise_type == 'delete':
            # Supprimer un caractère
            chars.pop(pos)
        
        return ''.join(chars)
    
    def augment_dataset(self, pairs: List[Tuple[str, str]], factor: int = 5) -> List[Tuple[str, str]]:
        """
        Augmente un dataset complet
        
        Args:
            pairs: Liste de paires (source, target)
            factor: Facteur de multiplication du dataset
        
        Returns:
            Dataset augmenté
        """
        augmented = []
        
        for source, target in pairs:
            # Ajouter l'original
            augmented.append((source, target))
            
            # Générer des variations
            variations = self.augment_pair(source, target, num_variations=factor - 1)
            augmented.extend(variations[1:])  # Exclure l'original (déjà ajouté)
        
        print(f"📈 Dataset augmenté: {len(pairs)} → {len(augmented)} paires (x{factor})")
        
        return augmented


class ContextualAugmenter:
    """Augmentation contextuelle en ajoutant des variations sémantiques"""
    
    def __init__(self):
        # Variations contextuelles pour les salutations
        self.contextual_variations = {
            'bonjour': ['salut', 'hello', 'coucou', 'bonsoir', 'bon matin'],
            'merci': ['merci beaucoup', 'merci bien', 'grand merci'],
            'au revoir': ['à bientôt', 'à plus tard', 'bye', 'salut'],
            'comment allez-vous': ['comment vas-tu', 'comment ça va', 'ça va'],
            'oui': ['ok', 'd\'accord', 'bien sûr'],
            'non': ['pas du tout', 'jamais', 'négatif'],
        }
    
    def get_variations(self, source: str) -> List[str]:
        """Retourne des variations contextuelles d'une phrase source"""
        source_lower = source.lower().strip('.!?')
        
        if source_lower in self.contextual_variations:
            return self.contextual_variations[source_lower]
        
        return []
