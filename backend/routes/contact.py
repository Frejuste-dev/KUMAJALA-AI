from flask import Blueprint, request, jsonify
from services.firestore import save_contact_message
from datetime import datetime

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    """
    Endpoint pour recevoir les messages du formulaire de contact.
    
    Payload attendu:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Investissement",
        "message": "Je suis intéressé par..."
    }
    """
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Le champ "{field}" est requis'
                }), 400
        
        # Validation basique de l'email
        email = data.get('email')
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'error': 'Format d\'email invalide'
            }), 400
        
        # Préparation des données pour Firestore
        contact_data = {
            'name': data.get('name'),
            'email': email,
            'subject': data.get('subject'),
            'message': data.get('message'),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'new'  # Pour un futur système de gestion
        }
        
        # Sauvegarde dans Firestore
        message_id = save_contact_message(contact_data)
        
        return jsonify({
            'success': True,
            'message': 'Votre message a été envoyé avec succès',
            'id': message_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur lors de l\'envoi du message',
            'details': str(e)
        }), 500
