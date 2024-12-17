from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@health_bp.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    return {"size": 0, "scores": []}, 200