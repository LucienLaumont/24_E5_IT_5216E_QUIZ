import sqlite3

def init_db(db_name="database.db"):
    """
    Initialise une base de données SQLite avec une table d'exemple.
    :param db_name: Nom de la base de données SQLite 
    """
    try:
        # Connexion à la base de données (ou création si elle n'existe pas)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        print(f"Base de données '{db_name}' connectée avec succès.")

        # Création d'une table (exemple : Question)
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

        # Création de la table Answer avec une foreign key vers Question
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

        # Sauvegarde et fermeture
        conn.commit()
        conn.close()
        print("Base de données initialisée et fermée avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")