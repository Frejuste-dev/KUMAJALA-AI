import os
import tempfile
from google.cloud import firestore
import json

class FirestoreService:

    def __init__(self):
        # Initialisation du client Firestore
        creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        self.load_local_translations()
    
        if creds_json:
            try:
                # Écrire temporairement le JSON dans un fichier
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    f.write(creds_json)
                    temp_path = f.name
            
                # Configurer la variable d'environnement pour que Firestore la trouve
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_path
                
                # Maintenant initialiser Firestore
                self.db = firestore.Client()
                self.use_local_data = False
                print("✅ Service Firestore initialisé avec succès (credentials depuis variable d'env).")
            except Exception as e:
                print(f"❌ Erreur connexion Firestore: {e}. Fallback vers les données locales.")
                self.use_local_data = True
                # self.load_local_translations()
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                self.db = firestore.Client()
                self.use_local_data = False
                print("✅ Service Firestore initialisé avec succès (chemin fichier credentials).")
            except Exception as e:
                print(f"❌ Erreur connexion Firestore: {e}. Fallback vers les données locales.")
                self.use_local_data = True
                # self.load_local_translations()
        else:
            print("⚠️ GOOGLE_APPLICATION_CREDENTIALS non définie. Utilisation des données locales.")
            self.use_local_data = True
            # self.load_local_translations()

        # Métadonnées des langues (hardcodées pour le MVP du hackathon)
        self._language_metadata = {
            'bété': {'code': 'bété', 'name': 'Bété', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'baoulé': {'code': 'baoulé', 'name': 'Baoulé', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'mooré': {'code': 'mooré', 'name': 'Mooré', 'region': 'Burkina Faso', 'code_gtts': 'fr'},
            'agni': {'code': 'agni', 'name': 'Agni', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'fr': {'code': 'fr', 'name': 'Français', 'region': 'Global', 'code_gtts': 'fr'}
        }

    def load_local_translations(self):
        """Charge les traductions depuis le fichier JSON local (data/language.json)."""
        try:
            script_dir = os.path.dirname(__file__)
            json_path = os.path.join(script_dir, '..', 'data', 'language.json') # Chemin vers language.json

            with open(json_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self.local_translations = {}
                # Assurez-vous que la structure "fr" existe au niveau supérieur
                if "fr" in raw_data:
                    self.local_translations["fr"] = {
                        k.lower(): v for k, v in raw_data["fr"].items()
                    }
                else:
                    # Si la structure n'a pas de clé "fr" au premier niveau,
                    # considérez que raw_data est directement le dictionnaire des traductions.
                    # Adaptez ceci si votre fichier JSON a une structure racine différente.
                    self.local_translations = raw_data
                print(f"INFO: Traductions locales chargées depuis {json_path}.")

        except FileNotFoundError:
            print("WARN: Fichier data/language.json non trouvé. Création de données par défaut.")
            self.local_translations = {
                "fr": {
                    "bonjour": {
                        "bété": "Akwaba", "baoulé": "Mo ho", "mooré": "Ne y windga", "agni": "Agni oh"
                    },
                    "comment allez-vous?": {
                        "bété": "Bi ye né?", "baoulé": "Wo ho tè n?", "mooré": "Fo laafi?", "agni": "Aka kye?"
                    },
                    "merci": {
                        "bété": "Akpé", "baoulé": "Mo", "mooré": "Barika", "agni": "Akpé"
                    },
                    "au revoir": {
                        "bété": "Kan na", "baoulé": "Kan na", "mooré": "Nan kã pãalem", "agni": "Aka na"
                    },
                    "oui": {
                        "bété": "Yoo", "baoulé": "Yoo", "mooré": "Yãa", "agni": "Aoo"
                    },
                    "non": {
                        "bété": "Kou", "baoulé": "Kou", "mooré": "Ayi", "agni": "N'an"
                    },
                    "bonne nuit": {
                        "bété": "Dè wèlè", "baoulé": "Dè wèlè", "mooré": "Sẽn-doogo", "agni": "Anwielé"
                    },
                    "je m'appelle": {
                        "bété": "Man yi tɔ", "baoulé": "Man yi tɔ", "mooré": "Ma yiire", "agni": "Mina yɛ"
                    },
                    "où est": {
                        "bété": "Kpá nyɛ", "baoulé": "Kpá nyɛ", "mooré": "Fo bee", "agni": "Wan ye?"
                    },
                    "combien": {
                        "bété": "Kpé nyɛ", "baoulé": "Kpé nyɛ", "mooré": "Kpé nyɛ", "agni": "Kye o?"
                    },
                    "s'il vous plaît": {
                        "bété": "Akpé o", "baoulé": "Akpé o", "mooré": "Tõnd pa", "agni": "Kpaa"
                    },
                    "excusez-moi": {
                        "bété": "Pardon", "baoulé": "Pardon", "mooré": "Tõnd wii", "agni": "Pardon"
                    },
                    "ça va": {
                        "bété": "Bi dè", "baoulé": "Wo dè", "mooré": "A laafi", "agni": "Aka ya?"
                    },
                    "boire": {
                        "bété": "Nyɛ", "baoulé": "Nyɛ", "mooré": "Nyu", "agni": "Nyu"
                    },
                    "manger": {
                        "bété": "Dyi", "baoulé": "Dyi", "mooré": "Di", "agni": "Di"
                    },
                    "dormir": {
                        "bété": "Dè", "baoulé": "Dè", "mooré": "Sẽn", "agni": "Dè"
                    },
                    "maison": {
                        "bété": "Kpè", "baoulé": "Kpè", "mooré": "Yiri", "agni": "Aso"
                    },
                    "eau": {
                        "bété": "Nyɛ", "baoulé": "Nyɛ", "mooré": "Koom", "agni": "Nsu"
                    },
                    "argent": {
                        "bété": "Kpɛ", "baoulé": "Kpɛ", "mooré": "Galaga", "agni": "Sika"
                    },
                    "travail": {
                        "bété": "Wɔ", "baoulé": "Wɔ", "mooré": "Tuma", "agni": "Adwuma"
                    }
                }
            }
            self._save_local_translations_to_file() # Sauvegarde les données par défaut
        except Exception as e:
            print(f"❌ Erreur lors du chargement des traductions locales: {e}")
            self.local_translations = {"fr": {}} # Assure que le dictionnaire est toujours initialisé

    def _save_local_translations_to_file(self):
        """Sauvegarde les données locales dans le fichier JSON (data/language.json)."""
        try:
            script_dir = os.path.dirname(__file__)
            json_path = os.path.join(script_dir, '..', 'data', 'language.json') # Chemin vers language.json
            os.makedirs(os.path.dirname(json_path), exist_ok=True) # Crée le dossier 'data' si inexistant
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.local_translations, f, ensure_ascii=False, indent=2)
            print(f"INFO: Traductions locales sauvegardées dans {json_path}.")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des traductions locales dans le fichier: {e}")

    def get_translation(self, text, target_language):
        """Récupère une traduction depuis Firestore ou les données locales"""
        text_lower = text.lower()
        if self.use_local_data:
            return self._get_local_translation(text_lower, target_language)
        else:
            result = self._get_firestore_translation(text_lower, target_language)
            if result is None :
                print(f"DEBUG: Pas trouvé dans Firestore, fallback vers données locales pour '{text_lower}'")
                return self._get_local_translation(text_lower, target_language)
            return result
                

    def _get_local_translation(self, text_lower, target_language):
        """Récupère une traduction depuis les données locales"""
        translations = self.local_translations.get("fr", {})
        if text_lower in translations and target_language in translations[text_lower]:
            return translations[text_lower][target_language]
        return None

    def _get_firestore_translation(self, text_lower, target_language):
        """Récupère une traduction depuis Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text_lower)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                return data.get(target_language)
            return None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération Firestore: {e}")
            return None

    def save_translation(self, text, target_language, translation):
        """Sauvegarde une traduction dans Firestore ou localement"""
        text_lower = text.lower()
        if self.use_local_data:
            return self._save_local_translation(text_lower, target_language, translation)
        else:
            return self._save_firestore_translation(text_lower, target_language, translation)

    def _save_local_translation(self, text_lower, target_language, translation):
        """Sauvegarde une traduction localement"""
        try:
            if "fr" not in self.local_translations:
                self.local_translations["fr"] = {}

            if text_lower not in self.local_translations["fr"]:
                self.local_translations["fr"][text_lower] = {}

            self.local_translations["fr"][text_lower][target_language] = translation

            self._save_local_translations_to_file() # Sauvegarde après chaque modification

            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde locale: {e}")
            return False

    def _save_firestore_translation(self, text_lower, target_language, translation):
        """Sauvegarde une traduction dans Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text_lower)
            doc_ref.set({
                target_language: translation
            }, merge=True) # Utiliser set avec merge=True pour ajouter/mettre à jour un champ sans écraser le document entier
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde Firestore: {e}")
            return False

    def update_translation_manual(self, french_text: str, target_language: str, new_translation: str) -> bool:
        """
        Met à jour ou ajoute manuellement une traduction spécifique.
        Ceci est utilisé pour corriger ou ajouter des traductions.
        """
        french_text_lower = french_text.lower()
        print(f"DEBUG: Tentative de mise à jour manuelle: '{french_text}' en '{target_language}' avec '{new_translation}'")

        if self.use_local_data:
            try:
                if "fr" not in self.local_translations:
                    self.local_translations["fr"] = {}
                if french_text_lower not in self.local_translations["fr"]:
                    self.local_translations["fr"][french_text_lower] = {}

                self.local_translations["fr"][french_text_lower][target_language] = new_translation
                self._save_local_translations_to_file() # Sauvegarde après chaque modification manuelle
                print(f"INFO: Traduction locale mise à jour/ajoutée pour '{french_text_lower}' en '{target_language}'.")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour manuelle locale: {e}")
                return False
        else:
            try:
                doc_ref = self.db.collection('translations').document(french_text_lower)
                doc_ref.set({
                    target_language: new_translation
                }, merge=True)
                print(f"INFO: Traduction Firestore mise à jour/ajoutée pour '{french_text_lower}' en '{target_language}'.")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour manuelle Firestore: {e}")
                return False

    def get_supported_languages(self):
        """
        Retourne la liste des langues supportées (hardcodée pour le MVP du hackathon).
        """
        # Retourne simplement les valeurs du dictionnaire _language_metadata
        # Trié par nom de langue pour un affichage cohérent
        return sorted(self._language_metadata.values(), key=lambda x: x['name'])

    def save_contact_message(self, contact_data):
        """
        Sauvegarde un message de contact dans Firestore ou localement.
        
        Args:
            contact_data (dict): Données du formulaire de contact
                {
                    'name': str,
                    'email': str,
                    'subject': str,
                    'message': str,
                    'timestamp': str,
                    'status': str
                }
        
        Returns:
            str: ID du document créé
        """
        if self.use_local_data:
            # Mode local: sauvegarder dans un fichier JSON
            return self._save_contact_local(contact_data)
        else:
            # Mode Firestore
            return self._save_contact_firestore(contact_data)
    
    def _save_contact_local(self, contact_data):
        """Sauvegarde un message de contact localement"""
        try:
            script_dir = os.path.dirname(__file__)
            contacts_path = os.path.join(script_dir, '..', 'data', 'contacts.json')
            
            # Charger les contacts existants
            contacts = []
            if os.path.exists(contacts_path):
                with open(contacts_path, 'r', encoding='utf-8') as f:
                    contacts = json.load(f)
            
            # Générer un ID simple
            contact_id = f"contact_{len(contacts) + 1}"
            contact_data['id'] = contact_id
            
            # Ajouter le nouveau contact
            contacts.append(contact_data)
            
            # Sauvegarder
            os.makedirs(os.path.dirname(contacts_path), exist_ok=True)
            with open(contacts_path, 'w', encoding='utf-8') as f:
                json.dump(contacts, f, ensure_ascii=False, indent=2)
            
            print(f"INFO: Message de contact sauvegardé localement avec ID: {contact_id}")
            return contact_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde locale du contact: {e}")
            raise e
    
    def _save_contact_firestore(self, contact_data):
        """Sauvegarde un message de contact dans Firestore"""
        try:
            # Ajouter le document à la collection 'contacts'
            doc_ref = self.db.collection('contacts').add(contact_data)
            contact_id = doc_ref[1].id
            print(f"INFO: Message de contact sauvegardé dans Firestore avec ID: {contact_id}")
            return contact_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde Firestore du contact: {e}")
            raise e


# Instance globale du service Firestore
firestore_service = FirestoreService()

# Fonctions helper pour l'import dans les routes
def get_translation(text, target_language):
    return firestore_service.get_translation(text, target_language)

def save_translation(text, target_language, translation):
    return firestore_service.save_translation(text, target_language, translation)

def get_supported_languages():
    return firestore_service.get_supported_languages()

def update_translation_manual(french_text, target_language, new_translation):
    return firestore_service.update_translation_manual(french_text, target_language, new_translation)

def save_contact_message(contact_data):
    return firestore_service.save_contact_message(contact_data)



