import sqlite3

def increment_positions(cursor, position):
    """
    Incrémente les positions des questions existantes >= position donnée.
    """
    cursor.execute('''
        UPDATE Question
        SET position = position + 1
        WHERE position >= ?
    ''', (position,))

def decrement_positions(cursor, position):
    """
    Décrémente les positions des questions existantes > position donnée.
    
    :param cursor: Curseur de la base de données.
    :param position: Position seuil à partir de laquelle décrémenter.
    """
    cursor.execute('''
        UPDATE Question
        SET position = position - 1
        WHERE position > ?
    ''', (position,))