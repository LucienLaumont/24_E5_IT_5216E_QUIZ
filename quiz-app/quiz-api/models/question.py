
class Question:
    def __init__(self, id: int, position: int, title: str, text: str, image: str):
        """
        Initialise un objet Question.
        :param id: Identifiant unique de la question
        :param position: Position de la question
        :param title: Titre de la question
        :param text: Texte de la question
        :param image: Lien vers l'image associée
        """
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image

    def __repr__(self):
        return f"<Question(id={self.id}, position={self.position}, title='{self.title}')>"
