import time
import schedule
from nba_api.stats.endpoints import playerdashboardbygeneralsplits, commonallplayers, teamdashboardbygeneralsplits
import datetime


def get_current_season():
    now = datetime.datetime.now()
    if now.month >= 10:  # NBA saison commence en octobre
        return f"{now.year}-{now.year + 1 - 2000}"
    else:
        return f"{now.year - 1}-{now.year - 2000}"


def get_teams():
    """
    Récupère l'ensemble des équipes qui jouent ce soir
    """
    calendar, old_calendar = schedule.get_nba_schedule()
    teams = list()
    for game in calendar:
        teams.append(game['team_home'])
        teams.append(game['team_visitor'])
    return teams


def get_players(team_id):

    # Récupération de tous les joueurs actifs dans la ligue
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=True)

    # Filtre des joueurs qui appartiennent à l'équipe actuelle
    team_players = [player for player in all_players.get_data_frames(
    )[0].to_dict(orient='records') if player['TEAM_ID'] == team_id]

    return team_players


def get_player_stats(player_id):
    '''
    Fonction pour récupérer les statistiques du joueur avec l'ID donné
    '''
    person_id = player_id['PERSON_ID']
    # Appel de l'API pour obtenir les statistiques générales du joueur
    player_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
        player_id=person_id,
        season=get_current_season(),
        per_mode_detailed='PerGame'
    )

    # Conversion des résultats en dictionnaire
    player_stats_dict = player_stats.get_normalized_dict()

    # Calcul de l'évaluation du joueur
    if len(player_stats_dict['OverallPlayerDashboard']) > 0:
        evaluation = (
            player_stats_dict['OverallPlayerDashboard'][0]['PTS'] +
            player_stats_dict['OverallPlayerDashboard'][0]['REB'] +
            player_stats_dict['OverallPlayerDashboard'][0]['AST'] +
            player_stats_dict['OverallPlayerDashboard'][0]['STL'] +
            player_stats_dict['OverallPlayerDashboard'][0]['BLK'] -
            player_stats_dict['OverallPlayerDashboard'][0]['FGA'] +
            player_stats_dict['OverallPlayerDashboard'][0]['FGM'] -
            player_stats_dict['OverallPlayerDashboard'][0]['FG3A'] +
            player_stats_dict['OverallPlayerDashboard'][0]['FG3M'] -
            player_stats_dict['OverallPlayerDashboard'][0]['TOV'] -
            player_stats_dict['OverallPlayerDashboard'][0]['PF']
        )

        # Ajout des statistiques du joueur à la liste
        player = {
            'PlayerID': person_id,
            'DISPLAY_FIRST_LAST': player_id['DISPLAY_FIRST_LAST'],
            'TEAM_ID': player_id['TEAM_ID'],
            'GP': player_stats_dict['OverallPlayerDashboard'][0]['GP'],
            'MIN': player_stats_dict['OverallPlayerDashboard'][0]['MIN'],
            'Points': player_stats_dict['OverallPlayerDashboard'][0]['PTS'],
            'Rebounds': player_stats_dict['OverallPlayerDashboard'][0]['REB'],
            'Assists': player_stats_dict['OverallPlayerDashboard'][0]['AST'],
            'Steals': player_stats_dict['OverallPlayerDashboard'][0]['STL'],
            'Blocks': player_stats_dict['OverallPlayerDashboard'][0]['BLK'],
            'FieldGoalsMade': player_stats_dict['OverallPlayerDashboard'][0]['FGM'],
            'FieldGoalsAttempted': player_stats_dict['OverallPlayerDashboard'][0]['FGA'],
            'ThreePointersMade': player_stats_dict['OverallPlayerDashboard'][0]['FG3M'],
            'ThreePointersAttempted': player_stats_dict['OverallPlayerDashboard'][0]['FG3A'],
            'Turnovers': player_stats_dict['OverallPlayerDashboard'][0]['TOV'],
            'PersonalFouls': player_stats_dict['OverallPlayerDashboard'][0]['PF'],
            'Evaluation': evaluation
        }
    else:
        # Ajout des statistiques du joueur à la liste
        player = {
            'PlayerID': person_id,
            'DISPLAY_FIRST_LAST': player_id['DISPLAY_FIRST_LAST'],
            'TEAM_ID': player_id['TEAM_ID'],
            'GP': 0,
            'MIN': 0,
            'Points': 0,
            'Rebounds': 0,
            'Assists': 0,
            'Steals': 0,
            'Blocks': 0,
            'FieldGoalsMade': 0,
            'FieldGoalsAttempted': 0,
            'ThreePointersMade': 0,
            'ThreePointersAttempted': 0,
            'Turnovers': 0,
            'PersonalFouls': 0,
            'Evaluation': 0
        }

    return player
