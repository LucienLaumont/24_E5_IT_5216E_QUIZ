import jwt
import datetime
from werkzeug.exceptions import Unauthorized
from functools import wraps
from flask import request, jsonify

class JwtError(Exception):
    """Exception raised for jwt errors in the quiz app 
    """

    def __init__(self, message="Jwt error"):
        self.message = message
        super().__init__(self.message)


secret = "LeonMarchandestlemeilleur!"
expiration_in_seconds = 3600


def build_token():
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_in_seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': 'quiz-app-admin'
        }
        return jwt.encode(
            payload,
            secret,
            algorithm="HS256"
        )
    except Exception as e:
        return e


def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret, algorithms="HS256")
        # if decoding did not fail, this means we are correctly logged in
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise JwtError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError as e:
        raise JwtError('Invalid token. Please log in again.')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Vérifiez si un token est fourni dans les en-têtes HTTP
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Format: Bearer <token>

        if not token:
            return jsonify({"error": "Token manquant. Accès non autorisé."}), 403

        try:
            # Décoder le token
            data = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expiré. Veuillez vous reconnecter."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalide. Veuillez vous reconnecter."}), 401

        return f(*args, **kwargs)

    return decorated