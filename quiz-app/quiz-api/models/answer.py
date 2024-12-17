
class Answer:
    def __init__(self, id: int, question_id: int, text: str, is_correct: bool):
        """
        Initialise un objet Answer.
        :param id: Identifiant unique de la réponse
        :param question_id: Identifiant de la question associée
        :param text: Texte de la réponse
        :param is_correct: Booléen indiquant si la réponse est correcte
        """
        self.id = id
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct

    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, is_correct={self.is_correct})>"
