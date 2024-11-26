import random
import time
import hashlib

def distribute_datanode_id():
    current_time = str(time.time())
    hash_object = hashlib.sha256(current_time.encode())
    return hash_object.hexdigest()
