class Question:
    """
    Modèle représentant une question dans un quiz.
    """
    def __init__(self, id: int, quiz_id: int, title: str, text: str, image: str):
        """
        Initialise un objet Question.

        :param id: Identifiant unique de la question.
        :param quiz_id: Identifiant du quiz associé.
        :param title: Titre ou résumé de la question.
        :param text: Texte complet de la question.
        :param image: URL ou chemin vers une image associée à la question.
        """
        self.id = id
        self.quiz_id = quiz_id
        self.title = title
        self.text = text
        self.image = image

    def __repr__(self):
        """
        Représentation textuelle de l'objet Question.
        """
        return f"<Question(id={self.id}, quiz_id={self.quiz_id}, title='{self.title}')>"
