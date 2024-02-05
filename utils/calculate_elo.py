import json
import math

def probability(rating1, rating2):
    return 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def elo_rating(rating_a, rating_b, k, d):
    pa = probability(rating_b + 100, rating_a) if d == 1 else probability(rating_b + 100, rating_a)
    pb = probability(rating_a, rating_b + 100) if d == 1 else probability(rating_a, rating_b + 100)

    rating_a = rating_a + k * (1 - pa) if d == 1 else rating_a + k * (0 - pa)
    rating_b = rating_b + k * (0 - pb) if d == 1 else rating_b + k * (1 - pb)

    return rating_a, rating_b

def update_elo(match, team_elos):
    home_team_id = match["home_team"]["id"]
    visitor_team_id = match["visitor_team"]["id"]

    home_team_elo, home_team_wins, home_team_losses, home_team_name, home_team_city, home_team_history = team_elos.get(home_team_id, (1500, 0, 0, match["home_team"]["name"], match["home_team"]["city"], []))
    visitor_team_elo, visitor_team_wins, visitor_team_losses, visitor_team_name, visitor_team_city, visitor_team_history = team_elos.get(visitor_team_id, (1500, 0, 0, match["visitor_team"]["name"], match["visitor_team"]["city"], []))

    result = 1 if match["home_team_score"] > match["visitor_team_score"] else 0  # 1 for home team win, 0 otherwise

    home_team_elo, visitor_team_elo = elo_rating(home_team_elo, visitor_team_elo, 20, result)

    home_team_wins += result
    home_team_losses += 1 - result
    visitor_team_wins += 1 - result
    visitor_team_losses += result

    home_team_history.append({
        "match_id": match["id"],
        "date": match["date"],
        "elo": home_team_elo,
        "result": "Win" if result == 1 else "Loss",
        "opposing_team": visitor_team_name,
        "scores": {"winner_score": match["home_team_score"], "losser_score": match["visitor_team_score"]}
    })

    visitor_team_history.append({
        "match_id": match["id"],
        "date": match["date"],
        "elo": visitor_team_elo,
        "result": "Win" if result == 0 else "Loss",
        "opposing_team": home_team_name,
        "scores": {"winner_score": match["visitor_team_score"], "losser_score": match["home_team_score"]}
    })

    team_elos[home_team_id] = (home_team_elo, home_team_wins, home_team_losses, home_team_name, home_team_city, home_team_history)
    team_elos[visitor_team_id] = (visitor_team_elo, visitor_team_wins, visitor_team_losses, visitor_team_name, visitor_team_city, visitor_team_history)

    return team_elos

def sort_teams_by_elo(team_stats):
    sorted_teams = sorted(team_stats.items(), key=lambda x: x[1]["elo"], reverse=True)
    return dict(sorted_teams)

def print_team_stats(team_stats):
    print("{:<5} {:<35} {:<15} {:<8} {:<8} {:<15} {:<10}".format("Idx", "Team", "Elo", "Wins", "Losses", "Total Games", "Win Rate"))
    print("="*105)
    for index, (team_id, stats) in enumerate(team_stats.items(), 1):
        print("{:<5} {:<35} {:<15.2f} {:<8} {:<8} {:<15} {:<.2f}%".format(
            index,
            f"{stats['city']} {stats['team_name']}", 
            stats['elo'], 
            stats['wins'], 
            stats['losses'], 
            stats['total_games'], 
            stats['win_rate']
        ))

def sort_and_print(elo_json):
    # Example usage:
    with open(elo_json, "r") as file:
        team_stats = json.load(file)

    sorted_teams = sort_teams_by_elo(team_stats)
    print_team_stats(sorted_teams)

def start_calculating(read_file, write_file):
    with open(read_file, "r") as file:
        matches = json.load(file)

    team_elos = {}

    for match in matches:
        team_elos = update_elo(match, team_elos)

    team_stats = {
        team_id: {"elo": elo, "wins": wins, "losses": losses, "total_games": wins + losses, "win_rate": wins / (wins + losses) * 100,
                  "team_name": team_name, "city": city, "match_history": history}
        for team_id, (elo, wins, losses, team_name, city, history) in team_elos.items()
    }

    with open(write_file, "w") as file:
        json.dump(team_stats, file, indent=2)
        
    print("[🟢] Successfully calculated and saved all NBA team ELOs to respective json file.")
    
    return None

if __name__ == "__main__":
    start_calculating()
