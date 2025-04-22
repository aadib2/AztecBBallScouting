from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from app.scraper import test_scrape, scrape_season_stats, scrape_career_stats_totals
from app.schema import PlayerStats


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# player name formatting in url can be the following ways:
# lamont-butler
# lamont%20butler
@app.get("/players/{name}")
def get_player_stats(name: str):
    raw_stats = test_scrape(name)
    print(raw_stats)
    return PlayerStats(**raw_stats)


@app.get("/players/{name}/season/{year}")
def get_season_stats(name: str, year: str):
    raw_stats = scrape_season_stats(name, year)
    return PlayerStats(**raw_stats)

@app.get("/players/{name}/career_totals")
def get_career_stats_totals(name: str):
    raw_stats = scrape_career_stats_totals(name)
    filtered_stats = {k: v for k, v in raw_stats.items() if v is not None}
    return filtered_stats