import requests
from bs4 import BeautifulSoup
import re
import logging
from bs4 import Comment


def format_player_name(name):
    if re.fullmatch(r"[a-z\-]+-\d+", name.lower()):
        return name.lower()
    parts = name.lower().split()
    return '-'.join(parts) + "-1"


def scrape_season_stats(player: str, season: str) -> dict:
    """Scrape stats for a given NCAA player and a specific season (e.g., '2023' for 2022–23)."""
    logger = logging.getLogger("uvicorn.error")
    player_slug = format_player_name(player)
    url = f"https://www.sports-reference.com/cbb/players/{player_slug}.html"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Player not found or URL failed: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find tables in both regular HTML and comments
    tables = {
        'per_game': soup.find("table", {"id": "players_per_game"}),
        'totals': soup.find("table", {"id": "players_totals"})
    }

    # Check comments for hidden tables
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment, "html.parser")
        if not tables['per_game']:
            tables['per_game'] = comment_soup.find("table", {"id": "players_per_game"})
        if not tables['totals']:
            tables['totals'] = comment_soup.find("table", {"id": "players_totals"})

    # Look for season data in both tables
    row_data = None
    for table_type, table in tables.items():
        if not table:
            continue
        row = table.find("tr", {"id": f"players_{table_type}.{season}"})
        if row:
            row_data = row
            break

    if not row_data:
        raise ValueError(f"No stats found for season {season}")

    # Unified field mapping
    key_map = {
        "year_id": "season",
        "team_name_abbr": "team",
        "conf_abbr": "conference",
        "class": "class_year",
        "pos": "position",
        "g": "games_played",
        "gs": "games_started",
        "mp": "minutes_played",
        "fg": "field_goals_made",
        "fga": "field_goal_attempts",
        "fg_pct": "fg_percentage",
        "fg3": "three_pt_made",
        "fg3a": "three_pt_attempts",
        "fg3_pct": "three_pt_percentage",
        "fg2": "two_pt_made",
        "fg2a": "two_pt_attempts",
        "fg2_pct": "two_pt_percentage",
        "efg_pct": "effective_fg_percentage",
        "ft": "free_throws_made",
        "fta": "free_throw_attempts",
        "ft_pct": "free_throw_percentage",
        "orb": "offensive_rebounds",
        "drb": "defensive_rebounds",
        "trb": "total_rebounds",
        "ast": "assists",
        "stl": "steals",
        "blk": "blocks",
        "tov": "turnovers",
        "pf": "personal_fouls",
        "pts": "points",
        "awards": "awards"
    }

    results = {}
    cells = row_data.find_all(["td", "th"])
    for cell in cells:
        raw_key = cell.get("data-stat")
        mapped_key = key_map.get(raw_key, raw_key)
        val = cell.text.strip()
        results[mapped_key] = val if val else None

    logger.info(f"Scraped {season} stats for {player}: {results}")
    return results


def scrape_career_stats_totals(player: str) -> dict:
    player_slug = format_player_name(player)
    url = f"https://www.sports-reference.com/cbb/players/{player_slug}.html"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Player not found: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        soup.append(BeautifulSoup(comment, "html.parser"))

    table = soup.find("table", {"id": "players_totals"})
    if not table:
        raise ValueError("Totals table not found.")

    rows = table.find_all("tr")
    seasons_played = 0
    for row in rows:
        row_id = row.get("id", "")
        if row_id == "players_totals.Career":
            break
        if re.match(r"players_totals\.\d{4}", row_id):
            seasons_played += 1

    career_row = table.find("tr", {"id": "players_totals.Career"})
    if not career_row:
        raise ValueError("Career totals row not found.")

    key_map = {
        "year_id": "season",
        "g": "games_played",
        "games": "games_played",
        "gs": "games_started",
        "games_started": "games_started",
        "mp": "minutes_played",
        "fg": "field_goals_made",
        "fga": "field_goal_attempts",
        "fg_pct": "fg_percentage",
        "fg3": "three_pt_made",
        "fg3a": "three_pt_attempts",
        "fg3_pct": "three_pt_percentage",
        "fg2": "two_pt_made",
        "fg2a": "two_pt_attempts",
        "fg2_pct": "two_pt_percentage",
        "efg_pct": "effective_fg_percentage",
        "ft": "free_throws_made",
        "fta": "free_throw_attempts",
        "ft_pct": "free_throw_percentage",
        "orb": "offensive_rebounds",
        "drb": "defensive_rebounds",
        "trb": "total_rebounds",
        "ast": "assists",
        "stl": "steals",
        "blk": "blocks",
        "tov": "turnovers",
        "pf": "personal_fouls",
        "pts": "points",
        "awards": "awards"
    }

    results = {}
    for cell in career_row.find_all(["td", "th"]):
        key = key_map.get(cell.get("data-stat"))
        if key and cell.text.strip():
            results[key] = cell.text.strip()

    results["seasons_played"] = seasons_played
    return results

def slug_to_display_name(slug: str) -> str:
    """Converts slug (e.g. "air-force") to display name (e.g. "Air Force")"""
    return slug.replace("-", " ").title()

def scrape_basic_team_stats(team: str, season: str) -> dict:
    url = f"https://www.sports-reference.com/cbb/seasons/{season}-school-stats.html"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Player not found: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        soup.append(BeautifulSoup(comment, "html.parser"))

    table = soup.find("tbody")
    if not table:
        # Try to find any table if tbody not found directly
        table = soup.find("table")
        if table:
            table = table.find("tbody")

    display_name = slug_to_display_name(team)
    rows = table.find_all("tr")
    row = None
    for r in rows:
        school_cell = r.find("td", {"data-stat": "school_name"})
        if school_cell and display_name.lower() in school_cell.get_text().lower():
            row = r
            break

    if not row:
        raise ValueError(f"Team {display_name} not found in {season} stats.")

    key_map ={
       "school_name": "school_name",
       "g": "games",
       "wins" : "wins",
       "losses" : "losses",
       "win_loss_pct": "win_loss_pct",
       "srs": "simple_rating_system",
       "sos": "strength_of_schedule",
       "wins_conf": "wins_conference",
       "losses_conf": "losses_conference",
       "wins_home": "wins_home",
       "losses_home": "losses_home",
       "wins_visitor": "wins_away",
       "losses_visitor": "losses_away",
       "pts": "points",
       "opp_pts": "opponent_points",
       "mp": "minutes_played",
       "fg": "field_goals",
       "fga": "field_goal_attempts",
       "fg_pct": "field_goal_percentage",
       "fg3": "three_point_field_goals",
       "fg3a": "three_point_field_goal_attempts",
       "fg3_pct": "three_point_field_goal_percentage",
       "ft": "free_throws",
       "fta": "free_throw_attempts",
       "ft_pct": "free_throw_percentage",
       "orb": "offensive_rebounds",
       "trb": "total_rebounds",
       "ast": "assists",
       "stl": "steals",
       "blk": "blocks",
       "tov": "turnovers",
       "pf": "personal_fouls",
   }
    results = {}
    # Include <th> as well since "ranker" is in a <th>, not <td>
    for cell in row.find_all(["td", "th"]):
        key = key_map.get(cell.get("data-stat"))
        value = cell.text.strip()
        if key and value and value != '':  # Avoid empty or dummy cells
            results[key] = value

    return results




def test_scrape(player):
    logger = logging.getLogger("uvicorn.error")
    player_slug = format_player_name(player)
    logger.info(f"PLAYER_SLUG: {player_slug}")
    url = f"https://www.sports-reference.com/cbb/players/{player_slug}.html"
    response = requests.get(url)
    logger.info(f"URL: {url}")

    if response.status_code != 200:
        raise ValueError(f"Player not found or URL failed: {url}")

    soup = BeautifulSoup(response.text, "html.parser")
    totals_table = soup.find("table", {"id": "players_totals"}) # Find name
    if not totals_table:
        raise ValueError("No totals table found.")

    row_2025 = totals_table.find("tr", {"id": "players_totals.2025"})
    if not row_2025:
        raise ValueError("No 2024–25 season stats found.")

    key_map = {
        "year_id": "season",
        "team_name_abbr": "team",
        "conf_abbr": "conference",
        "class": "class_year",
        "pos": "position",
        "games": "games_played",
        "games_started": "games_started",
        "mp": "minutes_played",
        "fg": "field_goals_made",
        "fga": "field_goal_attempts",
        "fg_pct": "fg_percentage",
        "fg3": "three_pt_made",
        "fg3a": "three_pt_attempts",
        "fg3_pct": "three_pt_percentage",
        "fg2": "two_pt_made",
        "fg2a": "two_pt_attempts",
        "fg2_pct": "two_pt_percentage",
        "efg_pct": "effective_fg_percentage",
        "ft": "free_throws_made",
        "fta": "free_throw_attempts",
        "ft_pct": "free_throw_percentage",
        "orb": "offensive_rebounds",
        "drb": "defensive_rebounds",
        "trb": "total_rebounds",
        "ast": "assists",
        "stl": "steals",
        "blk": "blocks",
        "tov": "turnovers",
        "pf": "personal_fouls",
        "pts": "points",
        "awards": "awards"
    }

    results = {}
    cells = row_2025.find_all(["td", "th"])
    logger.info(f"# of cells found in row: {len(cells)}")

    for cell in cells:
        raw_key = cell.get("data-stat")
        mapped_key = key_map.get(raw_key, raw_key)
        val = cell.text.strip()
        results[mapped_key] = val if val else None

    logger.info(f"SCRAPED STATS: {results}")
    return results