from nba_api.stats.endpoints import leaguestandingsv3
from nba_api.stats.endpoints import scoreboard
import dateparser
import standing
from datetime import date, datetime, timedelta, timezone

# Date du jour
current_date = date.today()

# Afficher la date du jour
print("Date du jour :", current_date)


# Récupération des matchs du jour
def get_nba_schedule(current_date):
    calendar = []

    # Appel à l'API à travers le module Scoreboard pour récupérer les infos sur les matchs à la date concernée
    games = scoreboard.Scoreboard(
        day_offset=0, game_date=current_date).get_data_frames()[0]

    # Pour chacun des matchs du jour
    for index, row in games.iterrows():
        # On récupère la date et l'heure du match qu'on transforme en objet datetime.
        date_match = row['GAME_DATE_EST'].split('T')[0]
        heure_match = row['GAME_STATUS_TEXT']
        date_obj = dateparser.parse(f"{date_match} {heure_match}")
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

    return calendar


def get_team_records():
    # Obtenir les classements actuels des équipes
    standings = leaguestandingsv3.LeagueStandingsV3()

    # Obtenir les données des équipes
    team_data = standings.get_normalized_dict()["Standings"]

    # Créer un dictionnaire pour stocker les informations sur les équipes
    team_records = {}

    # Parcourir les données des équipes
    for team_stats in team_data:
        team_id = team_stats["TeamID"]
        team_name = team_stats["TeamName"]
        wins = team_stats["WINS"]
        losses = team_stats["LOSSES"]
        home = team_stats["HOME"]
        road = team_stats["ROAD"]

        # Stocker les informations dans le dictionnaire
        team_records[team_id] = {
            "Team_Name": team_name, "Wins": wins, "Losses": losses, "Home": home, "Road": road}

    return team_records


def pourcentage(match_data, team_records):
    # Calculer le pourcentage de victoire à domicile et à l'extérieur pour chaque équipe
    for match in match_data:
        home_team_id = match['team_home']
        visitor_team_id = match['team_visitor']

        if home_team_id in team_records and visitor_team_id in team_records:
            home_wins = int(team_records[home_team_id]["Home"].split('-')[0])
            home_losses = int(team_records[home_team_id]["Home"].split('-')[1])
            road_wins = int(
                team_records[visitor_team_id]["Road"].split('-')[0])
            road_losses = int(
                team_records[visitor_team_id]["Road"].split('-')[1])

            # Calculer le pourcentage de victoire
            home_win_percentage = home_wins / (home_wins + home_losses) * 100
            road_win_percentage = road_wins / (road_wins + road_losses) * 100

            eval_team[home_team_id] += home_win_percentage
            eval_team[visitor_team_id] += road_win_percentage


schedule = get_nba_schedule(current_date)
eval_team = {team_id: 0 for game in schedule for team_id in [
    game['team_home'], game['team_visitor']]}


classement = get_team_records()
pourcentage(schedule, classement)


# for team, data in classement.items():
# eval_team['team'] =

print()
