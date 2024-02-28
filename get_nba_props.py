# https://github.com/M4THYOU/prop_odds_python_example/blob/main/main.py
import requests
import urllib
from datetime import datetime

BASE_URL = 'https://api.prop-odds.com/beta'
LEAGUE = 'nba'
API_KEY = 'TpGZ71Ti8KQagTLtyUh2YVKV6WQCucXq7a9CX5zmH8'

def get_daily_games():
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f"{BASE_URL}/games/{LEAGUE}?date={current_date}&tz=America/New_York&api_key={API_KEY}"
    response = requests.get(url)
    daily_games = response.json()["games"]
    for daily_game in daily_games:
        print("Getting props for", daily_game["home_team"], "vs.", daily_game["away_team"])
        get_props(daily_game["game_id"])
        break;


def get_props(game_id):
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
    player_ous = {}
    specific_url = f"{BASE_URL}/odds/{game_id}/{specific_prop}?api_key={API_KEY}"
    specific_response = requests.get(specific_url)
    odds = specific_response.json()
    for item in odds["sportsbooks"][0]["market"]["outcomes"]:
        #we want player, if its over/under, value, odds
        bet_odds = item["odds"]  # Get handicap value
        #only do overs
        if 'over' in item['name'].lower():
            bet_type = 'over'
            player_name = item['name'].lower().split(' over ')[0]
            bet_value = item['name'].lower().split(' over ')[-1]
        else:
            continue
        player_bet_info = [bet_type, bet_value, bet_odds]
        if player_name.split()[-1] != "over":
            if player_name not in player_ous:
                player_ous[player_name] = player_bet_info
    for key in player_ous.keys():
        print(key, player_ous[key])
def main():
    get_daily_games()


if __name__ == '__main__':
    main()
