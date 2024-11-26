import os
from flask import Blueprint, request, jsonify, current_app
from .utils import *

test_api_bp = Blueprint('test', __name__)
upload_api_bp = Blueprint('upload', __name__)
download_api_bp = Blueprint('download', __name__)

@test_api_bp.route('/')
def test():
    return jsonify({"message": "Hello, World!"})

@upload_api_bp.route('/init', methods=['POST'])
def init_upload():
    """
    初始化文件上传。
    """
    data = request.get_json()
    file_id = data.get('file_id')  # 文件唯一 ID（如哈希）
    if not file_id:
        return jsonify({"message": "File ID is required"}), 400

    storage_path = current_app.config['STORAGE_PATH']
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return jsonify({"message": "Upload initialized", "file_id": file_id}), 200

@upload_api_bp.route('/chunk', methods=['POST'])
def upload_chunk():
    """
    上传单个文件块。
    """
    file_id = request.form.get('file_id')
    chunk_index = request.form.get('chunk_index', type=int)
    file = request.files.get('file')

    if not file_id or chunk_index is None or not file:
        return jsonify({"message": "Invalid parameters"}), 400

    storage_path = current_app.config['STORAGE_PATH']
    chunk_path = get_chunk_path(storage_path, file_id, chunk_index)
    file.save(chunk_path)

    return jsonify({"message": f"Chunk {chunk_index} uploaded successfully"}), 200

@upload_api_bp.route('/complete', methods=['POST'])
def complete_upload():
    """
    完成上传并合并文件。
    """
    data = request.get_json()
    file_id = data.get('file_id')
    total_chunks = int(data.get('total_chunks'))
    output_filename = data.get('output_filename')

    if not file_id or total_chunks is None or not output_filename:
        return jsonify({"message": "Invalid parameters"}), 400

    storage_path = current_app.config['STORAGE_PATH']
    try:
        output_path = merge_chunks(storage_path, file_id, total_chunks, output_filename)
        return jsonify({"message": "File upload complete", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"message": "Failed to merge chunks", "error": str(e)}), 500


@download_api_bp.route('/<file_id>/<chunk_index>', methods=['GET'])
def download_chunk(file_id, chunk_index):
    """
    按块下载合并后的文件
    """

    chunk_index = int(chunk_index)  # 确保块索引为整数
    chunk_size = current_app.config['CHUNK_SIZE']
    storage_path = current_app.config['STORAGE_PATH']
    file_path = get_file_path(storage_path, file_id)

    # 获取文件的总大小
    file_size = os.path.getsize(file_path)

    # 计算开始和结束的字节偏移量
    start_byte = chunk_index * chunk_size
    end_byte = min(start_byte + chunk_size, file_size)

    print(f"Downloading chunk {chunk_index} from {start_byte} to {end_byte}")

    # 检查请求的块是否超出了文件的范围
    if start_byte >= file_size:
        return jsonify({"message": "Chunk index out of range"}), 404

    # 读取文件的指定块并返回给客户端
    with open(file_path, 'rb') as f:
        f.seek(start_byte)
        chunk_data = f.read(end_byte - start_byte)

    # 将该块返回给客户端
    return chunk_data, 200, {'Content-Type': 'application/octet-stream'}
