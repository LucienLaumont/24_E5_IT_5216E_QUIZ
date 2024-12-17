from flask import Blueprint, jsonify, request, Response
from database.init_db import init_db
from database import manage_position
import sqlite3

DATABASE_NAME = "database.db"

question_bp = Blueprint('question', __name__)

@question_bp.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    try:
        init_db()
        return Response('Ok', status=200)  # Return plain text response
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500


@question_bp.route('/questions', methods=['POST'])
def questions():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupération du payload JSON
        payload = request.get_json()

        # Validation des champs requis pour la question
        required_fields = ['position', 'title', 'text', 'image', 'possibleAnswers']
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"Le champ '{field}' est requis."}), 400

        # Extraction des valeurs pour la question
        position = payload['position']
        title = payload['title']
        text = payload['text']
        image = payload['image']
        possible_answers = payload['possibleAnswers']
        
        
        # Gestion des conflits de position
        manage_position.increment_positions(cursor, position)

        # Insertion de la question dans la base de données
        cursor.execute('''
            INSERT INTO Question (position, title, text, image)
            VALUES (?, ?, ?, ?)
        ''', (position, title, text, image))
        question_id = cursor.lastrowid  # Récupération de l'ID de la question insérée

        # Validation et insertion des réponses possibles
        if not isinstance(possible_answers, list) or len(possible_answers) == 0:
            return jsonify({"error": "Le champ 'possibleAnswers' doit être une liste non vide."}), 400

        for answer in possible_answers:
            if 'text' not in answer or 'isCorrect' not in answer:
                return jsonify({"error": "Chaque réponse doit contenir les champs 'text' et 'isCorrect'."}), 400
            
            cursor.execute('''
                INSERT INTO Answer (question_id, text, isCorrect)
                VALUES (?, ?, ?)
            ''', (question_id, answer['text'], answer['isCorrect']))

        # Sauvegarde et fermeture
        conn.commit()
        conn.close()

        return jsonify({"message": "Question et réponses insérées avec succès."}), 200

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
