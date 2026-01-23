"""
Architecture du modèle Seq2Seq avec mécanisme d'attention pour la traduction
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

from ml.config import (
    EMBEDDING_DIM, ENCODER_UNITS, DECODER_UNITS, DROPOUT_RATE,
    PAD_ID, START_ID, END_ID, MAX_SEQUENCE_LENGTH
)


class Encoder(keras.Model):
    """Encodeur bidirectionnel LSTM"""
    
    def __init__(self, vocab_size, embedding_dim=EMBEDDING_DIM, enc_units=ENCODER_UNITS, **kwargs):
        super(Encoder, self).__init__(**kwargs)
        
        self.enc_units = enc_units
        self.vocab_size = vocab_size
        
        # Couche d'embedding
        self.embedding = layers.Embedding(
            vocab_size, 
            embedding_dim,
            mask_zero=True,  # Masquer le padding
            name='encoder_embedding'
        )
        
        # LSTM bidirectionnel
        self.lstm = layers.Bidirectional(
            layers.LSTM(
                enc_units,
                return_sequences=True,
                return_state=True,
                dropout=DROPOUT_RATE,
                recurrent_dropout=DROPOUT_RATE,
                name='encoder_lstm'
            ),
            name='bidirectional_encoder'
        )
        
        self.dropout = layers.Dropout(DROPOUT_RATE)
    
    def call(self, x, training=False):
        """
        Forward pass de l'encodeur
        
        Args:
            x: Séquence d'entrée [batch_size, seq_len]
            training: Mode entraînement
        """
        # Embedding
        x = self.embedding(x)
        x = self.dropout(x, training=training)
        
        # LSTM bidirectionnel
        # states: [forward_h, forward_c, backward_h, backward_c]
        output = self.lstm(x, training=training)
        encoder_output = output[0]
        states = output[1:]
        
        forward_h, forward_c, backward_h, backward_c = states
        
        # Combiner les états forward et backward avec tf.concat (plus sûr en call)
        state_h = tf.concat([forward_h, backward_h], axis=-1)
        state_c = tf.concat([forward_c, backward_c], axis=-1)
        
        return encoder_output, state_h, state_c
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'vocab_size': self.vocab_size,
            'enc_units': self.enc_units
        })
        return config


class BahdanauAttention(layers.Layer):
    """Mécanisme d'attention de Bahdanau"""
    
    def __init__(self, units, **kwargs):
        super(BahdanauAttention, self).__init__(**kwargs)
        self.units = units
        
        # Couches de transformation
        self.W1 = layers.Dense(units, name='attention_W1')
        self.W2 = layers.Dense(units, name='attention_W2')
        self.V = layers.Dense(1, name='attention_V')
    
    def call(self, query, values):
        """
        Calcule les poids d'attention et le vecteur de contexte
        
        Args:
            query: État caché du décodeur [batch_size, hidden_dim]
            values: Sorties de l'encodeur [batch_size, seq_len, hidden_dim]
        
        Returns:
            context_vector: Vecteur de contexte [batch_size, hidden_dim]
            attention_weights: Poids d'attention [batch_size, seq_len, 1]
        """
        # query shape: [batch_size, hidden_dim]
        # values shape: [batch_size, seq_len, hidden_dim]
        
        # Ajouter une dimension temporelle à query
        query_with_time_axis = tf.expand_dims(query, 1)
        
        # Calculer le score d'attention
        score = self.V(tf.nn.tanh(
            self.W1(query_with_time_axis) + self.W2(values)
        ))
        
        # attention_weights shape: [batch_size, seq_len, 1]
        attention_weights = tf.nn.softmax(score, axis=1)
        
        # Vecteur de contexte
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)
        
        return context_vector, attention_weights
    
    def get_config(self):
        config = super().get_config()
        config.update({'units': self.units})
        return config


class Decoder(keras.Model):
    """Décodeur LSTM avec attention"""
    
    def __init__(self, vocab_size, embedding_dim=EMBEDDING_DIM, dec_units=DECODER_UNITS, **kwargs):
        super(Decoder, self).__init__(**kwargs)
        
        self.dec_units = dec_units
        self.vocab_size = vocab_size
        
        # Couche d'embedding
        self.embedding = layers.Embedding(
            vocab_size,
            embedding_dim,
            mask_zero=True,
            name='decoder_embedding'
        )
        
        # LSTM
        self.lstm = layers.LSTM(
            dec_units,
            return_sequences=True,
            return_state=True,
            dropout=DROPOUT_RATE,
            recurrent_dropout=DROPOUT_RATE,
            name='decoder_lstm'
        )
        
        # Attention
        self.attention = BahdanauAttention(dec_units)
        
        # Couche de sortie
        self.fc = layers.Dense(vocab_size, name='output_dense')
        
        self.dropout = layers.Dropout(DROPOUT_RATE)
    
    def call(self, x, hidden, cell, encoder_output, training=False):
        """
        Forward pass du décodeur
        
        Args:
            x: Token d'entrée [batch_size, 1]
            hidden: État caché précédent [batch_size, dec_units]
            cell: État cellule précédent [batch_size, dec_units]
            encoder_output: Sorties de l'encodeur [batch_size, seq_len, enc_units]
            training: Mode entraînement
        
        Returns:
            output: Prédictions [batch_size, 1, vocab_size]
            state_h: Nouvel état caché
            state_c: Nouvel état cellule
            attention_weights: Poids d'attention
        """
        # Calculer l'attention
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        
        # x shape: [batch_size, 1]
        x = self.embedding(x)
        
        # Concaténer
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        
        # LSTM
        output, state_h, state_c = self.lstm(x, initial_state=[hidden, cell], training=training)
        
        # Squeeze the time dimension: [batch, 1, units] -> [batch, units]
        output = tf.squeeze(output, axis=1)
        
        # Couche de sortie
        prediction = self.fc(output)
        
        return prediction, state_h, state_c, attention_weights
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'vocab_size': self.vocab_size,
            'dec_units': self.dec_units
        })
        return config


class Seq2SeqModel(keras.Model):
    """Modèle Seq2Seq complet avec attention"""
    
    def __init__(self, source_vocab_size, target_vocab_size, **kwargs):
        super(Seq2SeqModel, self).__init__(**kwargs)
        
        self.source_vocab_size = source_vocab_size
        self.target_vocab_size = target_vocab_size
        
        # Créer l'encodeur et le décodeur
        self.encoder = Encoder(source_vocab_size)
        self.decoder = Decoder(target_vocab_size)
        
        # Couches de projection
        self.project_h = layers.Dense(DECODER_UNITS, name='project_h')
        self.project_c = layers.Dense(DECODER_UNITS, name='project_c')
    
    def call(self, inputs, training=False):
        """
        Forward pass du modèle complet
        
        Args:
            inputs: Tuple de (source_seq, target_seq)
            training: Mode entraînement
        
        Returns:
            predictions: Prédictions [batch_size, target_seq_len, vocab_size]
        """
        source_seq, target_seq = inputs
        
        # Encoder
        encoder_output, state_h, state_c = self.encoder(source_seq, training=training)
        
        # Projection initiale pour le décodeur
        state_h = self.project_h(state_h)
        state_c = self.project_c(state_c)
        
        # Teacher forcing: exclure le dernier token
        dec_input_seq = target_seq[:, :-1]
        target_len = tf.shape(dec_input_seq)[1]
        
        # TensorArray pour accumuler les sorties
        all_outputs = tf.TensorArray(tf.float32, size=target_len)
        
        # Boucle temporelle
        for t in tf.range(target_len):
            # Token à t
            # shape: [batch, 1]
            token_input = dec_input_seq[:, t:t+1]
            
            # Un pas de décodage
            predictions, state_h, state_c, _ = self.decoder(
                token_input, state_h, state_c, encoder_output, training=training
            )
            
            # Stocker
            all_outputs = all_outputs.write(t, predictions)
        
        # [seq_len, batch, vocab] -> [batch, seq_len, vocab]
        all_outputs = all_outputs.stack()
        all_outputs = tf.transpose(all_outputs, [1, 0, 2])
        
        return all_outputs
    
    def translate(self, source_text_ids, source_vocab, target_vocab, max_length=MAX_SEQUENCE_LENGTH):
        """
        Traduit une séquence source en séquence cible
        
        Args:
            source_text_ids: IDs de la séquence source [seq_len]
            source_vocab: Vocabulaire source
            target_vocab: Vocabulaire cible
            max_length: Longueur maximale de la traduction
        
        Returns:
            translation: Texte traduit
            attention_weights: Poids d'attention pour visualisation
        """
        # Ajouter une dimension batch
        source_seq = tf.expand_dims(source_text_ids, 0)
        
        # Encoder
        encoder_output, state_h, state_c = self.encoder(source_seq, training=False)
        
        # Projeter l'état de l'encodeur vers la dimension du décodeur
        state_h = self.project_h(state_h)
        state_c = self.project_c(state_c)
        
        # Initialiser avec le token START
        decoder_input = tf.expand_dims([START_ID], 0)
        
        result = []
        attention_plot = []
        
        for _ in range(max_length):
            # Décoder un pas
            predictions, state_h, state_c, attention_weights = self.decoder(
                decoder_input, state_h, state_c, encoder_output, training=False
            )
            
            # Stocker les poids d'attention
            attention_plot.append(attention_weights.numpy())
            
            # Prendre le token le plus probable
            predicted_id = tf.argmax(predictions, axis=-1).numpy()[0]
            
            # Arrêter si on génère le token END
            if predicted_id == END_ID:
                break
            
            result.append(predicted_id)
            
            # Utiliser la prédiction comme prochaine entrée
            decoder_input = tf.expand_dims([predicted_id], 0)
        
        # Décoder les IDs en texte
        translation = target_vocab.decode(result, skip_special_tokens=True)
        
        return translation, np.array(attention_plot)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'source_vocab_size': self.source_vocab_size,
            'target_vocab_size': self.target_vocab_size
        })
        return config


def create_model(source_vocab_size, target_vocab_size):
    """
    Fonction utilitaire pour créer un modèle Seq2Seq
    
    Args:
        source_vocab_size: Taille du vocabulaire source
        target_vocab_size: Taille du vocabulaire cible
    
    Returns:
        Modèle Seq2Seq compilé
    """
    model = Seq2SeqModel(source_vocab_size, target_vocab_size)
    
    print(f"✅ Modèle créé:")
    print(f"   - Vocab source: {source_vocab_size}")
    print(f"   - Vocab cible: {target_vocab_size}")
    print(f"   - Embedding dim: {EMBEDDING_DIM}")
    print(f"   - Encoder units: {ENCODER_UNITS}")
    print(f"   - Decoder units: {DECODER_UNITS}")
    
    return model


if __name__ == "__main__":
    # Test de création du modèle
    print("🧪 Test de l'architecture du modèle\n")
    
    # Créer un modèle de test
    model = create_model(source_vocab_size=1000, target_vocab_size=800)
    
    # Créer des données de test
    batch_size = 4
    seq_len = 10
    
    source_seq = tf.random.uniform((batch_size, seq_len), maxval=1000, dtype=tf.int32)
    target_seq = tf.random.uniform((batch_size, seq_len), maxval=800, dtype=tf.int32)
    
    # Forward pass
    print("\n🔄 Test du forward pass...")
    predictions = model((source_seq, target_seq), training=True)
    
    print(f"✅ Prédictions shape: {predictions.shape}")
    print(f"   Expected: ({batch_size}, {seq_len-1}, 800)")
    
    print("\n✅ Architecture validée!")
