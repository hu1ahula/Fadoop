import os
import requests

# 服务器地址和端点
BASE_URL = 'http://localhost:8000/api/upload'
INIT_URL = f'{BASE_URL}/init'
CHUNK_URL = f'{BASE_URL}/chunk'
COMPLETE_URL = f'{BASE_URL}/complete'

# 配置文件和分块参数
FILE_PATH = './song.mp3'  # 待上传的文件路径
FILE_ID = 'unique_file_id'  # 唯一文件标识符
CHUNK_SIZE = 1 * 1024 * 1024  # 每个块的大小，4MB
OUTPUT_FILENAME = 'song_chunk.mp3'  # 合并后的文件名

def init_upload(file_id):
    """初始化上传"""
    response = requests.post(INIT_URL, json={'file_id': file_id})
    if response.status_code == 200:
        print("Upload initialized successfully.")
    else:
        print(f"Failed to initialize upload: {response.json()}")

def upload_chunk(file_id, chunk_index, chunk_data):
    """上传文件块"""
    files = {
        'file': ('chunk', chunk_data)
    }
    data = {
        'file_id': file_id,
        'chunk_index': chunk_index
    }
    response = requests.post(CHUNK_URL, data=data, files=files)
    if response.status_code == 200:
        print(f"Chunk {chunk_index} uploaded successfully.")
    else:
        print(f"Failed to upload chunk {chunk_index}: {response.json()}")

def complete_upload(file_id, total_chunks, output_filename):
    """完成上传并合并文件"""
    response = requests.post(COMPLETE_URL, json={
        'file_id': file_id,
        'total_chunks': total_chunks,
        'output_filename': output_filename
    })
    if response.status_code == 200:
        print("File upload complete.")
        print(f"File saved as: {response.json()['output_path']}")
    else:
        print(f"Failed to complete upload: {response.json()}")

def chunk_file(file_path, chunk_size):
    """将文件分块"""
    with open(file_path, 'rb') as f:
        chunk_index = 0
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_index, chunk_data
            chunk_index += 1

def main():
    """执行分块上传"""
    # 步骤 1: 初始化上传
    init_upload(FILE_ID)
    
    # 步骤 2: 上传文件块
    total_chunks = 0
    for chunk_index, chunk_data in chunk_file(FILE_PATH, CHUNK_SIZE):
        upload_chunk(FILE_ID, chunk_index, chunk_data)
        total_chunks += 1
    
    print(f"Total chunks: {total_chunks}")
    # 步骤 3: 完成上传
    complete_upload(FILE_ID, total_chunks, OUTPUT_FILENAME)

if __name__ == '__main__':
    main()
