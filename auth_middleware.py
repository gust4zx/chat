from flask import request, jsonify
import jwt

SECRET_KEY = 'your_secret_key'  # Use o mesmo segredo definido em auth.py

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if token is None:
            return jsonify({'message': 'Token é necessário!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 403

        return f(current_user, *args, **kwargs)
    
    return decorator