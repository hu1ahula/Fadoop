from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import api_bp, heartbeat_bp, register_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(heartbeat_bp, url_prefix='/api/heartbeat')
    app.register_blueprint(register_bp, url_prefix='/api/register')

    return app