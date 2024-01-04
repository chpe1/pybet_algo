import sqlite3


def query(requete, valeurs=None):
    connexion = sqlite3.connect("base_de_donnees.db")
    cursor = connexion.cursor()
    if valeurs is None:
        resultats = cursor.execute(requete).fetchall()
    else:
        resultats = cursor.execute(requete, valeurs).fetchall()
    connexion.commit()
    cursor.close()
    connexion.close()
    return resultats


# CREATE TABLE IF NOT EXISTS players (
#     id INTEGER PRIMARY KEY,
#     DISPLAY_FIRST_LAST TEXT,
#     TEAM_ID INTEGER,
#     GP REAL,
#     MIN REAL,
#     Points REAL,
#     Rebounds REAL,
#     Assists REAL,
#     Steals REAL,
#     Blocks REAL,
#     FieldGoalsMade REAL,
#     FieldGoalsAttempted REAL,
#     ThreePointersMade REAL,
#     ThreePointersAttempted REAL,
#     Turnovers REAL,
#     PersonalFouls REAL,
#     Evaluation REAL
# );
