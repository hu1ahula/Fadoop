from app import create_app
from app.utils import register_datanode
import logging

app = create_app()

if __name__ == '__main__':
    # 注册 DataNode
    if not register_datanode():
        logging.error("Failed to register datanode")
        exit(1)
    logging.info("Registered datanode successfully")
    app.run(debug=True, port=8000)
