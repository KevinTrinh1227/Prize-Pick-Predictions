""" =============================================
* Uses theballdontlie api and searches for a specific
* player's current stats in different stat types.
============================================= """

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

    fp_ftm = player_stats.get('ftm', "--")
    fp_points = player_stats.get('pts', "--")
    fp_rebounds = player_stats.get('reb', "--")
    fp_assists = player_stats.get('ast', "--")

    # Get points + rebounds, points + assists, and points + rebounds + assists, defaulting to "--" if not available
    fp_points_rebounds = fp_points + fp_rebounds if (fp_points != "--" and fp_rebounds != "--") else "--"
    fp_points_assists = fp_points + fp_assists if (fp_points != "--" and fp_assists != "--") else "--"
    fp_points_rebounds_assists = fp_points + fp_rebounds + fp_assists if (
    fp_points != "--" and fp_rebounds != "--" and fp_assists != "--") else "--"

    # Return player stats that we need
    return player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists