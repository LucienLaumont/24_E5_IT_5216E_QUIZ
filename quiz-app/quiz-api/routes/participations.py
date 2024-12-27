from flask import Blueprint, jsonify, request, Response
import sqlite3
from security.jwt_utils import token_required

DATABASE_NAME = "database.db"

participation_bp = Blueprint('participation', __name__)

@participation_bp.route('/participations/all', methods=['DELETE'])
@token_required
def delete_all_participations():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('DELETE FROM Participation')

        conn.commit()
        conn.close()

        return Response('All participations deleted successfully.', status=204)

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@participation_bp.route('/participations', methods=['POST'])
def post_participation():
    try:
        payload = request.get_json()
        player_name = payload.get("playerName")
        quiz_id = payload.get("quiz_id")
        answers = payload.get("answers")

        if not player_name or not quiz_id or not answers:
            return jsonify({"error": "Fields 'playerName', 'quiz_id', and 'answers' are required."}), 400

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Quiz WHERE id = ?', (quiz_id,))
        if not cursor.fetchone():
            return jsonify({"error": f"Quiz with id {quiz_id} does not exist."}), 404

        cursor.execute('''
            SELECT q.position, a.id
            FROM Question q
            LEFT JOIN Answer a ON q.id = a.question_id
            WHERE q.quiz_id = ? AND a.isCorrect = 1
            ORDER BY q.position;
        ''', (quiz_id,))
        correct_answers = {row[0]: row[1] for row in cursor.fetchall()}

        if len(answers) != len(correct_answers):
            return jsonify({"error": "Number of answers does not match the number of questions."}), 400

        cursor.execute('''
            INSERT INTO Participation (quiz_id, playerName, score)
            VALUES (?, ?, ?)
        ''', (quiz_id, player_name, 0))
        participation_id = cursor.lastrowid

        score = 0
        for position, user_answer_id in enumerate(answers, start=1):
            correct_answer_id = correct_answers.get(position)
            if correct_answer_id == user_answer_id:
                score += 1

            cursor.execute('''
                INSERT INTO ParticipationAnswer (participation_id, question_id, answer_id)
                SELECT ?, q.id, ?
                FROM Question q
                WHERE q.quiz_id = ? AND q.position = ?
            ''', (participation_id, user_answer_id, quiz_id, position))

        cursor.execute('UPDATE Participation SET score = ? WHERE id = ?', (score, participation_id))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Participation recorded successfully.",
            "playerName": player_name,
            "score": score,
            "participationId": participation_id
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@participation_bp.route('/participations/<int:participation_id>', methods=['GET'])
def get_participation(participation_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT p.playerName, p.score, q.title AS quizTitle
            FROM Participation p
            LEFT JOIN Quiz q ON p.quiz_id = q.id
            WHERE p.id = ?
        ''', (participation_id,))
        participation = cursor.fetchone()

        if not participation:
            return jsonify({"error": "Participation not found."}), 404

        conn.close()
        return jsonify({
            "playerName": participation[0],
            "score": participation[1],
            "quizTitle": participation[2]
        }), 200

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@participation_bp.route('/participations/rankings', methods=['GET'])
def get_rankings():
    try:
        quiz_id = request.args.get('quiz_id', type=int)
        if not quiz_id:
            return jsonify({"error": "'quiz_id' parameter is required."}), 400

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT p.playerName, p.score
            FROM Participation p
            WHERE p.quiz_id = ?
            ORDER BY p.score DESC
        ''', (quiz_id,))
        rankings = [{"name": row[0], "score": row[1]} for row in cursor.fetchall()]

        conn.close()
        return jsonify(rankings), 200

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@participation_bp.route('/participations/top-scores', methods=['GET'])
def get_top_scores():
    try:
        quiz_id = request.args.get('quiz_id', type=int)
        if not quiz_id:
            return jsonify({"error": "'quiz_id' parameter is required."}), 400

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT p.playerName, p.score
            FROM Participation p
            WHERE p.quiz_id = ?
            ORDER BY p.score DESC
            LIMIT 5
        ''', (quiz_id,))
        top_scores = [{"name": row[0], "score": row[1]} for row in cursor.fetchall()]

        conn.close()
        return jsonify(top_scores), 200

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
