from flask import Flask
import os
import threading
from .utils import send_heartbeat, register_datanode
import logging

def create_app():    
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 创建存储路径
    if not os.path.exists(app.config['STORAGE_PATH']):
        os.makedirs(app.config['STORAGE_PATH'])

    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()

    from app.routes import upload_api_bp, test_api_bp, download_api_bp
    app.register_blueprint(upload_api_bp, url_prefix='/api/upload')
    app.register_blueprint(download_api_bp, url_prefix='/api/download')
    app.register_blueprint(test_api_bp, url_prefix='/api/test')

    return app