class Answer:
    """
    Modèle représentant une réponse à une question dans un quiz.
    """

    def __init__(self, id: int, question_id: int, text: str, is_correct: bool, position: int):
        """
        Initialise un objet Answer.

        :param id: Identifiant unique de la réponse.
        :param question_id: Identifiant de la question associée.
        :param text: Texte de la réponse.
        :param is_correct: Booléen indiquant si la réponse est correcte (True) ou incorrecte (False).
        """
        self.id = id
        self.question_id = question_id
        self.position = position
        self.text = text
        self.is_correct = is_correct

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet Answer.

        :return: Chaîne de caractères représentant l'objet Answer avec ses principaux attributs.
        """
        return f"<Answer(id={self.id}, question_id={self.question_id}, is_correct={self.is_correct}, position={self.position})>"
