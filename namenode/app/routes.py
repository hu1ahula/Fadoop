from flask import Blueprint, request, jsonify, current_app
from .utils import *

api_bp = Blueprint('api', __name__)
heartbeat_bp = Blueprint('heartbeat', __name__)
register_bp = Blueprint('register', __name__)

@api_bp.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message='Hello, World!')


@api_bp.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify(message=f'Hello, {name}!')

@heartbeat_bp.route('/')
def heartbeat():
    return jsonify({"message": "Good."})

@register_bp.route('/', methods=['POST'])
def register():
    data = request.get_json()
    
    if data["datanode_id"] == "None":
        data["datanode_id"] = distribute_datanode_id()

    return jsonify(data)
