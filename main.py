from nba_api.stats.endpoints import leaguestandingsv3
import schedule
import standing
import players
from datetime import date, datetime, timedelta, timezone
import time


def percentage(match_data, team_records):
    # Calcul du pourcentage de victoire à domicile et à l'extérieur pour chaque équipe
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

            home_win_percentage = home_wins / (home_wins + home_losses) * 100
            road_win_percentage = road_wins / (road_wins + road_losses) * 100

            eval_team[home_team_id] += home_win_percentage
            eval_team[visitor_team_id] += road_win_percentage


# Récupération des matchs du jour et des 4 jours précédents
calendar, old_calendar = schedule.get_nba_schedule()

# Récupération du classement NBA
classement = standing.get_team_records()

# Création d'un dictionnaire informant de l'évalutation attribuée à chaque équipe concernée -> nbr de points de chaque équipe initialisé à 0
eval_team = {team_id: 0 for game in calendar for team_id in [
    game['team_home'], game['team_visitor']]}

# Création d'une liste avec l'ensemble des équipes qui jouent ce soir
liste_teams = [team_id for game in calendar for team_id in [
    game['team_home'], game['team_visitor']]]

# Calcul du pourcentage de victoire (home ou away) pour chaque équipe concernée par les matchs du soir
# Attribution du nombre de points équivalent au pourcentage à chaque équipe
# Ajout de ce nombre de points à eval_team
percentage(calendar, classement)

# Calcul d'un handicap en fonction du nombre de matchs joués lors des 5 derniers jours
handicap_calendrier = schedule.handicap(liste_teams, old_calendar)

# Retrait de ce handicap à l'évaluation de l'équipe.
for equipe_id, handicap in handicap_calendrier.items():
    eval_team[equipe_id] += handicap

# Récupération des statistiques des joueurs des équipes qui jouent ce soir.
for team_id in liste_teams:
    player_ids = players.get_players(team_id)
    players_stats = [players.get_player_stats(player_id) for player_id in player_ids]
    # Pause pour éviter de surcharger l'API
    time.sleep(1)

# Comme la récupération des stats des joueurs est longue, le mieux serait d'enregistrer les données dans une base de données SQLITE pour y accéder plus rapidement par la suite.

print()


"""
Exemple de données reçues par l'API la page players
{'PlayerID': {'PERSON_ID': 1630532, 'DISPLAY_LAST_COMMA_FIRST': 'Wagner, Franz', 'DISPLAY_FIRST_LAST': 'Franz Wagner', 'ROSTERSTATUS': 1, 'FROM_YEAR': '2021', 'TO_YEAR': '2023', 'PLAYERCODE': 'franz_wagner', 'PLAYER_SLUG': 'franz_wagner', 'TEAM_ID': 1610612753, 'TEAM_CITY': 'Orlando', 'TEAM_NAME': 'Magic', 'TEAM_ABBREVIATION': 'ORL', 'TEAM_CODE': 'magic', 'TEAM_SLUG': 'magic', 'GAMES_PLAYED_FLAG': 'Y', 'OTHERLEAGUE_EXPERIENCE_CH': '00'}, 'Points': 21.3, 'Rebounds': 6.0, 'Assists': 4.0, 'Steals': 1.2, 'Blocks': 0.4, 'FieldGoalsMade': 7.9, 'FieldGoalsAttempted': 16.9, 'ThreePointersMade': 1.4, 'ThreePointersAttempted': 4.9, 'Turnovers': 1.9, 'PersonalFouls': 2.4, 'Evaluation': 16.1}, 
{'PlayerID': {'PERSON_ID': 1629021, 'DISPLAY_LAST_COMMA_FIRST': 'Wagner, Moritz', 'DISPLAY_FIRST_LAST': 'Moritz Wagner', 'ROSTERSTATUS': 1, 'FROM_YEAR': '2018', 'TO_YEAR': '2023', 'PLAYERCODE': 'moritz_wagner', 'PLAYER_SLUG': 'moritz_wagner', 'TEAM_ID': 1610612753, 'TEAM_CITY': 'Orlando', 'TEAM_NAME': 'Magic', 'TEAM_ABBREVIATION': 'ORL', 'TEAM_CODE': 'magic', 'TEAM_SLUG': 'magic', 'GAMES_PLAYED_FLAG': 'Y', 'OTHERLEAGUE_EXPERIENCE_CH': '01'}, 'Points': 11.2, 'Rebounds': 4.4, 'Assists': 1.2, 'Steals': 0.5, 'Blocks': 0.3, 'FieldGoalsMade': 4.4, 'FieldGoalsAttempted': 7.3, 'ThreePointersMade': 0.5, 'ThreePointersAttempted': 1.6, 'Turnovers': 1.3, 'PersonalFouls': 2.2, 'Evaluation': 10.100000000000001}


"""
