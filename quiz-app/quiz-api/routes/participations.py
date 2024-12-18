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

        # Récupérer les réponses correctes avec l'index dans le groupe de réponses
        cursor.execute('''
            SELECT q.position, a.id, 
                (SELECT COUNT(*) 
                    FROM Answer a2 
                    WHERE a2.question_id = a.question_id AND a2.id < a.id) AS answer_index
            FROM Question q
            LEFT JOIN Answer a ON q.id = a.question_id
            WHERE a.isCorrect = 1
            ORDER BY q.position;
        ''')

        # Construire le dictionnaire {position: index de la réponse correcte}
        correct_answers = {row[0]: row[2]+1 for row in cursor.fetchall()}

        # Vérifier le nombre de questions
        total_questions = len(correct_answers)
        if len(answers) != total_questions:
            return jsonify({"error": "Le nombre de réponses ne correspond pas au nombre de questions."}), 400

        # Insérer la participation
        cursor.execute("INSERT INTO Participation (playerName, score) VALUES (?, ?)", (player_name, 0))
        participation_id = cursor.lastrowid

        print(correct_answers)
        print(answers)
        # Calculer le score
        score = 0
        for position, user_answer_id in enumerate(answers):
            # Vérifier si la réponse est correcte
            correct_answer_id = correct_answers.get(position+1)
            print(correct_answer_id,user_answer_id)
            if correct_answer_id == user_answer_id:
                score += 1

            # Enregistrer la réponse de l'utilisateur dans ParticipationAnswer
            cursor.execute("""
                INSERT INTO ParticipationAnswer (participation_id, question_id, answer_id)
                SELECT ?, q.id, ?
                FROM Question q
                WHERE q.position = ?
            """, (participation_id, user_answer_id, position))

        # Mettre à jour le score dans la table Participation
        cursor.execute("UPDATE Participation SET score = ? WHERE id = ?", (score, participation_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Participation enregistrée avec succès.", "playerName": player_name, "score": score}), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


@participation_bp.route('/correct-answers', methods=['GET'])
def get_correct_answers():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Exécuter la requête pour récupérer les réponses correctes
        cursor.execute('''
            SELECT q.position, a.id
            FROM Question q
            LEFT JOIN Answer a ON q.id = a.question_id
            WHERE a.isCorrect = 1
            ORDER BY q.position;
        ''')
        results = cursor.fetchall()

        # Générer la liste où l'indice correspond à la position
        correct_answers = [None] * (max([row[0] for row in results]) + 1)  # Crée une liste basée sur les positions
        for position, answer_id in results:
            correct_answers[position] = answer_id

        conn.close()

        return jsonify(correct_answers), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
