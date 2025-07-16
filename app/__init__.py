from flask import  Flask
from app.extensions import db, bcrypt, cors
import os
from flask_session import Session
from config import Config
from flask_cors import CORS
from .routes.auth_routes import auth_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'  
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 
    app.config['SESSION_COOKIE_SECURE'] = False # Set to True in production with HTTPS
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    Session(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    


    return app
