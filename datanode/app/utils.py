import os
import requests
import time
import config
import json

def get_chunk_path(storage_path, file_id, chunk_index):
    """
    返回块的存储路径。
    """
    return os.path.join(storage_path, f"{file_id}_chunk_{chunk_index}")

def merge_chunks(storage_path, file_id, total_chunks, output_filename):
    """
    合并所有块为完整文件。
    """
    output_path = os.path.join(storage_path, output_filename)
    with open(output_path, 'wb') as output_file:
        for i in range(total_chunks):
            chunk_path = get_chunk_path(storage_path, file_id, i)
            with open(chunk_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            os.remove(chunk_path)  # 合并后删除块文件
    return output_path

def get_file_path(storage_path, filename):
    """
    返回文件的存储路径。
    """
    file_path = os.path.join(storage_path, filename)
    return file_path

def get_storage_size(storage_path):
    """
    获取存储空间的总大小。
    """
    files = os.listdir(storage_path)
    block_numbers = len(files)
    total_size = sum(os.path.getsize(os.path.join(storage_path, file)) for file in files)
    return block_numbers, total_size

def register_datanode():
    print(__file__)
    """
    向 NameNode 注册 DataNode
    """
    namenode = config.Config.NAME_NODE
    port = config.Config.NAME_NODE_PORT
    config_directory = config.Config.CONFIG_DIRECTORY

    block_numbers, total_size = get_storage_size(config_directory)

    registration_data = {
        "datanode_id": "None",
        "port": port,
        "used": total_size,
        "blocks": block_numbers
    }

    if os.path.exists(f"{config_directory}/config/node_info.json"):
        print("Node info exists")
        with open(f"{config_directory}/config/node_info.json", "r") as f:
            node_info = json.load(f)
        registration_data["datanode_id"] = node_info["datanode_id"]

    # 向 NameNode 发送 HTTP 注册请求
    response = requests.post(f"http://{namenode}:{port}/api/register", json=registration_data)

    if response.status_code == 200:
        # 如果成功，获取 DataNode ID
        response_data = response.json()

        os.makedirs(f"{config_directory}/config", exist_ok=True)
        with open(f"{config_directory}/config/node_info.json", "w", ) as f:
            json.dump(response_data, f)
        print(response_data)
        return True
    else:
        print("DataNode 注册失败")
        return False


def report_storage_info():
    """向 NameNode 报告存储信息"""
    storage_dir = config.Config.STORAGE_PATH
    files = os.listdir(storage_dir)
    block_numbers = len(files)
    total_size = sum(os.path.getsize(storage_dir))


def send_heartbeat():
    """每隔 x 秒向 NameNode 发送心跳包"""
    namenode = config.Config.NAME_NODE
    port = config.Config.NAME_NODE_PORT
    heartbeat_interval = config.Config.HEARTBEAT_INTERVAL
    while True:
        try:
            namenode_url = f"http://{namenode}:{port}/api/heartbeat/"
            response = requests.get(namenode_url)
            if response.status_code == 200:
                print("Heartbeat sent successfully to NameNode.")
            else:
                print(f"Failed to send heartbeat: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending heartbeat: {e}")

        # 等待下次心跳
        time.sleep(heartbeat_interval)