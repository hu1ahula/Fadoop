import os

class Config:
    CHUNK_SIZE = 1 * 1024 * 1024 # 1MB
    NAME_NODE = 'localhost'
    NAME_NODE_PORT = 8000
    HEARTBEAT_INTERVAL = 5
