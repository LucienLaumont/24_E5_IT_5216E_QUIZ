from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib

from routes.health import health_bp
from routes.questions import question_bp
from routes.participations import participation_bp
from routes.quizzes import quiz_bp
from security.jwt_utils import build_token, token_required

app = Flask(__name__)
CORS(app)

# Enregistrement des blueprints
app.register_blueprint(health_bp)
app.register_blueprint(question_bp)
app.register_blueprint(participation_bp)
app.register_blueprint(quiz_bp)

@app.route('/login', methods=['POST'])
def post_login():
    try:
        payload = request.get_json()

        if 'password' not in payload:
            return jsonify({"error": "Le champ 'password' est requis."}), 400

        tried_password = payload['password'].encode('UTF-8')
        hashed = hashlib.md5(tried_password).digest()

        if hashed == b'\xed\xc2z\xec!\xb6\xaee\xef\x91X.\x0c;\xdf\x19':
            token = build_token()
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Unauthorized"}), 401

    except Exception as e:
        return jsonify({"error": "Une erreur s'est produite.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
