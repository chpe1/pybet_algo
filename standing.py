from nba_api.stats.endpoints import leaguestandingsv3


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


# Exemple d'utilisation de la fonction
if __name__ == "__main__":
    team_records = get_team_records()

    # Afficher les informations
    for team_name, records in team_records.items():
        print(
            f"{team_name}: Victoires - {records['Wins']}, Défaites - {records['Losses']}")
