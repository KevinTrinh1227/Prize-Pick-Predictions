from find_player import get_player_stats

# Get player name from user input
player_name = input("Enter player name: ")

# Get player stats
player_stats, player_id, team_name, points, rebounds, assists, turnovers, blocks, steals, free_throws_made, points_rebounds, points_assists, points_rebounds_assists = get_player_stats(player_name)

try:
    # Print player stats
    print("Player ID: " + str(player_id))
    print("Team: " + team_name)
    print("Points per game: " + str(points))
    print("Rebounds per game: " + str(rebounds))
    print("Assists per game: " + str(assists))
    print("Turnovers per game: " + str(turnovers))
    print("Blocks per game: " + str(blocks))
    print("Steals per game: " + str(steals))
    print("Free throws made per game: " + str(free_throws_made))
    print("Points + rebounds per game: " + str(points_rebounds))
    print("Points + assists per game: " + str(points_assists))
    print("Points + rebounds + assists per game: " + str(points_rebounds_assists))
except:
    print("Player not found.")
