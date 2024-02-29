import get_player_stats, get_nba_props


def main():
    over_lines, under_lines = get_nba_props.main()
    for key in over_lines:
        print(key, over_lines[key])
        print(key, under_lines[key])
        player_stats = get_player_stats.main(key)
        if player_stats == -1:
            del over_lines[key]
            del under_lines[key]
        print(f"Player Stats for {key}:")
        print(f"PPG: {player_stats['PPG']:.2f}")
        print(f"RPG: {player_stats['RPG']:.2f}")
        print(f"FG%: {player_stats['FG%']:.2f}")
        print(f"3P%: {player_stats['3P%']:.2f}")

if __name__ == "__main__":
    main()