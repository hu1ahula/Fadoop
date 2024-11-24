import os
from werkzeug.utils import secure_filename

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
