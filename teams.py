from nba_api.stats.static import teams
import gestion_bdd


def get_nba_teams():
    nba_teams = teams.get_teams()
    teams_dict = {}

    for team in nba_teams:
        team_id = team['id']
        team_name = team['full_name']
        teams_dict[team_id] = team_name

    return teams_dict


nba_teams_dict = get_nba_teams()
connection = gestion_bdd.create_connection()
if connection:
    try:
        cursor = connection.cursor()
        for id, team in nba_teams_dict.items():
            gestion_bdd.insert_team_id(cursor, id, team)
        connection.commit()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

print(nba_teams_dict)
