from flask import Blueprint, jsonify
import sqlite3

DATABASE_NAME = "database.db"

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@health_bp.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Récupérer le nombre de questions dans la table Question
        cursor.execute("SELECT COUNT(*) FROM Question;")
        size = cursor.fetchone()[0]

        # Récupérer tous les scores de la table Participation
        cursor.execute("SELECT score FROM Participation;")
        scores = [row[0] for row in cursor.fetchall()]

        # Fermer la connexion
        conn.close()

        return jsonify({"size": size, "scores": scores}), 200

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500
