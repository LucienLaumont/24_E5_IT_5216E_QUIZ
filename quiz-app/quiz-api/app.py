from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib

from jwt_utils import build_token

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def PostLogin():
    try:
        # Récupération du payload JSON
        payload = request.get_json()

        # Validation de la présence du mot de passe
        if 'password' not in payload:
            return jsonify({"error": "Le champ 'password' est requis."}), 400

        # Récupération du mot de passe fourni
        tried_password = payload['password'].encode('UTF-8')
        hashed = hashlib.md5(tried_password).digest()

        # Comparaison avec un hachage précalculé
        if hashed == b'\xed\xc2z\xec!\xb6\xaee\xef\x91X.\x0c;\xdf\x19':
            token = build_token()
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Unauthorized"}), 401

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run()