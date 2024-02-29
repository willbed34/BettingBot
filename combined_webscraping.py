import get_player_stats, get_nba_props

def interpret_bet(player_name, bet):

    if bet[0] == "over":
        if bet[2] < 0:
            print(f"In order to win $100, you would need to bet ${bet[2]} that {player_name} scores more than {bet[1]} points.")
        else:
            print(f"In order to win ${bet[2]}, you would need to bet $100 that {player_name} scores more than {bet[1]} points.")
    else:
        if bet[2] < 0:
            print(f"In order to win $100, you would need to bet ${bet[2]} that {player_name} scores less than {bet[1]} points.")
        else:
            print(f"In order to win ${bet[2]}, you would need to bet $100 that {player_name} scores less than {bet[1]} points.")

def main():
    over_lines, under_lines = get_nba_props.main()
    for key in over_lines:
        print(key, over_lines[key])
        print(key, under_lines[key])
        player_stats = get_player_stats.main(key)
        if player_stats == -1:
            del over_lines[key]
            del under_lines[key]
        
        print(f"Player Stats for {key}, who is playing in {over_lines[key][3]} vs {over_lines[key][4]}:")
        print(f"PPG: {player_stats['PPG']:.2f}")
        print(f"RPG: {player_stats['RPG']:.2f}")
        print(f"FG%: {player_stats['FG%']:.2f}")
        print(f"3P%: {player_stats['3P%']:.2f}")
        print(f"SPG: {player_stats['SPG']:.2f}")  # Steals per game
        print(f"BPG: {player_stats['BPG']:.2f}")  # Blocks per game
        print(f"DRPG: {player_stats['DRPG']:.2f}")  # Defensive rebounds per game
        interpret_bet(key, over_lines[key])
        interpret_bet(key, under_lines[key])

if __name__ == "__main__":
    main()