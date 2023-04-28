""" =============================================
* finds the nba team given the abbreviation and
* calculates the team's elo.
============================================= """

import requests

def get_nba_team_info(team_abbr):
    base_url = 'https://www.balldontlie.io/api/v1/'
    team_url = f'teams?abbreviation={team_abbr.upper()}'
    response = requests.get(base_url + team_url)

    if response.status_code == 200:
        team_data = response.json()['data'][0]
        team_name = team_data['full_name']
        team_city = team_data['city']
        team_id = team_data['id']
        return f'Team Name: {team_name}, City: {team_city}, ID: {team_id}'
    else:
        return f'Error {response.status_code}: Could not retrieve data'