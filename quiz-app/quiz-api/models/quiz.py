class Quiz:
    """
    Modèle représentant un quiz.
    """
    def __init__(self, id: int, title: str, description: str, created_at: str):
        """
        Initialise un objet Quiz.

        :param id: Identifiant unique du quiz.
        :param title: Titre du quiz.
        :param description: Description du quiz.
        :param created_at: Date de création du quiz.
        """
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at

    def __repr__(self):
        """
        Représentation textuelle de l'objet Quiz.
        """
        return f"<Quiz(id={self.id}, title='{self.title}', created_at='{self.created_at}')>"
