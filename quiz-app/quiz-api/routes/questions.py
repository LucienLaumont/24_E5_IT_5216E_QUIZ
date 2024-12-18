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

@question_bp.route('/questions/all',methods=['DELETE'])
def delete_all_questions():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('''
            DELETE FROM Question
        ''')
        
        # Sauvegarde et fermeture
        conn.commit()
        conn.close()

        return Response('Delete Questions table', status=204)
    
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['DELETE'])
@token_required
def delete_question(questionId):
    """
    Supprime une question spécifique et décrémente les positions des questions ayant une position supérieure.
    :param questionId: Identifiant de la question à supprimer.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')

        # Récupération de la position de la question à supprimer
        cursor.execute('''
            SELECT position FROM Question
            WHERE id = ?
        ''', (questionId,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return jsonify({"error": "Question non trouvée."}), 404

        position = result[0]

        # Suppression de la question
        cursor.execute('''
            DELETE FROM Question
            WHERE id = ?
        ''', (questionId,))

        # Décrémenter les positions des questions supérieures
        manage_position.decrement_positions(cursor, position)

        # Sauvegarde et fermeture
        conn.commit()
        conn.close()

        return Response(status=204)

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    """
    Récupère les détails d'une question avec ses réponses possibles.
    :param questionId: Identifiant unique de la question.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupération de la question
        cursor.execute('''
            SELECT id, position, title, text, image
            FROM Question
            WHERE id = ?
        ''', (questionId,))
        question_row = cursor.fetchone()

        if not question_row:
            conn.close()
            return jsonify({"error": "Question non trouvée."}), 404

        # Structurer la réponse pour la question
        question = {
            "id": question_row[0],
            "position": question_row[1],
            "title": question_row[2],
            "text": question_row[3],
            "image": question_row[4]
        }

        # Récupération des réponses possibles associées à la question
        cursor.execute('''
            SELECT text, isCorrect
            FROM Answer
            WHERE question_id = ?
        ''', (questionId,))
        answers = cursor.fetchall()

        # Structurer la liste des réponses possibles
        possible_answers = []
        for answer in answers:
            possible_answers.append({
                "text": answer[0],
                "isCorrect": bool(answer[1])
            })

        # Fermer la connexion
        conn.close()

        # Ajouter les réponses possibles à la question
        question["possibleAnswers"] = possible_answers

        # Retourner la réponse
        return jsonify(question), 200

    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500

@question_bp.route('/questions', methods=['GET'])
def get_question_by_position():
    """
    Récupère une question spécifique en fonction de sa position et ses réponses possibles.
    :query param position: La position de la question à récupérer.
    """
    try:
        # Récupération de la position depuis les paramètres de requête
        position = request.args.get('position', type=int)
        if position is None:
            return jsonify({"error": "Le paramètre 'position' est requis et doit être un entier."}), 400

        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupération de la question avec la position spécifiée
        cursor.execute('''
            SELECT id, position, title, text, image
            FROM Question
            WHERE position = ?
        ''', (position,))
        question_row = cursor.fetchone()

        if not question_row:
            conn.close()
            return jsonify({"error": f"Aucune question trouvée pour la position {position}."}), 404

        # Structuration de l'objet question
        question = {
            "id": question_row[0],
            "position": question_row[1],
            "title": question_row[2],
            "text": question_row[3],
            "image": question_row[4]
        }

        # Récupération des réponses possibles associées à la question
        cursor.execute('''
            SELECT text, isCorrect
            FROM Answer
            WHERE question_id = ?
        ''', (question["id"],))
        answers = cursor.fetchall()

        # Structuration des réponses possibles
        question["possibleAnswers"] = [
            {"text": answer[0], "isCorrect": bool(answer[1])} for answer in answers
        ]

        # Fermeture de la connexion
        conn.close()

        # Retourner la question et ses réponses possibles
        return jsonify(question), 200

    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@question_bp.route('/questions', methods=['POST'])
@token_required
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

        return jsonify({
            "id": question_id,
            "message": "Question et réponses insérées avec succès."
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500

@question_bp.route('/questions/<int:questionId>', methods=['PUT'])
@token_required
def update_question(questionId):
    try:
        payload = request.get_json()
        new_position = payload.get('position')
        new_text = payload.get('text')
        new_title = payload.get('title')
        new_image = payload.get('image')
        possible_answers = payload.get('possibleAnswers')

        if new_position is None or new_text is None or new_title is None or possible_answers is None:
            return jsonify({"error": "Les champs 'position', 'text', 'title' et 'possibleAnswers' sont requis."}), 400

        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupérer l'ancienne position
        cursor.execute("SELECT position FROM Question WHERE id = ?", (questionId,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Question non trouvée."}), 404

        old_position = result[0]

        # Gérer l'incrémentation ou la décrémentation
        manage_position.decrement_positions(cursor, old_position)
        manage_position.increment_positions(cursor, new_position)

        # Mettre à jour la question
        cursor.execute('''
            UPDATE Question
            SET position = ?, text = ?, title = ?, image = ?
            WHERE id = ?
        ''', (new_position, new_text, new_title, new_image, questionId))

        # Supprimer les anciennes réponses
        cursor.execute("DELETE FROM Answer WHERE question_id = ?", (questionId,))

        # Ajouter les nouvelles réponses
        for answer in possible_answers:
            cursor.execute('''
                INSERT INTO Answer (question_id, text, isCorrect)
                VALUES (?, ?, ?)
            ''', (questionId, answer['text'], int(answer['isCorrect'])))

        # Sauvegarder et fermer
        conn.commit()
        conn.close()

        return jsonify({"message": "Question et réponses mises à jour avec succès."}), 204

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
