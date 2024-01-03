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


def get_team_stats(team_id):
    '''
    Fonction pour récupérer les statistiques de l'équipe avec l'ID donné
     '''
    # Liste pour stocker les statistiques de chaque équipe
    team_stats_list = []

    team_stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
        team_id=team_id,
        season=get_current_season(),
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )

    # Conversion des résultats en dictionnaire
    team_stats_dict = team_stats.get_normalized_dict()

    # Ajout des statistiques de l'équipe à la liste
    team_stats_list.append({
        'Id Team': team_id,
        'GamesPlayed': team_stats_dict['OverallTeamDashboard'][0]['GP'],
        'Points': team_stats_dict['OverallTeamDashboard'][0]['PTS'],
        'Rebounds': team_stats_dict['OverallTeamDashboard'][0]['REB'],
        'Assists': team_stats_dict['OverallTeamDashboard'][0]['AST'],
        'Somme': team_stats_dict['OverallTeamDashboard'][0]['PTS'] + team_stats_dict['OverallTeamDashboard'][0]['REB'] + team_stats_dict['OverallTeamDashboard'][0]['AST']
    })

    return team_stats_list


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
            'PlayerID': player_id,
            'Matchs joués': player_stats_dict['OverallPlayerDashboard'][0]['GP'],
            'Minutes jouées': player_stats_dict['OverallPlayerDashboard'][0]['MIN'],
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
            'Matchs joués': 0,
            'Minutes jouées': 0,
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


def main():
    # Liste des ID de team qui jouent ce soir
    team_ids = get_teams()

    for team_id in team_ids:
        team_stats = get_team_stats(team_id)
        print(f"Team {team_id} Stats: {team_stats}")

        player_ids = get_players(team_id)

        players_stats = [get_player_stats(player_id)
                         for player_id in player_ids]
        print(f"Players Stats: {players_stats}")

        # Pause pour éviter de surcharger l'API
        time.sleep(1)


if __name__ == "__main__":
    main()
