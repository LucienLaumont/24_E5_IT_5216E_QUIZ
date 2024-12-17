from flask import Blueprint, jsonify, request
from database.init_db import init_db

question_bp = Blueprint('question', __name__)

@question_bp.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    try:
        init_db()
        return jsonify({"Answer": "Database initialized"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions', methods = ['POST'])
def questions():
    return

