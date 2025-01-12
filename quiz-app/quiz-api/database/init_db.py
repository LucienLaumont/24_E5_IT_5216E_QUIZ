import sqlite3

def init_db(db_name="quiz.db"):
    """
    Initialise une base de données SQLite avec les tables nécessaires pour un quiz.
    :param db_name: Nom de la base de données SQLite.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        print(f"Base de données '{db_name}' connectée avec succès.")

        cursor.execute('PRAGMA foreign_keys = ON;')

        # Table Question
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER NOT NULL,
                title TEXT,
                text TEXT,
                image TEXT
            );
        ''')
        print("Table 'Question' créée avec succès.")

        # Table Answer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT,
                isCorrect BOOL,
                FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE
            );
        ''')
        print("Table 'Answer' créée avec succès.")

        # Table Participation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Participation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                PlayerName TEXT NOT NULL,
                score INT,
                participation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Table 'Participation' créée avec succès.")

        # Table ParticipationAnswer (réponses sélectionnées par le joueur pour chaque question)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ParticipationAnswer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participation_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer_id INTEGER NOT NULL,
                FOREIGN KEY (participation_id) REFERENCES Participation(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE,
                FOREIGN KEY (answer_id) REFERENCES Answer(id) ON DELETE CASCADE
            );
        ''')
        print("Table 'ParticipationAnswer' créée avec succès.")

        # Sauvegarde et fermeture
        conn.commit()
        conn.close()
        print("Base de données initialisée et fermée avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")

# Exemple d'utilisation
init_db()
