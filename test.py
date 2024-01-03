from nba_api.stats.endpoints import commonallplayers, teamdashboardbygeneralsplits, playerdashboardbygeneralsplits
from nba_api.stats.static import teams
import datetime

# Récupération de la liste des équipes
teams_info = teams.get_teams()

# Fonction pour obtenir la saison en cours


def get_current_season():
    now = datetime.datetime.now()
    if now.month >= 10:  # NBA saison commence en octobre
        return f"{now.year}-{now.year + 1 - 2000}"
    else:
        return f"{now.year - 1}-{now.year - 2000}"


def stat_by_player(teams_info):
    # Liste pour stocker les statistiques de chaque équipe
    team_stats_list = []

    # Récupération de tous les joueurs actifs dans la ligue
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=True)

    # Boucle à travers chaque équipe
    for team in teams_info:
        team_id = team['id']

        # Filtrer les joueurs qui appartiennent à l'équipe actuelle
        team_players = [player for player in all_players.get_data_frames(
        )[0].to_dict(orient='records') if player['TEAM_ID'] == team_id]

        # Liste pour stocker les statistiques de chaque joueur
        player_stats_list = []

        # Boucle à travers chaque joueur de l'équipe
        for player in team_players:
            player_id = player['PERSON_ID']

            # Appel de l'API pour obtenir les statistiques générales du joueur
            player_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
                player_id=player_id,
                season=get_current_season(),
                per_mode_detailed='PerGame'
            )

            # Conversion des résultats en dictionnaire
            player_stats_dict = player_stats.get_normalized_dict()

            # Vérification si des statistiques sont disponibles
            if 'OverallPlayerDashboard' in player_stats_dict and player_stats_dict['OverallPlayerDashboard']:
                player_stats_data = player_stats_dict['OverallPlayerDashboard'][0]

                evaluation = (
                    player_stats_data.get('PTS', 0) +
                    player_stats_data.get('REB', 0) +
                    player_stats_data.get('AST', 0) +
                    player_stats_data.get('STL', 0) +
                    player_stats_data.get('BLK', 0) -
                    player_stats_data.get('FGA', 0) +
                    player_stats_data.get('FGM', 0) -
                    player_stats_data.get('FG3A', 0) +
                    player_stats_data.get('FG3M', 0) -
                    player_stats_data.get('TOV', 0) -
                    player_stats_data.get('PF', 0)
                )

                # Ajout des statistiques du joueur à la liste
                player_stats_list.append({
                    'PlayerID': player_id,
                    'Player': player['DISPLAY_FIRST_LAST'],
                    'Points': player_stats_data.get('PTS', 0),
                    'Rebounds': player_stats_data.get('REB', 0),
                    'Assists': player_stats_data.get('AST', 0),
                    'Steals': player_stats_data.get('STL', 0),
                    'Blocks': player_stats_data.get('BLK', 0),
                    'FieldGoalsMade': player_stats_data.get('FGM', 0),
                    'FieldGoalsAttempted': player_stats_data.get('FGA', 0),
                    'ThreePointersMade': player_stats_data.get('FG3M', 0),
                    'ThreePointersAttempted': player_stats_data.get('FG3A', 0),
                    'Turnovers': player_stats_data.get('TOV', 0),
                    'PersonalFouls': player_stats_data.get('PF', 0),
                    'Evaluation': evaluation
                })
            else:
                # Ajout des statistiques du joueur à la liste avec des valeurs par défaut
                player_stats_list.append({
                    'PlayerID': player_id,
                    'Player': player['DISPLAY_FIRST_LAST'],
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
                })
            # Ajout des statistiques de l'équipe à la liste
            team_stats_list.append({
                'TeamID': team_id,
                'Team': team['full_name'],
                'PlayerStats': player_stats_list
            })

    # Affichage des statistiques de chaque équipe
    for team_stats in team_stats_list:
        print(f"Team ID: {team_stats['TeamID']}, {team_stats['Team']}")
        for player_stats in team_stats['PlayerStats']:
            print(f"  {player_stats['Player']} - Points: {player_stats['Points']}, Rebounds: {player_stats['Rebounds']}, Assists: {player_stats['Assists']}, Evaluation: {player_stats['Evaluation']}")

    return team_stats_list


stat_by_player(teams_info)
print()
