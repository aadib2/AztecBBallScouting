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