"""
    Project name: Prize Pick Predictions
    Author: Kevin Huy Trinh
    Date created: March 2022
    Python Version: 3.11.1
    Dependencies: Requirement.txt
    Description: Python program that makes recommendations on
        betting in favor/against a player's prize pick line_score
        value using a linear regression machine learning algorithm
        that takes into account the opposing team's elo, and the
        desired player's current seasonal score in diff stat types.

    api link --> https://api.prizepicks.com/projections?league_id=7
"""

import time
from utils.json_parser import *
from utils.bet_recommendation import *
from utils.current_player_stats import *
import requests
# from utils.team_finder import *
from utils.calculate_elo import *
from utils.get_all_matches import *
from utils.json_functions import *

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

json_dir_location = "json files"
pre_json = "json files/pre_formatted_projections.json"                      # where we copied and paste api into
post_json = "json files/post_formatted_projections.json"                    # organized json file
points_json = "json files/points.json"                                      # player points recommendations json
assists_json = "json files/assists.json"                                    # player assists recommendations json
rebounds_json = "json files/rebounds.json"                                  # player rebounds recommendations json
points_assists_json = "json files/points_assists.json"                      # player pts+asts recommendations json
points_rebounds_json = "json files/points_rebounds.json"                    # player pts+rebs recommendations json
points_assists_rebounds_json = "json files/points_assists_rebounds.json"    # player pts+asts+rebs recommendations json
season_matches_json = "json files/match_results.json"                       # displays the season's match results
team_elos_json = "json files/team_elos.json"                                # All 30 NBA team's elo ratings and history

wipe_json_files(json_dir_location)                                          # we clean all json files for new data only

print("""
______      _         _____ _      _    _____              _ _      _   _                 
|  __ \    (_)       |  __ (_)    | |  |  __ \            | (_)    | | (_)                
| |__) | __ _ _______| |__) |  ___| | _| |__) | __ ___  __| |_  ___| |_ _  ___  _ __  ___ 
|  ___/ '__| |_  / _ \  ___/ |/ __| |/ /  ___/ '__/ _ \/ _` | |/ __| __| |/ _ \| '_ \/ __|
| |   | |  | |/ /  __/ |   | | (__|   <| |   | | |  __/ (_| | | (__| |_| | (_) | | | \__ |
|_|   |_|  |_/___\___|_|   |_|\___|_|\_\_|   |_|  \___|\__,_|_|\___|\__|_|\___/|_| |_|___/\n""")

""" =============================================
Because PP does not allow public API, this is a work around
that uses a webdriver to access the PP end point to scrape the data

IMPORTANT: This method uses Firefox and requires a Gecko Driver
Download the correct version here: https://github.com/mozilla/geckodriver/releases
================================================= """

current_season_year = 2023      # 2023 means 2023-24 NBA season (Change if needed)

get_all_matches(season_matches_json, current_season_year)       # params (read file, current season yyyy)
start_calculating(season_matches_json, team_elos_json)          # params(read file, write file)
sort_and_print(team_elos_json)                                  # will sort and print out elo table

# you can change this out if you want to use a different driver/browser combo
# information about driver and browser in README.md
gecko_path = "./drivers/geckodriver.exe"
service = Service(gecko_path)
driver = webdriver.Firefox()


url = 'https://api.prizepicks.com/projections?league_id=7'
driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Find the 'div' tag with ID "json"
json_div = soup.find('div', {'id': 'json'})

# Check if 'json_div' is not None before saving its content to a JSON file
if json_div:
    
    json_content = json_div.get_text(strip=True, separator='\n')

    try:
        # Try to parse the extracted content as JSON
        json_data = json.loads(json_content)

        
        filename = pre_json

        
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=2)

        print(f"[🟢] Successfully pulled and saved Prize Pick data to {filename}\n")
    except json.JSONDecodeError:
        print("[🔴]Invalid JSON content.")
else:
    print("[🔴] No 'div' tag with ID 'json' found on the page.")

driver.quit()

""" =============================================
* Here we call parse/clean our json file and extract
* only relevant information that we need using the
* parse_json_file() and assigning the data var to it
============================================= """
data = parse_json_file(pre_json, post_json)
num_players = len(data)                         # number of players we collected from parsing
players_printed = 0                             # total # of players we were able to collect
table = []                                      # table were printing out
n_a = "--"                                      # default value if a stat is NULL

# Each stat type is going to be separated into its own json file
default_data = []

# Open or create each JSON file and initialize data
points_data = open_or_create_json(points_json, default_data)
assists_data = open_or_create_json(assists_json, default_data)
rebounds_data = open_or_create_json(rebounds_json, default_data)
points_assists_data = open_or_create_json(points_assists_json, default_data)
points_rebounds_data = open_or_create_json(points_rebounds_json, default_data)
points_assists_rebounds_data = open_or_create_json(points_assists_rebounds_json, default_data)

""" =============================================
* Looping through each player inside our new
* parsed and cleaned up json file
============================================= """
for idx, key in enumerate(data):
    # the attribute values
    name = data[key]['name']
    team_name = data[key]['attributes']['team_name']
    team_city_state = data[key]['attributes']['market']
    photo_link = data[key]['attributes']['image_url']
    player_position = data[key]['attributes']['position']

    # initialize values to "--" which is N/A
    points = n_a
    rebounds = n_a
    assists = n_a
    turnovers = n_a
    points_assists = n_a
    points_rebounds = n_a
    points_rebounds_assists = n_a

    # check if player has stat_type and update value accordingly
    for item in data[key]['strike_values']:
        if item['stat_type'] == 'Points':
            points = item['line_score']
        elif item['stat_type'] == 'Turnovers':
            turnovers = item['line_score']
        elif item['stat_type'] == 'Rebounds':
            rebounds = item['line_score']
        elif item['stat_type'] == 'Assists':
            assists = item['line_score']
        elif item['stat_type'] == 'Pts+Asts':
            points_assists = item['line_score']
        elif item['stat_type'] == 'Pts+Rebs':
            points_rebounds = item['line_score']
        elif item['stat_type'] == 'Pts+Rebs+Asts':
            points_rebounds_assists = item['line_score']

    try:
        player_name = name
        num_attempts = 1

        min_attempts, max_attempts = 1, 2+1     # 5 attempts to get online player data
        for i in range(min_attempts, max_attempts):
            num_attempts = i
            try:
                fp_player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists = get_player_stats(
            player_name, current_season_year)

                # making the recommendations on points
                recommendation_pts = predict(points, fp_points, n_a)
                recommendation_reb = predict(rebounds, fp_rebounds, n_a)
                recommendation_ast = predict(assists, fp_assists, n_a)

                # find the combined stats
                recommendation_pts_ast = predict(points_assists, fp_points + fp_assists, n_a)
                recommendation_pts_reb = predict(points_rebounds, fp_points + fp_assists, n_a)
                recommendation_pts_ast_reb = predict(points_rebounds_assists, fp_points + fp_assists + fp_rebounds, n_a)

                table.append(
                    [idx + 1, name, team_name, points, fp_points, recommendation_pts, rebounds, fp_rebounds,
                     recommendation_reb,
                     assists, fp_assists, recommendation_ast, points_assists,
                     points_rebounds, points_rebounds_assists])
                

                """
                =============================================
                * Calculating the absolute value of the differences
                * between the predicted score and line scores for the player
                * so longer distance between the two means more likely to hit
                =============================================
                """
                diff_pts = round(abs(fp_points - points), 5) if isinstance(fp_points, (int, float)) and isinstance(points, (
                int, float)) else n_a
                diff_reb = round(abs(fp_rebounds - rebounds), 5) if isinstance(fp_rebounds, (int, float)) and isinstance(rebounds,
                                                                                                            (
                                                                                                                int,
                                                                                                                float)) else n_a
                diff_assists = round(abs(fp_assists - assists), 5) if isinstance(fp_assists, (int, float)) and isinstance(assists,
                                                                                                                    (
                                                                                                                        int,
                                                                                                                        float)) else n_a
                diff_pts_ast = round(abs((fp_points + fp_assists) - points_assists), 5) if isinstance(fp_points,
                                                                                                        (
                                                                                                        int, float)) and isinstance(
                    fp_assists, (int, float)) and isinstance(points_assists, (int, float)) else n_a
                diff_pts_reb = round(abs((fp_points + fp_rebounds) - points_rebounds), 5) if isinstance(fp_points,
                                                                                                        (int,
                                                                                                        float)) and isinstance(
                    fp_rebounds, (int, float)) and isinstance(points_rebounds, (int, float)) else n_a
                diff_pts_ast_reb = round(abs((fp_points + fp_assists + fp_rebounds) - points_rebounds_assists), 5) if isinstance(
                    fp_points, (int, float)) and isinstance(fp_assists, (int, float)) and isinstance(fp_rebounds, (
                    int, float)) and isinstance(points_rebounds_assists, (int, float)) else n_a


                """ =============================================
                * Here we append the values and split them into
                * their own json files for the flask app.py;
                * if they are missing a value we do NOT append.
                ============================================= """
                # Appending points json
                if recommendation_pts != n_a:
                    points_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "points",
                                "strike_value": points,
                                "predicted_value": fp_points,
                                "bet_recommendation": recommendation_pts,
                                "difference": diff_pts
                            }
                        }
                    })

                # Appending assists json
                if recommendation_ast != n_a:
                    assists_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "assists",
                                "strike_value": assists,
                                "predicted_value": fp_assists,
                                "bet_recommendation": recommendation_ast,
                                "difference": diff_assists
                            }
                        }
                    })

                # Appending assists json
                if recommendation_reb != n_a:
                    rebounds_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "rebounds",
                                "strike_value": rebounds,
                                "predicted_value": fp_rebounds,
                                "bet_recommendation": recommendation_reb,
                                "difference": diff_reb
                            }
                        }
                    })

                # Appending points + assists json
                if recommendation_pts_ast != n_a:
                    points_assists_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+ast",
                                "strike_value": points_assists,
                                "predicted_value": fp_points + fp_assists,
                                "bet_recommendation": recommendation_pts_ast,
                                "difference": diff_pts_ast
                            }
                        }
                    })

                # Appending points + rebounds json
                if recommendation_pts_reb != n_a:
                    points_rebounds_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+rebs",
                                "strike_value": points_rebounds,
                                "predicted_value": fp_points + fp_rebounds,
                                "bet_recommendation": recommendation_pts_reb,
                                "difference": diff_pts_reb
                            }
                        }
                    })

                # Appending points + assists + rebounds json
                if recommendation_pts_ast_reb != n_a:
                    points_assists_rebounds_data.append({
                        player_name: {
                            "general": {
                                "player_id": fp_player_id,
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+rebs+asts",
                                "strike_value": points_rebounds_assists,
                                "predicted_value": fp_points + fp_assists + fp_rebounds,
                                "bet_recommendation": recommendation_pts_ast_reb,
                                "difference": diff_pts_ast_reb
                            }
                        }
                    })

                break
            except:
                if i < max_attempts - 1:
                    load_status = "FAILED"
                    start_str = f"[🟡] Load Status: {load_status:<15} Player: {player_name:<25}"
                    print(
                        f"{start_str:<60} Attempts: {num_attempts}/{(max_attempts - 1):<5} ({n_a:0>2}/{n_a} | {n_a}%) \t[In: {i} sec(s)]")
                    time.sleep(i)
                else:
                    load_status = "FAILED"
                    start_str = f"[🟡] Load Status: {load_status:<15} Player: {player_name:<25}"
                    print(
                        f"{start_str:<60} Attempts: {num_attempts}/{(max_attempts - 1):<5} ({n_a:0>2}/{n_a} | {n_a}%) \t[Final attempt]")

        """ =============================================
        * Writing the data into the json file with an indent
        * of 2 for each stat type for every player
        ============================================= """
        with open(points_json, 'w') as f_points:
            json.dump(points_data, f_points, indent=2)

        with open(assists_json, 'w') as f_assists:
            json.dump(assists_data, f_assists, indent=2)

        with open(rebounds_json, 'w') as f_rebounds:
            json.dump(rebounds_data, f_rebounds, indent=2)

        with open(points_assists_json, 'w') as f_points_assists:
            json.dump(points_assists_data, f_points_assists, indent=2)

        with open(points_rebounds_json, 'w') as f_points_rebounds:
            json.dump(points_rebounds_data, f_points_rebounds, indent=2)

        with open(points_assists_rebounds_json, 'w') as f_points_assists_rebounds:
            json.dump(points_assists_rebounds_data, f_points_assists_rebounds, indent=2)

        players_printed += 1
        load_status = "Successful"
        start_str = f"[🟢] Load Status: {load_status:<15} Player: {player_name:<25}"
        players_percentage = round((players_printed / num_players) * 100)
        print(f"{start_str:<60} Attempts: {num_attempts}/{(max_attempts - 1):<5} ({players_printed:0>2}/{num_players} | {players_percentage:0>2}%)")

    except Exception as e:
        """ =============================================
        * runs if we failed to get the player's actual season
        * average on the ball don't lie api. (so we skip player)
        ============================================= """
        player_name = name
        print(f"[🔴] Failed data loaded for: {player_name}. Exception: {e}. Skipping.")

    time.sleep(1.25)                           # help avoid being rate limited (60 req per min)


# number of players with at least 1 missing stat type
num_na_stats = sum(1 for row in table if n_a in row)
print(f"\n{num_na_stats} players have at least one missing stat.")
print(f"A total of {num_players} player objects in json file.")
print(f"{players_printed}/{num_players} were printed out in table format.\n\n")





""" =============================================
* Flask application python file that displays
* the json files from the "./json files/*.json"
============================================= """

from flask import Flask, render_template, request
import json

app = Flask(__name__)

# points.json is default when loading up
with open('json files/points.json') as f:
    data = json.load(f)

# Route for the home page
@app.route('/')
def index():

    """ =============================================
    * Check if a data source parameter was passed in the URL
    * This allows the user to switch between json files
    * to view the recommendations for different stat types
    ============================================= """
    data_source = request.args.get('data_source', 'points')
    if data_source == 'points':
        with open('json files/points.json') as f:
            data = json.load(f)
    elif data_source == 'rebounds':
        with open('json files/rebounds.json') as f:
            data = json.load(f)
    elif data_source == 'assists':
        with open('json files/assists.json') as f:
            data = json.load(f)
    elif data_source == 'pts_asts':
        with open('json files/points_assists.json') as f:
            data = json.load(f)
    elif data_source == 'pts_rebs':
        with open('json files/points_rebounds.json') as f:
            data = json.load(f)
    elif data_source == 'pts_rebs_asts':
        with open('json files/points_assists_rebounds.json') as f:
            data = json.load(f)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
