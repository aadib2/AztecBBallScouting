import requests
from bs4 import BeautifulSoup

def format_player_name(name):
   
    parts = name.lower().split()
    formatted = '-'.join(parts) + "-1"
    return formatted

def scrape_player_data(player):
    player_slug = format_player_name(player)
    url = f"https://www.sports-reference.com/cbb/players/{player_slug}.html"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Could not find player page for {player}"}

    soup = BeautifulSoup(response.text, "html.parser")
    stats_table = soup.find("table", {"id": "players_per_game"})

    if not stats_table:
        return {"error": f"No stats table found for {player}"}

    last_row = stats_table.find("tfoot").find("tr")

    stat_fields = {
        "PTS": "pts_per_g",
        "AST": "ast_per_g",
        "REB": "trb_per_g",
        "FG%": "fg_pct",
        "3P%": "fg3_pct",
        "Total Points": "pts"  # Add key for total points
    }

    stats = {}
    for label, key in stat_fields.items():
        cell = last_row.find("td", {"data-stat": key})
        stats[label] = cell.text if cell else "N/A"

    return stats

#               TODO
# test_scrape is meant to be dynamic for players and be able to retreieve more data than
# scrape_player_data, but keeps returning:
#
# .\AztecBBallScouting\app\scraper.py", line 57, in test_scrape
#   raise ValueError("No per-game stats table found.")

def test_scrape(player):
    player_slug = format_player_name(player)
    url = f"https://www.sports-reference.com/cbb/players/{player_slug}.html"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Player not found or URL failed: {url}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    per_game_table = soup.find("table,", {"id": "players_per_game"})
    
    if not per_game_table:
        raise ValueError("No per-game stats table found.")
    
    footer_row = per_game_table.find("tfoot").find("tr")
    if not footer_row:
        raise ValueError("No footer row in per-game table.")
    
    fields = {
        "g": "Games Played",
        "gs": "Games Started",
        "mp": "Minutes Per Game",
        "fg": "Field Goals Per Game",
        "fga": "Field Goal Attempts",
        "fg_pct": "FG%",
        "fg3": "3PT Makes",
        "fg3a": "3PT Attempts",
        "fg3_pct": "3PT%",
        "ft": "FT Makes",
        "fta": "FT Attempts",
        "ft_pct": "FT%",
        "orb": "Offensive Rebounds",
        "drb": "Defensive Rebounds",
        "trb": "Total Rebounds",
        "ast": "Assists",
        "stl": "Steals",
        "blk": "Blocks",
        "tov": "Turnovers",
        "pf": "Personal Fouls",
        "pts": "Points"
    }
    
    results = {}
    
    for stat_code, label in fields.items():
        td = footer_row.find("td", {"data-stat": stat_code})
        results[label] = td.text.strip() if td else "N/A"
        
    return results
    