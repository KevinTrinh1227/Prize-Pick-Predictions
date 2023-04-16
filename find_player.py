import requests
import json


def get_player_stats(player_name):
    # API endpoint for player search
    player_search_url = "https://www.balldontlie.io/api/v1/players?search=" + player_name

    response = requests.get(player_search_url)
    player_data = json.loads(response.text)
    fp_player_id = player_data['data'][0]['id']
    #team_id = player_data['data'][0]['team']['id']
    fp_team_name = player_data['data'][0]['team']['full_name']

    # API endpoint for player stats
    player_stats_url = "https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]=" + str(fp_player_id)

    # Retrieve player stats
    response = requests.get(player_stats_url)
    player_stats = json.loads(response.text)['data'][0]

    # Get turnovers, blocks, steals, free throws made, points+rebounds, points+assists, points+rebounds+assists per game,
    # defaulting to "--" if not available
    fp_turnovers = player_stats.get('turnover', "--")
    fp_blocks = player_stats.get('blk', "--")
    fp_steals = player_stats.get('stl', "--")
    fp_ftm = player_stats.get('ftm', "--")
    fp_points = player_stats.get('pts', "--")
    fp_rebounds = player_stats.get('reb', "--")
    fp_assists = player_stats.get('ast', "--")

    # Get points + rebounds, points + assists, and points + rebounds + assists, defaulting to "--" if not available
    fp_points_rebounds = fp_points + fp_rebounds if (fp_points != "--" and fp_rebounds != "--") else "--"
    fp_points_assists = fp_points + fp_assists if (fp_points != "--" and fp_assists != "--") else "--"
    fp_points_rebounds_assists = fp_points + fp_rebounds + fp_assists if (
    fp_points != "--" and fp_rebounds != "--" and fp_assists != "--") else "--"

    # Return player stats, ID, team name, points, rebounds, assists, turnovers, blocks, steals, and free throws made
    return player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_turnovers, fp_blocks, fp_steals, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists
