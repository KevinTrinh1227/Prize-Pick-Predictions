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
# from utils.team_finder import *

pre_json = "json files/pre_formatted_projections.json"                      # where we copied and paste api into
post_json = "json files/post_formatted_projections.json"                    # organized json file
points_json = "json files/points.json"                                      # player points recommendations json
assists_json = "json files/assists.json"                                    # player assists recommendations json
rebounds_json = "json files/rebounds.json"                                  # player rebounds recommendations json
points_assists_json = "json files/points_assists.json"                      # player pts+asts recommendations json
points_rebounds_json = "json files/points_rebounds.json"                    # player pts+rebs recommendations json
points_assists_rebounds_json = "json files/points_assists_rebounds.json"    # player pts+asts+rebs recommendations json


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
with open(points_json, 'r') as f_points:
    points_data = []
with open(assists_json, 'r') as f_assists:
    assists_data = []
with open(rebounds_json, 'r') as f_rebounds:
    rebounds_data = []
with open(points_assists_json, 'r') as f_points_assists:
    points_assists_data = []
with open(points_rebounds_json, 'r') as f_points_rebounds:
    points_rebounds_data = []
with open(points_assists_rebounds_json, 'r') as f_points_assists_rebounds:
    points_assists_rebounds_data = []

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
            player_name)

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

                """ =============================================
                * Calculating the absolute value of the differences
                * between the predicted score and line scores for the player
                * so longer distance between the two means more likely to hit
                ============================================= """
                diff_pts = abs(fp_points - points) if isinstance(fp_points, (int, float)) and isinstance(points, (
                int, float)) else n_a
                diff_reb = abs(fp_rebounds - rebounds) if isinstance(fp_rebounds, (int, float)) and isinstance(rebounds,
                                                                                                               (
                                                                                                                   int,
                                                                                                                   float)) else n_a
                diff_assists = abs(fp_assists - assists) if isinstance(fp_assists, (int, float)) and isinstance(assists,
                                                                                                                (
                                                                                                                    int,
                                                                                                                    float)) else n_a
                diff_pts_ast = abs((fp_points + fp_assists) - points_assists) if isinstance(fp_points,
                                                                                            (
                                                                                            int, float)) and isinstance(
                    fp_assists, (int, float)) and isinstance(points_assists, (int, float)) else n_a
                diff_pts_reb = abs((fp_points + fp_rebounds) - points_rebounds) if isinstance(fp_points,
                                                                                              (int,
                                                                                               float)) and isinstance(
                    fp_rebounds, (int, float)) and isinstance(points_rebounds, (int, float)) else n_a
                diff_pts_ast_reb = abs((fp_points + fp_assists + fp_rebounds) - points_rebounds_assists) if isinstance(
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "points",
                                "strike_value": points,
                                "actual_value": fp_points,
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "assists",
                                "strike_value": assists,
                                "actual_value": fp_assists,
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "rebounds",
                                "strike_value": rebounds,
                                "actual_value": fp_rebounds,
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+ast",
                                "strike_value": points_assists,
                                "actual_value": fp_points + fp_assists,
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+rebs",
                                "strike_value": points_rebounds,
                                "actual_value": fp_points + fp_rebounds,
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
                                "team_name": team_name,
                                "team_market": team_city_state,
                                "picture_link": photo_link,
                                "player_position": player_position
                            },
                            "stats": {
                                "type": "pts+rebs+asts",
                                "strike_value": points_rebounds_assists,
                                "actual_value": fp_points + fp_assists + fp_rebounds,
                                "bet_recommendation": recommendation_pts_ast_reb,
                                "difference": diff_pts_ast_reb
                            }
                        }
                    })

                break
            except:
                if i < max_attempts - 1:
                    load_status = "FAILED"
                    start_str = f"[🟡] Load Status: {load_status:<15} Player name: {player_name:<30}"
                    print(
                        f"{start_str:<60} Attempts taken: {num_attempts}/{(max_attempts - 1):<5} {n_a:0>2}/{n_a:<5} ({n_a}%) \t[In: {i} sec(s)]")
                    time.sleep(i)
                else:
                    load_status = "FAILED"
                    start_str = f"[🟡] Load Status: {load_status:<15} Player name: {player_name:<30}"
                    print(
                        f"{start_str:<60} Attempts taken: {num_attempts}/{(max_attempts - 1):<5} {n_a:0>2}/{n_a:<5} ({n_a}%) \t[Final attempt]")

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
        start_str = f"[🟢] Load Status: {load_status:<15} Player name: {player_name:<30}"
        players_percentage = round((players_printed / num_players) * 100)
        print(f"{start_str:<60} Attempts taken: {num_attempts}/{(max_attempts - 1):<5} {players_printed:0>2}/{num_players:<5} ({players_percentage:0>2}%)")

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
