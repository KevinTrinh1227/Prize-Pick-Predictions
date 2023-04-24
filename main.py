"""
    Project name: Prize Pick Predictions
    Author: Kevin Huy Trinh
    Date created: March 2022
    Python Version: 3.11.1
    Description: Linear regression python program that makes
        recommendations on betting in favor/against a player's prize
        pick line_score value using numerous machine learning algorithms. 
"""

# api link --> https://api.prizepicks.com/projections?league_id=7

import json
from tabulate import tabulate
from find_player import get_player_stats
from recommendation import predict
import time

pre_json = "json files/pre_formatted_projections.json"          # where we copied and paste api into
post_json = "json files/post_formatted_projections.json"        # after it gets cleaned up & formatted/organized
points_json = "json files/points.json"                          # player points recommendations json
assists_json = "json files/assists.json"                        # player assists recommendations json
rebounds_json = "json files/rebounds.json"                      # player rebounds recommendations json
points_assists_json = "json files/points_assists.json"
points_rebounds_json = "json files/points_rebounds.json"
points_assists_rebounds_json = "json files/points_assists_rebounds.json"

# reads the pre_formmatted json file
with open(pre_json, "r") as file:
    data = json.load(file)
    # Format the JSON with indentation
    json_str = json.dumps(data, indent=4)

# pre_formmatted json --> post_formatted json
json_dict = json.loads(json_str)
with open(pre_json, "w") as file:
    json.dump(json_dict, file, indent=4)

# Create dictionary to store results
results = {}

# Loop through included data to get player names and IDs
for item in data['included']:
    if item['type'] == 'new_player':
        player_id = item['id']
        player_name = item['attributes']['name']
        results[player_id] = {
            'name': player_name,
            'strike_values': []
        }

# Loop through projection data and match player IDs to add stat_type and line_score
for projection in data['data']:
    if projection['type'] == 'projection':
        player_id = projection['relationships']['new_player']['data']['id']
        stat_type = projection['attributes']['stat_type']
        line_score = projection['attributes']['line_score']
        results[player_id]['strike_values'].append({
            'stat_type': stat_type,
            'line_score': line_score
        })
        # Add player attributes to results dictionary
        for player in data['included']:
            if player['type'] == 'new_player' and player['id'] == player_id:
                results[player_id]['attributes'] = player['attributes']

# Write results to JSON file
with open(post_json, 'w') as f:
    json.dump(results, f, indent=2)
with open(post_json, 'r') as f:
    data = json.load(f)

# lengths and member counts
num_players = len(data)
players_printed = 0

table = []  # table were printing out
n_a = "--"

# this is where each stat type gets saved into its own json file
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
        fp_player_stats, fp_player_id, fp_team_name, fp_points, fp_rebounds, fp_assists, fp_ftm, fp_points_rebounds, fp_points_assists, fp_points_rebounds_assists = get_player_stats(
            player_name)

        # making the recommendations on points
        recommendation_pts = predict(points, fp_points, n_a)
        recommendation_reb = predict(rebounds, fp_rebounds, n_a)
        recommendation_ast = predict(assists, fp_assists, n_a)

        # findind the combined stats
        recommendation_pts_ast = predict(points_assists, fp_points + fp_assists, n_a)
        recommendation_pts_reb = predict(points_rebounds, fp_points + fp_assists, n_a)
        recommendation_pts_ast_reb = predict(points_rebounds_assists, fp_points + fp_assists + fp_rebounds, n_a)

        table.append(
            [idx + 1, name, team_name, points, fp_points, recommendation_pts, rebounds, fp_rebounds, recommendation_reb,
             assists, fp_assists, recommendation_ast, points_assists,
             points_rebounds, points_rebounds_assists])


        # =================================================
        # Calculating the absolute difference values
        # between the actual and line_scores for the player
        # =================================================
        diff_pts = abs(fp_points - points) if isinstance(fp_points, (int, float)) and isinstance(points, (int, float)) else n_a
        diff_reb = abs(fp_rebounds - rebounds) if isinstance(fp_rebounds, (int, float)) and isinstance(rebounds, (
            int, float)) else n_a
        diff_assists = abs(fp_assists - assists) if isinstance(fp_assists, (int, float)) and isinstance(assists, (
            int, float)) else n_a
        diff_pts_ast = abs((fp_points + fp_assists) - points_assists) if isinstance(fp_points,
                                                                                      (int, float)) and isinstance(
            fp_assists, (int, float)) and isinstance(points_assists, (int, float)) else n_a
        diff_pts_reb = abs((fp_points + fp_rebounds) - points_rebounds) if isinstance(fp_points,
                                                                                      (int, float)) and isinstance(
            fp_rebounds, (int, float)) and isinstance(points_rebounds, (int, float)) else n_a
        diff_pts_ast_reb = abs((fp_points + fp_assists + fp_rebounds) - points_rebounds_assists) if isinstance(
            fp_points, (int, float)) and isinstance(fp_assists, (int, float)) and isinstance(fp_rebounds, (
            int, float)) and isinstance(points_rebounds_assists, (int, float)) else n_a



        # =================================================
        # Here we append the values and split them into
        # their own json files for the flask app.py;
        # if they are missing a value we do NOT append.
        # =================================================

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

        # =================================================
        # Writing the data into the json file with an indent
        # of 2 for each player of that stat type
        # =================================================

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




    # =================================================
    # runs if we failed to get the player's actual season
    # average on the ball don't lie api. (so we skip player)
    # =================================================
    except Exception as e:
        player_name = name
        print(f"Failed to find {player_name}. Exception: {e}. Now skipping.")

    players_printed += 1
    time.sleep(2)  # to avoid being rate limited
    print(
        f"{players_printed}/{num_players} players have been loaded. ({round((players_printed / num_players) * 100)}%)")

# number of players with atleast 1 missing stat
num_na_stats = sum(1 for row in table if n_a in row)

print(tabulate(table,
               headers=['##', 'Name', 'Team Name', 'Pts', "FP-Pts", "Bet Rec.", "Rebs", "FP_reb", "Bet Rec.", "Ast",
                        "FP-Ast", "Bet Rec.", "Pts+Ast", "Pts+Rebs",
                        "Pts+Rebs+Ast"], tablefmt='orgtbl') + "\n")

print(f"\n{num_na_stats} players have at least one missing stat.")
print(f"A total of {num_players} player objects in json file.")
print(f"{players_printed}/{num_players} were printed out in table format.\n\n")
