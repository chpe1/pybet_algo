from nba_api.stats.endpoints import leaguestandingsv3
import schedule
import standing
from datetime import date, datetime, timedelta, timezone


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

liste_teams = [team_id for game in calendar for team_id in [
    game['team_home'], game['team_visitor']]]

# Calcul du pourcentage de victoire (home ou away) pour chaque équipe concerné
# Attribution du nombre de points équivalent au pourcentage à chaque équipe
# Ajout de ce nombre de points à eval_team
percentage(calendar, classement)

handicap_calendrier = schedule.handicap(liste_teams, old_calendar)
for equipe_id, handicap in handicap_calendrier.items():
    eval_team[equipe_id] += handicap

print()
