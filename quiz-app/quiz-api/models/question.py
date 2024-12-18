class Question:
    """
    Modèle représentant une question dans un quiz.
    """

    def __init__(self, id: int, position: int, title: str, text: str, image: str):
        """
        Initialise un objet Question.

        :param id: Identifiant unique de la question.
        :param position: Position de la question dans l'ordre du quiz.
        :param title: Titre ou résumé de la question.
        :param text: Texte complet de la question.
        :param image: URL ou chemin vers une image associée à la question.
        """
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet Question.

        :return: Chaîne formatée représentant les principaux attributs de l'objet Question.
        """
        return f"<Question(id={self.id}, position={self.position}, title='{self.title}')>"
