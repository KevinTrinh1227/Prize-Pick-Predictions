import requests
import json

def get_player_stats(player_name):
    # API endpoint for player search
    player_search_url = "https://www.balldontlie.io/api/v1/players?search=" + player_name

    # Retrieve player ID and team ID
    response = requests.get(player_search_url)
    player_data = json.loads(response.text)
    player_id = player_data['data'][0]['id']
    team_id = player_data['data'][0]['team']['id']

    # API endpoint for team name
    team_url = f"https://www.balldontlie.io/api/v1/teams/{team_id}"
    team_response = requests.get(team_url)
    team_data = json.loads(team_response.text)
    team_name = team_data['full_name']

    # API endpoint for player stats
    player_stats_url = "https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]=" + str(player_id)

    # Retrieve player stats
    response = requests.get(player_stats_url)
    player_stats = json.loads(response.text)['data'][0]

    # Get turnovers, blocks, steals, and free throws made per game, defaulting to "--" if not available
    turnovers = player_stats.get('turnover', "--")
    blocks = player_stats.get('blk', "--")
    steals = player_stats.get('stl', "--")
    free_throws_made = player_stats.get('ftm', "--")

    # Return player stats, ID, team name, turnovers, blocks, steals, and free throws made
    return player_stats, player_id, team_name, turnovers, blocks, steals, free_throws_made

