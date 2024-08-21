from flask import Flask
from auth import auth_bp
from messages import messages_bp

app = Flask(__name__)

# Registra os blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(messages_bp, url_prefix='/api/messages')

if __name__ == '__main__':
    app.run(port=5000)