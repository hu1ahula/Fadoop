import os
from flask import Blueprint, request, jsonify, current_app
from .utils import get_chunk_path, merge_chunks

api_bp = Blueprint('api', __name__)

@api_bp.route('/upload/init', methods=['POST'])
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

@api_bp.route('/upload/chunk', methods=['POST'])
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

@api_bp.route('/upload/complete', methods=['POST'])
def complete_upload():
    """
    完成上传并合并文件。
    """
    data = request.get_json()
    file_id = data.get('file_id')
    total_chunks = data.get('total_chunks', type=int)
    output_filename = data.get('output_filename')

    if not file_id or total_chunks is None or not output_filename:
        return jsonify({"message": "Invalid parameters"}), 400

    storage_path = current_app.config['STORAGE_PATH']
    try:
        output_path = merge_chunks(storage_path, file_id, total_chunks, output_filename)
        return jsonify({"message": "File upload complete", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"message": "Failed to merge chunks", "error": str(e)}), 500
