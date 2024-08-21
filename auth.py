from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = 'your_secret_key'  # Use um segredo seguro em produção

# Armazenamento em memória
users = []

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Preencha todos os campos!'}), 400

    if any(user['username'] == username for user in users):
        return jsonify({'message': 'Usuário já registrado!'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.append({'username': username, 'password': hashed})
    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = next((u for u in users if u['username'] == username), None)
    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Nome de usuário ou senha incorretos!'}), 401

    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})