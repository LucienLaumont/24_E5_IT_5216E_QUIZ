
class Participation:
    """
    Modèle représentant une participation à un quiz.
    """

    def __init__(self, id: int, playerName: str):
        """
        Initialise une instance de Participation.

        :param id: Identifiant unique de la participation.
        :param playerName: Nom du joueur ayant effectué la participation.
        """
        self.id = id
        self.playerName = playerName

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'instance Participation.

        :return: Chaîne formatée avec les attributs de la participation.
        """
        return f"Participation(id={self.id}, playerName='{self.playerName}')"

class ParticipationAnswer:
    """
    Modèle représentant une réponse sélectionnée par un joueur pour une question donnée lors d'une participation.
    """

    def __init__(self, id: int, participation_id: int, question_id: int, answer_id: int):
        """
        Initialise un objet ParticipationAnswer.

        :param id: Identifiant unique de l'entrée.
        :param participation_id: Identifiant de la participation associée.
        :param question_id: Identifiant de la question associée.
        :param answer_id: Identifiant de la réponse sélectionnée.
        """
        self.id = id
        self.participation_id = participation_id
        self.question_id = question_id
        self.answer_id = answer_id

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet ParticipationAnswer.

        :return: Chaîne formatée représentant les principaux attributs de l'objet.
        """
        return (f"<ParticipationAnswer(id={self.id}, participation_id={self.participation_id}, "
                f"question_id={self.question_id}, answer_id={self.answer_id})>")
