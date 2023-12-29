from datetime import datetime, timedelta, timezone
from nba_api.stats.endpoints import scoreboard
import dateparser
import gestion_bdd


def get_nba_schedule(current_date):
    calendar = []

    while current_date <= "2024-04-14":
        # Appel à l'API à travers le module Scoreboard pour récupérer les infos sur les matchs à la date concernée
        games = scoreboard.Scoreboard(
            day_offset=0, game_date=current_date).get_data_frames()[0]

        # Pour chacun des matchs du jour
        for index, row in games.iterrows():
            # On récupère la date et l'heure du match qu'on transforme en objet datetime.
            date_match = row['GAME_DATE_EST'].split('T')[0]
            heure_match = row['GAME_STATUS_TEXT']
            date_obj = dateparser.parse(
                f"{date_match} {heure_match}")
            # On convertit la date en timestamp
            timestamp = int(date_obj.replace(tzinfo=timezone.utc).timestamp())
            # On cré un dictionnaire avec uniquement les informations dont on a besoin
            game_info = {
                'timestamp': timestamp,
                'team_home': row['HOME_TEAM_ID'],
                'team_visitor': row['VISITOR_TEAM_ID']
            }
            # On ajoute ce match au calendrier
            calendar.append(game_info)

        # On ajoute une journée à la date courante
        current_date = (datetime.strptime(
            current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    return calendar


# Exemple d'utilisation
if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    nba_schedule = get_nba_schedule(current_date)

    connection = gestion_bdd.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            for game in nba_schedule:
                gestion_bdd.insert_match(cursor, game)
            connection.commit()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
