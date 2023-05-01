import requests
import csv

# Function to fetch player data from API
def fetch_player_data(player_name):
    url = f'https://www.balldontlie.io/api/v1/stats?seasons[]=2021&per_page=100&search={player_name}'
    response = requests.get(url)

    if response.status_code == 200:
        player_data = response.json()
        return player_data['data']
    else:
        print(f"Failed to fetch data for {player_name}")
        return None

# Function to calculate opponent strength based on ELO
def calculate_elo_strength(team_id):
    # Implementation of ELO calculation goes here
    # For now, let's just return a random value between 0 and 1
    import random
    return random.uniform(0, 1)

# Function to generate CSV file
def generate_csv(player_name):
    # Fetch player data
    player_data = fetch_player_data(player_name)

    # If player data is not available, return None
    if player_data is None:
        return None

    # Open CSV file for writing
    with open('player_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header row if file is empty
        if file.tell() == 0:
            writer.writerow(['player_name', 'game_date', 'team_id', 'opponent_team_id', 'opponent_strength', 'points', 'assists', 'rebounds'])

        # Write data rows for past 10 games
        for i in range(10):
            game = player_data[i]

            game_date = game['game']['date']
            team_id = game['team']['id']
            opponent_team_id = game['opponent']['id']
            opponent_strength = calculate_elo_strength(opponent_team_id)
            points = game['pts']
            assists = game['ast']
            rebounds = game['reb']

            row = [player_name, game_date, team_id, opponent_team_id, opponent_strength, points, assists, rebounds]
            writer.writerow(row)

            # Print out the data that was added to the CSV file
            print(row)

# Get input from user
player_name = input("Enter player name: ")

# Generate CSV file
generate_csv(player_name)
