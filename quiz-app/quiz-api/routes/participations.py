from flask import Blueprint, jsonify, request, Response
from database.init_db import init_db
from database import manage_position
import sqlite3
from security.jwt_utils import token_required

DATABASE_NAME = "database.db"

participation_bp = Blueprint('participation', __name__)

@participation_bp.route('/participations/all',methods=['DELETE'])
@token_required
def delete_all_participations():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('''
            DELETE FROM Participation
        ''')
        
        # Sauvegarde et fermeture
        conn.commit()
        conn.close()

        return Response('Delete PARTICIPATIONS table', status=204)
    
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@participation_bp.route('/participations', methods=['POST'])
def post_participation():
    try:
        payload = request.get_json()
        player_name = payload.get("playerName")
        answers = payload.get("answers")  # Liste des IDs de réponses choisies, indexée par position

        if not player_name or not answers:
            return jsonify({"error": "Les champs 'playerName' et 'answers' sont requis."}), 400

        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupérer toutes les questions et vérifier leur existence
        cursor.execute("SELECT id, position FROM Question;")
        questions = cursor.fetchall()
        total_questions = len(questions)

        if len(answers) != total_questions:
            return jsonify({"error": "Le nombre de réponses ne correspond pas au nombre de questions."}), 400

        # Insérer la participation
        cursor.execute("INSERT INTO Participation (playerName, score) VALUES (?, ?)", (player_name, 0))
        participation_id = cursor.lastrowid

        # Calculer le score
        score = 0
        for answer, index in enumerate(answers):

            # Vérifier si la réponse est correcte
            cursor.execute("SELECT isCorrect FROM Answer WHERE question_id = ? AND id = ?", (index, answer+1))
            result = cursor.fetchone()

            if result[0] == 1:  # Si la réponse est correcte
                score += 1

            # Enregistrer la réponse dans ParticipationAnswer
            cursor.execute("INSERT INTO ParticipationAnswer (participation_id, question_id, answer_id) VALUES (?, ?, ?)",
                           (participation_id, index, answer+1))

        # Mettre à jour le score dans la table Participation
        cursor.execute("UPDATE Participation SET score = ? WHERE id = ?", (score, participation_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Participation enregistrée avec succès.","playerName": player_name, "score": score}), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
