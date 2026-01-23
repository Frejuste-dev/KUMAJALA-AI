"""
Gestion des vocabulaires pour les langues sources et cibles
"""
import json
import os
from typing import Dict, List, Set
from collections import Counter
import pickle

from ml.config import (
    PAD_TOKEN, START_TOKEN, END_TOKEN, UNK_TOKEN,
    PAD_ID, START_ID, END_ID, UNK_ID,
    SPECIAL_TOKENS, MIN_VOCAB_FREQUENCY,
    VOCAB_FILE_TEMPLATE
)


class Vocabulary:
    """Classe pour gérer le vocabulaire d'une langue"""
    
    def __init__(self, language: str):
        self.language = language
        self.word2idx: Dict[str, int] = {}
        self.idx2word: Dict[int, str] = {}
        self.word_counts: Counter = Counter()
        
        # Initialiser avec les tokens spéciaux
        self._init_special_tokens()
    
    def _init_special_tokens(self):
        """Initialise les tokens spéciaux"""
        special_mapping = {
            PAD_TOKEN: PAD_ID,
            START_TOKEN: START_ID,
            END_TOKEN: END_ID,
            UNK_TOKEN: UNK_ID
        }
        
        for token, idx in special_mapping.items():
            self.word2idx[token] = idx
            self.idx2word[idx] = token
    
    def build_from_texts(self, texts: List[str], min_frequency: int = MIN_VOCAB_FREQUENCY):
        """
        Construit le vocabulaire à partir d'une liste de textes
        
        Args:
            texts: Liste de textes
            min_frequency: Fréquence minimale pour inclure un mot
        """
        # Compter les mots
        for text in texts:
            words = self._tokenize(text)
            self.word_counts.update(words)
        
        # Ajouter les mots au vocabulaire (triés par fréquence)
        next_idx = len(SPECIAL_TOKENS)
        for word, count in self.word_counts.most_common():
            if count >= min_frequency and word not in self.word2idx:
                self.word2idx[word] = next_idx
                self.idx2word[next_idx] = word
                next_idx += 1
        
        print(f"✅ Vocabulaire {self.language}: {len(self.word2idx)} mots (min_freq={min_frequency})")
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenise un texte en mots
        Pour les langues africaines, on utilise une tokenisation simple par espaces
        """
        # Normaliser le texte
        text = text.lower().strip()
        
        # Séparer par espaces et ponctuation
        # On garde la ponctuation comme tokens séparés
        import re
        tokens = re.findall(r'\w+|[^\w\s]', text)
        
        return tokens
    
    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """
        Encode un texte en séquence d'indices
        
        Args:
            text: Texte à encoder
            add_special_tokens: Ajouter START et END tokens
        
        Returns:
            Liste d'indices
        """
        tokens = self._tokenize(text)
        indices = [self.word2idx.get(token, UNK_ID) for token in tokens]
        
        if add_special_tokens:
            indices = [START_ID] + indices + [END_ID]
        
        return indices
    
    def decode(self, indices: List[int], skip_special_tokens: bool = True) -> str:
        """
        Décode une séquence d'indices en texte
        
        Args:
            indices: Liste d'indices
            skip_special_tokens: Ignorer les tokens spéciaux
        
        Returns:
            Texte décodé
        """
        words = []
        for idx in indices:
            word = self.idx2word.get(idx, UNK_TOKEN)
            
            if skip_special_tokens and word in SPECIAL_TOKENS:
                continue
            
            words.append(word)
        
        # Reconstruire le texte
        text = " ".join(words)
        
        # Nettoyer les espaces autour de la ponctuation
        import re
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        return text
    
    def __len__(self) -> int:
        """Retourne la taille du vocabulaire"""
        return len(self.word2idx)
    
    def save(self, filepath: str = None):
        """Sauvegarde le vocabulaire"""
        if filepath is None:
            filepath = VOCAB_FILE_TEMPLATE.format(language=self.language)
        
        vocab_data = {
            'language': self.language,
            'word2idx': self.word2idx,
            'idx2word': {int(k): v for k, v in self.idx2word.items()},
            'word_counts': dict(self.word_counts)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(vocab_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Vocabulaire sauvegardé: {filepath}")
    
    @classmethod
    def load(cls, filepath: str = None, language: str = None):
        """Charge un vocabulaire depuis un fichier"""
        if filepath is None and language is None:
            raise ValueError("Spécifier filepath ou language")
        
        if filepath is None:
            filepath = VOCAB_FILE_TEMPLATE.format(language=language)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        vocab = cls(vocab_data['language'])
        vocab.word2idx = vocab_data['word2idx']
        vocab.idx2word = {int(k): v for k, v in vocab_data['idx2word'].items()}
        vocab.word_counts = Counter(vocab_data['word_counts'])
        
        print(f"📂 Vocabulaire chargé: {filepath} ({len(vocab)} mots)")
        return vocab
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur le vocabulaire"""
        return {
            'language': self.language,
            'vocab_size': len(self),
            'total_words': sum(self.word_counts.values()),
            'unique_words': len(self.word_counts),
            'most_common': self.word_counts.most_common(10),
            'coverage': len(self.word_counts) / len(self) if len(self) > 0 else 0
        }
