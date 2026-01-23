"""
Configuration centralisée pour le modèle de traduction TensorFlow
"""
import os

# ==================== CHEMINS ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CHECKPOINTS_DIR = os.path.join(BASE_DIR, "checkpoints")

# Créer les dossiers s'ils n'existent pas
for directory in [MODEL_DIR, LOGS_DIR, CHECKPOINTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ==================== LANGUES ====================
SOURCE_LANGUAGE = "fr"
SUPPORTED_LANGUAGES = ["bété", "baoulé", "mooré", "agni"]

# ==================== HYPERPARAMÈTRES ====================
# Architecture
EMBEDDING_DIM = 256
ENCODER_UNITS = 512
DECODER_UNITS = 512
DROPOUT_RATE = 0.3

# Entraînement
BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.15
TEST_SPLIT = 0.15

# Séquences
MAX_SEQUENCE_LENGTH = 50
MIN_SEQUENCE_LENGTH = 1

# ==================== TOKENS SPÉCIAUX ====================
PAD_TOKEN = "<PAD>"
START_TOKEN = "<START>"
END_TOKEN = "<END>"
UNK_TOKEN = "<UNK>"

SPECIAL_TOKENS = [PAD_TOKEN, START_TOKEN, END_TOKEN, UNK_TOKEN]

# Indices des tokens spéciaux
PAD_ID = 0
START_ID = 1
END_ID = 2
UNK_ID = 3

# ==================== SEUILS ====================
CONFIDENCE_THRESHOLD = 0.7  # Seuil pour utiliser TF vs fallback Gemini
MIN_VOCAB_FREQUENCY = 1  # Fréquence minimale pour inclure un mot dans le vocab

# ==================== AUGMENTATION DE DONNÉES ====================
AUGMENTATION_FACTOR = 5  # Multiplier le dataset par ce facteur
NOISE_PROBABILITY = 0.1  # Probabilité d'ajouter du bruit

# ==================== CALLBACKS ====================
EARLY_STOPPING_PATIENCE = 10
REDUCE_LR_PATIENCE = 5
REDUCE_LR_FACTOR = 0.5

# ==================== ÉVALUATION ====================
BLEU_MAX_ORDER = 4  # BLEU-4
BEAM_WIDTH = 3  # Pour le beam search lors de l'inférence

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"
TENSORBOARD_UPDATE_FREQ = "epoch"

# ==================== FICHIERS ====================
LANGUAGE_JSON_PATH = os.path.join(DATA_DIR, "language.json")
VOCAB_FILE_TEMPLATE = os.path.join(MODEL_DIR, "vocab_{language}.json")
MODEL_FILE_TEMPLATE = os.path.join(MODEL_DIR, "{language}_model")
TOKENIZER_FILE_TEMPLATE = os.path.join(MODEL_DIR, "tokenizer_{language}.pkl")

# ==================== DEVICE ====================
# TensorFlow détectera automatiquement GPU si disponible
USE_GPU = True
MIXED_PRECISION = False  # Activer pour entraînement plus rapide sur GPU moderne
