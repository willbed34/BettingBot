# https://github.com/M4THYOU/prop_odds_python_example/blob/main/main.py
import requests
import urllib
from datetime import datetime

BASE_URL = 'https://api.prop-odds.com/beta'
LEAGUE = 'nba'
API_KEY = 'TpGZ71Ti8KQagTLtyUh2YVKV6WQCucXq7a9CX5zmH8'

def get_daily_games():
    current_date = datetime.now().strftime('%Y-%m-%d')
    #TODO: REMOVE ONCE READY FOR PRODUCTION, HARDCODING SO WE CAN TEST W/O WAITING FOR LINES
    current_date = "2024-02-28"
    url = f"{BASE_URL}/games/{LEAGUE}?date={current_date}&tz=America/New_York&api_key={API_KEY}"
    response = requests.get(url)
    daily_games = response.json()["games"]
    
    print("Available games for today:")
    for i, daily_game in enumerate(daily_games, 1):
        print(f"{i}. {daily_game['home_team']} vs. {daily_game['away_team']}")
    
    selected_game_index = int(input("Enter the number of the game you want to select: ")) - 1
    
    selected_game = daily_games[selected_game_index]

    print("Getting props for", selected_game["home_team"], "vs.", selected_game["away_team"])

    return selected_game["game_id"], selected_game["home_team"], selected_game["away_team"]
    
    
    


def get_props(game_id, home_team, away_team):
    url = f"{BASE_URL}/markets/{game_id}?api_key={API_KEY}"
    #https://api.prop-odds.com/beta/markets/562e11a59b19631a0e96a18894e4985c/?/api_key=TpGZ71Ti8KQagTLtyUh2YVKV6WQCucXq7a9CX5zmH8
    #https://api.prop-odds.com/beta/markets/ee5c9178cf8d6f4d7bc81897a76b542d?api_key=TpGZ71Ti8KQagTLtyUh2YVKV6WQCucXq7a9CX5zmH8

    print(url)
    response = requests.get(url)
    game_props = response.json()
    # print("prop: ", game_props["markets"][0]["name"])
    specific_prop = "player_points_over_under"
    # for game_prop in game_props["markets"]:
    #     print("prop: ", game_prop["name"])
    # https://api.prop-odds.com/beta/odds/ee5c9178cf8d6f4d7bc81897a76b542d/player_first_goal?api_key=TpGZ71Ti8KQagTLtyUh2YVKV6WQCucXq7a9CX5zmH8
    player_overs = {}
    player_unders = {}
    specific_url = f"{BASE_URL}/odds/{game_id}/{specific_prop}?api_key={API_KEY}"
    specific_response = requests.get(specific_url)
    odds = specific_response.json()
    print("keys: ", odds.keys())
    for item in odds["sportsbooks"][0]["market"]["outcomes"]:
        #we want player, if its over/under, value, odds
        bet_odds = item["odds"]  # Get handicap value
        if 'over' in item['name'].lower():
            bet_type = 'over'
            player_name = item['name'].split(' Over ')[0]
            bet_value = item['name'].split(' Over ')[-1]
        else:
            bet_type = 'under'
            player_name = item['name'].split(' Under ')[0]
            bet_value = item['name'].split(' Under ')[-1]
        
        if not (player_name.split()[-1] == "Over") and bet_type == "over":
            if player_name not in player_overs:
                player_overs[player_name] = [bet_type, float(bet_value), bet_odds, home_team, away_team]
        if not (player_name.split()[-1] == "Under") and bet_type == "under":
            if player_name not in player_unders:
                player_unders[player_name] = [bet_type, float(bet_value), bet_odds, home_team, away_team]

    # for key in player_overs.keys():
    #     print(key, player_overs[key])
    #     print(key, player_unders[key])
    return player_overs, player_unders
def main():
    selected_game_id, home_team, away_team = get_daily_games()
    return get_props(selected_game_id, home_team, away_team)

if __name__ == '__main__':
    main()
