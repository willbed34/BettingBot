from nba_api.stats.endpoints import playerdashboardbyyearoveryear
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Load teams file
teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
# Load players file
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

# Get team ID based on team abbreviation
def get_team_id(abv):
    for team in teams:
        if team['abbreviation'] == abv:
            return team['teamId']
    return -1

# Get player ID based on player name
def get_player_id(first, last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1

def get_player_stats(abv, firstName, lastName, season):
    player_id = get_player_id(firstName, lastName)
    
    # Create JSON request
    player_dashboard = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
        player_id=player_id,
        season=season
    )

    data = player_dashboard.get_data_frames()[0]
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(data.loc[0])

    # Extract relevant statistics
    stats = {
        "PPG": data.loc[0, 'PTS'] / data.loc[0, 'GP'],  # Points per game
        "RPG": data.loc[0, 'REB'] / data.loc[0, 'GP'],  # Rebounds per game
        "FG%": data.loc[0, 'FG_PCT'],  # Field goal percentage
        "3P%": data.loc[0, 'FG3_PCT'],  # Three-point percentage
        # Add more statistics as needed
    }

    return stats

# def get_espn_game_url(team1, team2):
#     # Load ESPN NBA scoreboard page
#     team_abv = "phi"
#     url = f"https://www.espn.com/nba/team/schedule/_/name/phi"
#     response = requests.get(url)
#     print(response.status_code)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         # Find the link corresponding to the game between team1 and team2
#         schedule_table = soup.find('tbody', class_='Table__TBODY')
#         games = schedule_table.find_all('tr')
#         for game in games[1:]:
#             game_data = game.find_all('td')
#             opp = game_data[1].find("div").find_all("span")[2].find("a").text
#             print("Opp: ", opp)

#     else:
#         print("Failed to retrieve data.")

def get_stats(player_name, team_name):
    player_name = player_name.lower().strip().replace(" ", "-")
    team_name = team_name.lower().strip().replace(" ", "-")
    url = f"https://www.nba.com/{team_name}/{player_name}"
    print(url)
    # url = "https://www.nba.com/sixers/joel-embiid"
    response = requests.get(url)
    print(response.status_code)
    player_page = BeautifulSoup(response.content, 'html.parser')

    stat_ids = ["pointsPerGame", "assistsPerGame", "stealsPerGame", "reboundsPerGame"]
    for stat_id in stat_ids:
        current_stat = player_page.find('p', id=stat_id)
        print(stat_id, ": ",current_stat)
    # stat_names = player_page.find_all("p", class_ = "stats-number")
    # for stat_name in stat_names:
    #     print("hey")
    #     print(stat_name.text)





if __name__ == "__main__":
    current_season = '2023-24'  # Adjust this as needed for the current season
    player_name = "Joel Embiid"

    player_stats = get_player_stats("PHI", *player_name.split(), current_season)

    print(f"Player Stats for {player_name} ({current_season}):")
    print(f"PPG: {player_stats['PPG']:.2f}")
    print(f"RPG: {player_stats['RPG']:.2f}")
    print(f"FG%: {player_stats['FG%']:.2f}")
    print(f"3P%: {player_stats['3P%']:.2f}")


    # player_name = "Joel Embiid"
    # player_team = "Sixers"
    # get_stats(player_name, player_team)
    # # game_url = get_espn_game_url("76ers", "Celtics")
    # # if game_url:
    # #     print("ESPN URL for the game:", game_url)
