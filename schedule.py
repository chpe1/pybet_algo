from datetime import timezone, timedelta, datetime
from nba_api.stats.endpoints import scoreboard
from nba_api.stats.static import teams
import dateparser


# Récupération des matchs du jour et des 4 jours précédents.
def get_nba_schedule():
    aujourdhui = datetime.now()
    dates = []
    for i in range(5):
        date = (aujourdhui - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)

    calendar = []
    old_calendar = []

    # Flag pour savoir si on est sur le premier indice de la liste dates (date du jour) => Dans ce cas, on mettra les matchs dans un dictionnaire à part
    indice_dates = 0
    for day in dates:
        # Appel à l'API à travers le module Scoreboard pour récupérer les infos sur les matchs à la date concernée
        games = scoreboard.Scoreboard(
            day_offset=0, game_date=day).get_data_frames()[0]

        # Pour chacun des matchs du jour
        for index, row in games.iterrows():
            # On récupère la date et l'heure du match qu'on transforme en objet datetime.
            date_match = row['GAME_DATE_EST'].split('T')[0]
            heure_match = row['GAME_STATUS_TEXT']
            date_obj = dateparser.parse(f"{date_match} {heure_match}")
            if date_obj is None:
                date_obj = dateparser.parse(f"{date_match} 00:00:00")
            # On convertit la date en timestamp
            timestamp = int(date_obj.replace(tzinfo=timezone.utc).timestamp())
            # On cré un dictionnaire avec uniquement les informations dont on a besoin
            game_info = {
                'timestamp': timestamp,
                'date' : date_obj.strftime('%d-%m-%Y'),
                'team_home': row['HOME_TEAM_ID'],
                'team_visitor': row['VISITOR_TEAM_ID']
            }
            if indice_dates == 0:
                # On ajoute ce match au calendrier
                calendar.append(game_info)
            else:
                old_calendar.append(game_info)
        indice_dates += 1


    return calendar, old_calendar

def handicap(liste_teams, four_last_days):
    # Initialisation dunnombre de matchs à 1 pour l'équipe (puisqu'elle joue aujourd'hui de par sa présence dans liste_teams)
    date_veille = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
    handicap = dict()
    # Parcourir les équipes ayant un match aujourd'hui
    for equipe_id in liste_teams:
        # Pour débogage, affichage du nom de l'équipe
        # all_teams = teams.get_teams()
        # for team in all_teams:
        #     if team['id'] == equipe_id:
        #         print(team['full_name'] + '-' + str(equipe_id))
        # Fin débogage
        b2b = False
        handicap[equipe_id]=0
        nombre_matchs = 1
        for match in four_last_days:
            # Calcul du nombre de fois où l'équipe apparait dans le calendrier des 4 derniers jours
            if equipe_id == match['team_home'] or equipe_id == match['team_visitor']:
                nombre_matchs += 1
            # L'équipe a-t-elle joué la veille ?
            b2b = (match['team_home'] == equipe_id or match['team_visitor'] == equipe_id) and match['date'] == date_veille

        # Calcul du nombre de points à retirer en fonction de la valeur des différentes variables
        if b2b:
            handicap[equipe_id] -= 20
        if nombre_matchs > 1 and nombre_matchs < 3:
            handicap[equipe_id] -= 10
        if nombre_matchs > 2:
            handicap[equipe_id] -= 20

    return handicap

