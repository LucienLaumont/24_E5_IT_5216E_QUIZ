from flask import Blueprint, jsonify, request, Response
from database.init_db import init_db
from security.jwt_utils import token_required
from database import manage_position
import sqlite3

DATABASE_NAME = "database.db"

question_bp = Blueprint('question', __name__)

@question_bp.route('/rebuild-db', methods=['POST'])
@token_required
def rebuild_db():
    try:
        init_db()
        return Response('Ok', status=200)
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions/all', methods=['DELETE'])
@token_required
def delete_all_questions():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('DELETE FROM Question')

        conn.commit()
        conn.close()
        return Response('All questions deleted successfully.', status=204)

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, quiz_id, position, title, text, image
            FROM Question
            WHERE id = ?
        ''', (questionId,))
        question_row = cursor.fetchone()

        if not question_row:
            return jsonify({"error": "Question not found."}), 404

        question = {
            "id": question_row[0],
            "quiz_id": question_row[1],
            "position": question_row[2],
            "title": question_row[3],
            "text": question_row[4],
            "image": question_row[5]
        }

        cursor.execute('''
            SELECT text, isCorrect
            FROM Answer
            WHERE question_id = ?
        ''', (questionId,))
        answers = cursor.fetchall()

        question["possibleAnswers"] = [
            {"text": answer[0], "isCorrect": bool(answer[1])} for answer in answers
        ]

        conn.close()
        return jsonify(question), 200

    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions', methods=['GET'])
def get_question_by_position():
    try:
        position = request.args.get('position', type=int)
        quiz_id = request.args.get('quiz_id', type=int)

        if position is None or quiz_id is None:
            return jsonify({"error": "Both 'position' and 'quiz_id' parameters are required."}), 400

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, quiz_id, position, title, text, image
            FROM Question
            WHERE position = ? AND quiz_id = ?
        ''', (position, quiz_id))
        question_row = cursor.fetchone()

        if not question_row:
            return jsonify({"error": "Question not found for the given position and quiz."}), 404

        question = {
            "id": question_row[0],
            "quiz_id": question_row[1],
            "position": question_row[2],
            "title": question_row[3],
            "text": question_row[4],
            "image": question_row[5]
        }

        cursor.execute('''
            SELECT text, isCorrect
            FROM Answer
            WHERE question_id = ?
        ''', (question["id"],))
        answers = cursor.fetchall()

        question["possibleAnswers"] = [
            {"text": answer[0], "isCorrect": bool(answer[1])} for answer in answers
        ]

        conn.close()
        return jsonify(question), 200

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions', methods=['POST'])
@token_required
def create_question():
    try:
        payload = request.get_json()
        required_fields = ['quiz_id', 'position', 'title', 'text', 'image', 'possibleAnswers']

        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"The field '{field}' is required."}), 400

        quiz_id = payload['quiz_id']
        position = payload['position']
        title = payload['title']
        text = payload['text']
        image = payload['image']
        possible_answers = payload['possibleAnswers']

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Quiz WHERE id = ?', (quiz_id,))
        if not cursor.fetchone():
            return jsonify({"error": f"Quiz with id {quiz_id} does not exist."}), 404

        cursor.execute('''
            INSERT INTO Question (quiz_id, position, title, text, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (quiz_id, position, title, text, image))
        question_id = cursor.lastrowid

        for answer in possible_answers:
            if 'text' not in answer or 'isCorrect' not in answer:
                return jsonify({"error": "Each answer must have 'text' and 'isCorrect' fields."}), 400

            cursor.execute('''
                INSERT INTO Answer (question_id, text, isCorrect)
                VALUES (?, ?, ?)
            ''', (question_id, answer['text'], answer['isCorrect']))

        conn.commit()
        conn.close()

        return jsonify({
            "id": question_id,
            "message": "Question and answers created successfully."
        }), 201

    except sqlite3.IntegrityError as e:
        return jsonify({"error": "Database integrity error.", "details": str(e)}), 500
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['PUT'])
@token_required
def update_question(questionId):
    try:
        payload = request.get_json()
        required_fields = ['position', 'title', 'text', 'image', 'possibleAnswers']

        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"The field '{field}' is required."}), 400

        new_position = payload['position']
        new_title = payload['title']
        new_text = payload['text']
        new_image = payload['image']
        possible_answers = payload['possibleAnswers']

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Question WHERE id = ?', (questionId,))
        if not cursor.fetchone():
            return jsonify({"error": "Question not found."}), 404

        cursor.execute('''
            UPDATE Question
            SET position = ?, title = ?, text = ?, image = ?
            WHERE id = ?
        ''', (new_position, new_title, new_text, new_image, questionId))

        cursor.execute('DELETE FROM Answer WHERE question_id = ?', (questionId,))
        for answer in possible_answers:
            cursor.execute('''
                INSERT INTO Answer (question_id, text, isCorrect)
                VALUES (?, ?, ?)
            ''', (questionId, answer['text'], answer['isCorrect']))

        conn.commit()
        conn.close()

        return jsonify({"message": "Question and answers updated successfully."}), 204

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['DELETE'])
@token_required
def delete_question(questionId):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('DELETE FROM Question WHERE id = ?', (questionId,))

        conn.commit()
        conn.close()

        return Response('Question deleted successfully.', status=204)

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
