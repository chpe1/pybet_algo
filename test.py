from nba_api.stats.endpoints import commonallplayers, playerdashboardbygeneralsplits
from nba_api.stats.static import teams
import datetime

# Fonction pour obtenir la saison en cours
def get_current_season():
    now = datetime.datetime.now()
    if now.month >= 10:  # NBA saison commence en octobre
        return f"{now.year}-{now.year + 1 - 2000}"
    else:
        return f"{now.year - 1}-{now.year - 2000}"

# Paramètres pour la requête
per_mode = 'PerGame'  # 'PerGame' pour obtenir des statistiques par match

# Récupération de la liste des équipes
teams_info = teams.get_teams()

# Liste pour stocker les statistiques de chaque équipe
team_stats_list = []

# Boucle à travers chaque équipe
for team_info in teams_info:
    team_id = team_info['id']
    team_name = team_info['full_name']

    # Récupération de tous les joueurs actifs dans la ligue
    all_players = commonallplayers.CommonAllPlayers(is_active=True)

    # Filtrer les joueurs qui appartiennent à l'équipe actuelle
    team_players = [player for player in all_players.get_data_frames()[0].to_dict(orient='records') if player['TEAM_ID'] == team_id]

    # Liste pour stocker les statistiques de chaque joueur
    player_stats_list = []

    # Boucle à travers chaque joueur de l'équipe
    for player in team_players:
        player_id = player['PERSON_ID']

        # Appel de l'API pour obtenir les statistiques générales du joueur
        player_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
            player_id=player_id,
            season=get_current_season(),
            per_mode=per_mode
        )

        # Conversion des résultats en dictionnaire
        player_stats_dict = player_stats.get_normalized_dict()

        # Calcul de l'évaluation selon la formule
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
            player_stats_dict['OverallPlayerDashboard'][0]['TO'] -
            player_stats_dict['OverallPlayerDashboard'][0]['PF']
        )

        # Ajout des statistiques et de l'évaluation du joueur à la liste
        player_stats_list.append({
            'PlayerID': player_id,
            'Player': player['DISPLAY_FIRST_LAST'],
            'Points': player_stats_dict['OverallPlayerDashboard'][0]['PTS'],
            'Rebounds': player_stats_dict['OverallPlayerDashboard'][0]['REB'],
            'Assists': player_stats_dict['OverallPlayerDashboard'][0]['AST'],
            'Steals': player_stats_dict['OverallPlayerDashboard'][0]['STL'],
            'Blocks': player_stats_dict['OverallPlayerDashboard'][0]['BLK'],
            'FieldGoalsMade': player_stats_dict['OverallPlayerDashboard'][0]['FGM'],
            'FieldGoalsAttempted': player_stats_dict['OverallPlayerDashboard'][0]['FGA'],
            'ThreePointersMade': player_stats_dict['OverallPlayerDashboard'][0]['FG3M'],
            'ThreePointersAttempted': player_stats_dict['OverallPlayerDashboard'][0]['FG3A'],
            'Turnovers': player_stats_dict['OverallPlayerDashboard'][0]['TO'],
            'PersonalFouls': player_stats_dict['OverallPlayerDashboard'][0]['PF'],
            'Evaluation': evaluation
        })

    # Ajout des statistiques de l'équipe à la liste
    team_stats_list.append({
        'TeamID': team_id,
        'Team': team_name,
        'PlayerStats': player_stats_list
    })

# Affichage des statistiques de chaque équipe
for team_stats in team_stats_list:
    print(f"Team ID: {team_stats['TeamID']}, {team_stats['Team']}")
    for player_stats in team_stats['PlayerStats']:
        print(f"  {player_stats['Player']} - Points: {player_stats['Points']}, Rebounds: {player_stats['Rebounds']}, Assists: {player_stats['Assists']}, Evaluation: {player_stats['Evaluation']}")
