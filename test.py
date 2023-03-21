import requests
import json

# Define function to retrieve player stats
def get_player_stats(player_name):
    # API endpoint for player search
    player_search_url = "https://www.balldontlie.io/api/v1/players?search=" + player_name

    # Retrieve player ID
    response = requests.get(player_search_url)
    player_data = json.loads(response.text)
    player_id = player_data['data'][0]['id']

    # API endpoint for player stats
    player_stats_url = "https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]=" + str(player_id)

    # Retrieve player stats
    response = requests.get(player_stats_url)
    player_stats = json.loads(response.text)['data'][0]

    # Return player stats
    return player_stats

# Get player name from user input
player_name = input("Enter player name: ")

# Get player stats
player_stats = get_player_stats(player_name)

# Print player stats
print("Points per game: " + str(player_stats['pts']))
print("Rebounds per game: " + str(player_stats['reb']))
print("Assists per game: " + str(player_stats['ast']))
