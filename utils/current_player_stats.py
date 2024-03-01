"""
=============================================
* Uses theballdontlie api and searches for a specific
* player's current stats in different stat types.
=============================================
"""
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

api_key = os.getenv("THE_BALL_DONT_LIEAPI_KEY")

def get_player_stats(full_name, current_season_year):

    # Split the input string into words
    name_array = full_name.split()

    # Extract first name and last name
    first_name = name_array[0]
    last_name = name_array[-1]

    url = f"https://api.balldontlie.io/v1/players?first_name={first_name}&?last_name={last_name}"
    headers = {"Authorization": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        player = data["data"][0]
        #print(f"First Name: {player['first_name']}")
        #print(f"Last Name: {player['last_name']}")
        #print(f"Player ID: {player['id']}")
        
        fp_player_id = player['id']
        fp_team_name = player['team']['full_name']
        
        player_url = f"https://api.balldontlie.io/v1/season_averages?season={current_season_year}&player_ids[]={player['id']}"
        player_response = requests.get(player_url, headers=headers)
        player_stats = player_response.json()["data"][0]
        #print(player_stats)
        
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
        #print("========================================================")
        #print(player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists)
        return player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists
    else:
        return None, "Error occurred while fetching player information."
