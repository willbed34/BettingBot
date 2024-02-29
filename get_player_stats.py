from nba_api.stats.endpoints import playerdashboardbyyearoveryear
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nba_api.stats.static import players
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

# Load teams file
# teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
# # Load players file
# players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)


# Get team ID based on team abbreviation
def get_team_id(team_name):
    team_id = [x for x in teams if x['full_name'] == team_name][0]['id']
    return team_id

# Get player ID based on player name
def get_player_id(player_name):
    try:
        player_dict = players.get_players()
        # 'id', 'full_name', 'first_name', 'last_name', 'is_active'
        player_id = [player for player in player_dict if player['full_name'] == player_name][0]["id"]
        return player_id
    except:
        return -1

def get_player_season_stats(player_name, season):
    player_id = get_player_id(player_name)
    if player_id == -1:
        return -1
    
    # Create JSON request
    player_dashboard = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
        player_id=player_id,
        season=season
    )

    data = player_dashboard.get_data_frames()[0]
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # print(data.loc[0])

    # Extract relevant statistics
    stats = {
        "PPG": data.loc[0, 'PTS'] / data.loc[0, 'GP'],  # Points per game
        "RPG": data.loc[0, 'REB'] / data.loc[0, 'GP'],  # Rebounds per game
        "FG%": data.loc[0, 'FG_PCT'],  # Field goal percentage
        "3P%": data.loc[0, 'FG3_PCT'],  # Three-point percentage
        "SPG": data.loc[0, 'STL'] / data.loc[0, 'GP'],  # Steals per game
        "BPG": data.loc[0, 'BLK'] / data.loc[0, 'GP'],  # Blocks per game
        "DRPG": data.loc[0, 'DREB'] / data.loc[0, 'GP'],  # Defensive rebounds per game
    }

    return stats

def get_player_gamelogs(player_name):
    player_id = get_player_id(player_name)
    if player_id == -1:
        return -1
    gamelog = pd.concat(playergamelog.PlayerGameLog(player_id=player_id, season=SeasonAll.all).get_data_frames())
    gamelog["GAME_DATE"] = pd.to_datetime(gamelog["GAME_DATE"], format="%b %d, %Y")
    gamelog = gamelog.query("GAME_DATE.dt.year in [2021, 2022, 2023]")
    print(gamelog)
    #do db stuff here, so we don't repetitively add gamelog to database
    


def main(player_name):
    current_season = '2023-24'  # Adjust this as needed for the current season

    player_stats = get_player_season_stats(player_name, current_season)
    get_player_gamelogs(player_name)
    return player_stats




if __name__ == "__main__":
    main()


# def get_stats(player_name, team_name):
#     player_name = player_name.lower().strip().replace(" ", "-")
#     team_name = team_name.lower().strip().replace(" ", "-")
#     url = f"https://www.nba.com/{team_name}/{player_name}"
#     print(url)
#     # url = "https://www.nba.com/sixers/joel-embiid"
#     response = requests.get(url)
#     print(response.status_code)
#     player_page = BeautifulSoup(response.content, 'html.parser')

#     stat_ids = ["pointsPerGame", "assistsPerGame", "stealsPerGame", "reboundsPerGame"]
#     for stat_id in stat_ids:
#         current_stat = player_page.find('p', id=stat_id)
#         print(stat_id, ": ",current_stat)
#     # stat_names = player_page.find_all("p", class_ = "stats-number")
#     # for stat_name in stat_names:
#     #     print("hey")
#     #     print(stat_name.text)