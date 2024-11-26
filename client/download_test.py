import os
import requests

# 服务器地址和端点
BASE_URL = 'http://localhost:8000/api/download'
CHUNK_URL = f'{BASE_URL}/{{file_id}}/{{chunk_index}}'

# 配置文件和分块参数
FILE_ID = 'song_chunk'  # 文件标识符
OUTPUT_FILENAME = 'downloaded_file.mp3'  # 下载后的文件名
CHUNK_SIZE = 1 * 1024 * 1024  # 每个块的大小，4MB（与上传时一致）

def download_chunk(file_id, chunk_index):
    """下载文件的单个块"""
    url = CHUNK_URL.format(file_id=file_id, chunk_index=chunk_index)
    response = requests.get(url, stream=True)
    print(url)
    
    if response.status_code == 200:
        print(f"Chunk {chunk_index} downloaded successfully.")
        return response.content
    else:
        print(f"Failed to download chunk {chunk_index}: {response.json()}")
        return None

def merge_chunks(output_filename, total_chunks):
    """合并所有下载的块"""
    with open(output_filename, 'wb') as output_file:
        for chunk_index in range(total_chunks):
            chunk_data = download_chunk(FILE_ID, chunk_index)
            if chunk_data is None:
                print(f"Error: Failed to download chunk {chunk_index}. Aborting.")
                break
            output_file.write(chunk_data)
        print(f"File saved as: {output_filename}")

def get_total_chunks(file_id):
    """获取文件的总块数（此函数假设你有一个接口可以查询文件的总块数）"""
    # 假设有一个接口返回文件的总块数
    total_chunks = 4  # 你可以根据实际的服务端实现来调整
    return total_chunks

def main():
    """执行分块下载"""
    # 步骤 1: 获取文件总块数
    total_chunks = get_total_chunks(FILE_ID)

    # 步骤 2: 下载所有块并合并
    merge_chunks(OUTPUT_FILENAME, total_chunks)

if __name__ == '__main__':
    main()
