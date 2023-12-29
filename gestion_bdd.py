import mysql.connector
from mysql.connector import Error


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='nba',
            user='root',
            password=''
        )
        if connection.is_connected():
            print(
                f"Connecté à la base de données MySQL (version {connection.get_server_info()})")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return None


def insert_match(cursor, game):
    try:
        cursor.execute("""
            INSERT INTO calendrier (timestamp, id_team_home, id_team_visitor)
            VALUES (%s, %s, %s)
        """, (game['timestamp'], game['team_home'], game['team_visitor']))
    except Error as e:
        print(f"Erreur lors de l'insertion du match : {e}")


def insert_team_id(cursor, id, team):
    try:
        cursor.execute("""
            INSERT INTO teams (id_teams, full_name)
            VALUES (%s, %s)
        """, (id, team))
    except Error as e:
        print(f"Erreur lors de l'insertion du match : {e}")
