"""
=============================================
* Uses theballdontlie api and searches for a specific
* player's current stats in different stat types.
=============================================
"""

import json
import requests

def get_player_stats(player_name):

    # API endpoint for player search
    player_search_url = "https://www.balldontlie.io/api/v1/players?search=" + player_name

    response = requests.get(player_search_url)
    player_data = json.loads(response.text)
    fp_player_id = player_data['data'][0]['id']
    fp_team_name = player_data['data'][0]['team']['full_name']

    # API endpoint for player stats
    player_stats_url = "https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]=" + str(fp_player_id)

    # Retrieve player stats
    response = requests.get(player_stats_url)
    player_stats = json.loads(response.text)['data'][0]

    fp_ftm = round(player_stats.get('ftm', "--"), 5)
    fp_points = round(player_stats.get('pts', "--"), 5)
    fp_rebounds = round(player_stats.get('reb', "--"), 5)
    fp_assists = round(player_stats.get('ast', "--"), 5)

    # Get points + rebounds, points + assists, and points + rebounds + assists, defaulting to "--" if not available
    fp_points_rebounds = round(fp_points + fp_rebounds, 5) if (fp_points != "--" and fp_rebounds != "--") else "--"
    fp_points_assists = round(fp_points + fp_assists, 5) if (fp_points != "--" and fp_assists != "--") else "--"
    fp_points_rebounds_assists = round(fp_points + fp_rebounds + fp_assists, 5) if (
    fp_points != "--" and fp_rebounds != "--" and fp_assists != "--") else "--"

    # Return player stats that we need
    return player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists
