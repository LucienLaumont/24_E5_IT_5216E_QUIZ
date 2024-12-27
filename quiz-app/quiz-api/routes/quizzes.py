from flask import Blueprint, jsonify, request, Response
import sqlite3

DATABASE_NAME = "database.db"

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quizzes', methods=['GET'])
def get_all_quizzes():
    """
    Récupère la liste de tous les quiz.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, description, created_at
            FROM Quiz
        ''')
        quizzes = [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "created_at": row[3]
            } for row in cursor.fetchall()
        ]

        conn.close()
        return jsonify(quizzes), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """
    Récupère les détails d'un quiz spécifique, y compris ses questions.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupérer les informations du quiz
        cursor.execute('''
            SELECT id, title, description, created_at
            FROM Quiz
            WHERE id = ?
        ''', (quiz_id,))
        quiz_row = cursor.fetchone()

        if not quiz_row:
            return jsonify({"error": "Quiz non trouvé."}), 404

        quiz = {
            "id": quiz_row[0],
            "title": quiz_row[1],
            "description": quiz_row[2],
            "created_at": quiz_row[3],
            "questions": []
        }

        # Récupérer les questions associées au quiz
        cursor.execute('''
            SELECT id, position, title, text, image
            FROM Question
            WHERE quiz_id = ?
            ORDER BY position
        ''', (quiz_id,))
        questions = [
            {
                "id": row[0],
                "position": row[1],
                "title": row[2],
                "text": row[3],
                "image": row[4]
            } for row in cursor.fetchall()
        ]

        quiz["questions"] = questions

        conn.close()
        return jsonify(quiz), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@quiz_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    """
    Crée un nouveau quiz.
    """
    try:
        payload = request.get_json()
        title = payload.get("title")
        description = payload.get("description")

        if not title:
            return jsonify({"error": "Le champ 'title' est requis."}), 400

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Insérer le quiz
        cursor.execute('''
            INSERT INTO Quiz (title, description)
            VALUES (?, ?)
        ''', (title, description))
        quiz_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return jsonify({"message": "Quiz créé avec succès.", "quizId": quiz_id}), 201

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """
    Supprime un quiz spécifique et toutes ses questions associées.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')

        # Supprimer le quiz
        cursor.execute('''
            DELETE FROM Quiz
            WHERE id = ?
        ''', (quiz_id,))

        conn.commit()
        conn.close()

        return Response(status=204)

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
