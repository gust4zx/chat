from flask import Blueprint, request, jsonify
from auth_middleware import token_required
import datetime

messages_bp = Blueprint('messages', __name__)

# Armazenamento em memória
messages = []

@messages_bp.route('/', methods=['POST'])
@token_required
def send_message(current_user):
    data = request.json
    user = data.get('user')
    text = data.get('text')

    if not user or not text:
        return jsonify({'message': 'Preencha todos os campos!'}), 400

    new_message = {'user': user, 'text': text, 'timestamp': datetime.datetime.utcnow()}
    messages.append(new_message)
    return jsonify(new_message), 201

@messages_bp.route('/', methods=['GET'])
@token_required
def get_messages(current_user):
    return jsonify(messages)