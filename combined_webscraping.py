import get_player_stats, get_nba_props


def main():
    over_lines, under_lines = get_nba_props.main()
    for key in over_lines:
        print(key, over_lines[key])
        print(key, under_lines[key])
        get_player_stats.main(key)

if __name__ == "__main__":
    main()