from nba_api.stats.endpoints import playerdashboardbygeneralsplits, commonallplayers, teamdashboardbygeneralsplits
from nba_api.stats.static import teams, players
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


def stat_by_team(teams_info):
    season_type = 'Regular Season'

    # Liste pour stocker les statistiques de chaque équipe
    team_stats_list = []

    # Boucle à travers chaque équipe
    for team in teams_info:
        team_id = team['id']
        
        # Appel de l'API pour obtenir les statistiques générales de l'équipe
        team_stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
            team_id=team_id,
            season=get_current_season(),
            season_type_all_star=season_type,
            per_mode_detailed='PerGame'
        )
        
        # Conversion des résultats en dictionnaire
        team_stats_dict = team_stats.get_normalized_dict()
        
        # Ajout des statistiques de l'équipe à la liste
        team_stats_list.append({
            'Id Team': team_id,
            'Team': team['full_name'],
            'GamesPlayed': team_stats_dict['OverallTeamDashboard'][0]['GP'],
            'Points': team_stats_dict['OverallTeamDashboard'][0]['PTS'],
            'Rebounds': team_stats_dict['OverallTeamDashboard'][0]['REB'],
            'Assists': team_stats_dict['OverallTeamDashboard'][0]['AST'],
            'Somme': team_stats_dict['OverallTeamDashboard'][0]['PTS'] + team_stats_dict['OverallTeamDashboard'][0]['REB'] + team_stats_dict['OverallTeamDashboard'][0]['AST']
        })
    # Affichage des statistiques de chaque équipe
    for stats in team_stats_list:
        print(f"{stats['Team']} - Points: {stats['Points']}, Rebounds: {stats['Rebounds']}, Assists: {stats['Assists']}")
    return team_stats_list

def stat_by_player(teams_info):
    # Liste pour stocker les statistiques de chaque équipe
    team_stats_list = []

    # Boucle à travers chaque équipe
    for team in teams_info:
        team_id = team['id']

        # Récupération de tous les joueurs actifs dans la ligue
        all_players = commonallplayers.CommonAllPlayers(is_only_current_season=True)

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
                per_mode_detailed='PerGame'
            )
            
            # Conversion des résultats en dictionnaire
            player_stats_dict = player_stats.get_normalized_dict()

            # Calcul de l'évaluation du joueur
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
            'Turnovers': player_stats_dict['OverallPlayerDashboard'][0]['TOV'],
            'PersonalFouls': player_stats_dict['OverallPlayerDashboard'][0]['PF'],
            'Evaluation': evaluation
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