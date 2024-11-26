import os

class Config:
    STORAGE_PATH = os.path.join(os.getcwd(), 'app', 'storage')  # 存储路径
    CONFIG_DIRECTORY = os.path.join(os.getcwd(), 'config')
    CHUNK_SIZE = 1 * 1024 * 1024 # 1MB
    NAME_NODE = 'localhost'
    NAME_NODE_PORT = 8001
    HEARTBEAT_INTERVAL = 5
