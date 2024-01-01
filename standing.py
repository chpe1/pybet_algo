from nba_api.stats.endpoints import leaguestandingsv3


def get_team_records():
    # Récupération du classement des équipes
    standings = leaguestandingsv3.LeagueStandingsV3()
    team_data = standings.get_normalized_dict()["Standings"]

    team_records = {}

    # Parcours des données des équipes
    for team_stats in team_data:
        team_id = team_stats["TeamID"]
        team_name = team_stats["TeamName"]
        home = team_stats["HOME"]
        road = team_stats["ROAD"]

        # Stockage les informations dans le dictionnaire
        team_records[team_id] = {
            "Team_Name": team_name, "Home": home, "Road": road}

    return team_records
