from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message='Hello, World!')


@api_bp.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify(message=f'Hello, {name}!')