"""
Script pour enrichir le dataset de traduction en utilisant Gemini AI.
Génère de nouvelles paires de traduction pour augmenter le volume de données d'entraînement.
"""
import os
import json
import time
import argparse
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importer le service Gemini
from services.gemini import GeminiService
from ml.config import SUPPORTED_LANGUAGES, LANGUAGE_JSON_PATH, DATA_DIR

class DatasetEnricher:
    def __init__(self):
        self.gemini = GeminiService()
        if not self.gemini.is_service_available():
            print("❌ Erreur: Le service Gemini n'est pas disponible. Vérifiez votre GEMINI_API_KEY.")
            
    def generate_translations(self, target_language: str, count: int = 50) -> Dict[str, str]:
        """
        Génère 'count' nouvelles paires de traduction pour une langue cible avec retry.
        """
        if not self.gemini.is_service_available():
            print(f"⚠️  Service Gemini indisponible pour {target_language}. On passe.")
            return {}

        print(f"🚀 Génération de {count} nouvelles paires pour le {target_language}...")
        
        # Charger les données existantes pour éviter les doublons et donner des exemples
        existing_data = self._load_existing_data(target_language)
        examples_str = "\n".join([f"- French: '{fr}' -> {target_language.capitalize()}: '{tg}'" 
                                 for fr, tg in list(existing_data.items())[:10]])

        prompt = f"""
        Tu es un expert linguiste spécialisé dans les langues africaines, en particulier le {target_language}.
        Ton objectif est de générer {count} nouvelles paires de traduction uniques du Français vers le {target_language}.
        Ces paires seront utilisées pour entraîner un modèle de traduction automatique.

        Voici quelques exemples existants pour t'inspirer du style et du vocabulaire :
        {examples_str}

        Consignes :
        1. Les phrases doivent être variées : conversations quotidiennes, besoins de base, expressions courantes, questions, etc.
        2. Les phrases doivent être relativement courtes (entre 1 et 10 mots).
        3. Assure-toi que les traductions en {target_language} sont authentiques et naturelles.
        4. Ne répète PAS les exemples fournis.
        5. Retourne UNIQUEMENT un objet JSON valide où la clé est la phrase en français et la valeur est sa traduction en {target_language}.
        6. Le format doit être strictement : {{"phrase fr 1": "traduction target 1", "phrase fr 2": "traduction target 2", ...}}

        Génère {count} paires maintenant :
        """

        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                # On utilise le modèle Gemini pour générer le contenu
                response = self.gemini.model.generate_content(prompt)
                
                # Nettoyer la réponse pour extraire le JSON
                content = response.text.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                new_pairs = json.loads(content)
                print(f"✅ {len(new_pairs)} nouvelles paires générées avec succès.")
                return new_pairs
                
            except Exception as e:
                print(f"⚠️ Erreur lors de l'essai {attempt + 1}/{max_retries}: {e}")
                if "429" in str(e):
                    print(f"⏳ Quota atteint. Attente de {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Backoff exponentiel
                else:
                    break
        
        return {}
    def _load_existing_data(self, target_language: str) -> Dict[str, str]:
        """Charge les données existantes pour une langue donnée."""
        if not os.path.exists(LANGUAGE_JSON_PATH):
            return {}
            
        with open(LANGUAGE_JSON_PATH, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            
        fr_data = full_data.get('fr', {})
        result = {}
        for fr_text, translations in fr_data.items():
            if target_language in translations:
                result[fr_text] = translations[target_language]
        return result

    def enrich_all(self, count_per_lang: int = 50):
        """Enrichit le dataset pour toutes les langues supportées."""
        if not os.path.exists(LANGUAGE_JSON_PATH):
            print(f"❌ Fichier source non trouvé: {LANGUAGE_JSON_PATH}")
            return

        with open(LANGUAGE_JSON_PATH, 'r', encoding='utf-8') as f:
            full_data = json.load(f)

        for lang in SUPPORTED_LANGUAGES:
            new_data = self.generate_translations(lang, count_per_lang)
            
            # Intégrer dans full_data['fr']
            for fr_text, translation in new_data.items():
                if fr_text not in full_data['fr']:
                    full_data['fr'][fr_text] = {}
                full_data['fr'][fr_text][lang] = translation
            
            # Petit délai pour éviter de saturer l'API
            time.sleep(2)

        # Sauvegarder les résultats
        output_path = os.path.join(DATA_DIR, "language_enriched.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
            
        print(f"\n✨ Dataset enrichi sauvegardé dans: {output_path}")
        print(f"💡 Vous pouvez maintenant remplacer 'language.json' par ce fichier ou l'utiliser pour l'entraînement.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enrichir le dataset Kumajala via Gemini')
    parser.add_argument('--count', type=int, default=50, help='Nombre de paires à générer par langue')
    args = parser.parse_args()
    
    enricher = DatasetEnricher()
    enricher.enrich_all(args.count)
