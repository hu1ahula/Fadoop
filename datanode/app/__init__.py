from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 创建存储路径
    if not os.path.exists(app.config['STORAGE_PATH']):
        os.makedirs(app.config['STORAGE_PATH'])

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app