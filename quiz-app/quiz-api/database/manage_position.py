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