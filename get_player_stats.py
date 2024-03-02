from nba_api.stats.endpoints import playerdashboardbyyearoveryear
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nba_api.stats.static import players
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import sqlite3
import constants
stat_keys = constants.STAT_KEYS

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

def get_player_season_stats(player_id, season):
    
    # Create JSON request
    player_dashboard = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
        player_id=player_id,
        season=season
    )

    data_frames = player_dashboard.get_data_frames()
    
    if not data_frames:
        print("No data available.")
        return -1
    
    data = data_frames[0]
    
    if data.empty:
        print("Empty DataFrame. No meaningful data available.")
        return -1

    # Extract relevant statistics
    stats = {
        stat_keys[0]: data.loc[0, 'PTS'] / data.loc[0, 'GP'],  # Points per game
        stat_keys[1]: data.loc[0, 'REB'] / data.loc[0, 'GP'],  # Rebounds per game
        stat_keys[2]: data.loc[0, 'FG_PCT'],  # Field goal percentage
        stat_keys[3]: data.loc[0, 'FG3_PCT'],  # Three-point percentage
        stat_keys[4]: data.loc[0, 'STL'] / data.loc[0, 'GP'],  # Steals per game
        stat_keys[5]: data.loc[0, 'BLK'] / data.loc[0, 'GP'],  # Blocks per game
        stat_keys[6]: data.loc[0, 'DREB'] / data.loc[0, 'GP'],  # Defensive rebounds per game
    }

    return stats

def get_player_gamelogs(player_id):
    #returns player gamelog. can be filtered after based on home games, vs a certain team, etc
    
    gamelog_df = pd.concat(playergamelog.PlayerGameLog(player_id=player_id, season=SeasonAll.all).get_data_frames())
    # gamelog["GAME_DATE"] = pd.to_datetime(gamelog["GAME_DATE"], format="%b %d, %Y")
    # gamelog = gamelog.query("GAME_DATE.dt.year in [2021, 2022, 2023, 2024]")
    #get stats only against certain team
    # print(gamelog_df.columns)
    return gamelog_df
    #do db stuff here, so we don't repetitively add gamelog to database
    #get headers
    #actually put season stats in database

def get_games_vs_specific_team(gamelog_df, team_abv):
    print(gamelog_df.columns)
    was_games_df = gamelog_df[gamelog_df["MATCHUP"].str.contains(team_abv)]
    return was_games_df





def main(player_name):
    player_id = get_player_id(player_name)
    if player_id == -1:
        return -1
    current_season = '2023-24'  # Adjust this as needed for the current season

    
    player_stats = get_player_season_stats(player_id, current_season)
    return player_stats

def put_players_in_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Delete tables if they exist
    c.execute('DROP TABLE IF EXISTS "players";')
    c.execute('DROP TABLE IF EXISTS "player_2024_stats";')

    # Create Companies table
    c.execute('''CREATE TABLE players (
                player_id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE player_2024_stats (
                player_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                PPG REAL NOT NULL,
                RPG REAL NOT NULL,
                FGPCT REAL NOT NULL,
                THREEPCT REAL NOT NULL,
                SPG REAL NOT NULL,
                BPG REAL NOT NULL,
                DRPG REAL NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(player_id)
                )''')
    conn.commit()
    player_dict = players.get_players()
    current_season = '2023-24'
    i = 0
    # 'id', 'full_name', 'first_name', 'last_name', 'is_active'
    for player in player_dict:
        cur_id = player["id"]
        player_name = player["full_name"]
        is_active = player["is_active"]
        if is_active:
            print(i, " getting: ", player_name)
            player_stats = get_player_season_stats(cur_id, current_season)
            # print(player_stats)
            if player_stats == -1:
                print(f"No stats for {player_name}")
                continue
            c.execute('INSERT INTO players VALUES (?, ?)', (cur_id, player_name))

            insert_values = tuple([cur_id, player_name] + [player_stats[x] for x in stat_keys])
            c.execute('INSERT INTO player_2024_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', insert_values)
            i += 1
    conn.commit()

if __name__ == "__main__":
    # player_stats = get_player_season_stats(2544, '2023-24')
    # print(player_stats)
    # put_players_in_database()
    lebron_gamelog = get_player_gamelogs(2544)
    lebron_vs_was = get_games_vs_specific_team(lebron_gamelog, "WAS")
    print(lebron_vs_was)
