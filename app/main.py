from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, HTTPException
from app.scraper import test_scrape, scrape_season_stats, scrape_team_schedule, router, scrape_career_stats_totals, scrape_basic_team_stats, get_play_by_play
from app.schema import PlayerStats, TeamStats
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def catch_exceptions_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    return FileResponse("teamdata.html")

#@app.get("/player-stats/")
#def get_player_stats(player: str = Query(...)):
#    stats = scrape_player_data(player)
#    return {"player": player, "stats": stats}

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
def get_career_totals(name: str, pretty: bool = Query(False)):
    raw_stats = scrape_career_stats_totals(name)
    filtered_stats = {k: v for k, v in raw_stats.items() if v is not None}

    if pretty:
        import json
        pretty_json = json.dumps(filtered_stats, indent=4)
        return Response(content=pretty_json, media_type="application/json")

    return filtered_stats

@app.get("/teams/{name}/season/{year}")
def get_team_season_stats(name: str, year: str, pretty: bool = Query(False)):
    raw_stats = scrape_basic_team_stats(name, year)

    if pretty:
        import json
        pretty_json = json.dumps(raw_stats, indent=4)
        return Response(content=pretty_json, media_type="application/json")

    return TeamStats(**raw_stats)

@app.get("/team-schedule/")
def get_team_schedule(team: str = Query("lal", description="NBA team slug, e.g., 'lal' for Lakers")):
    return scrape_team_schedule(team)

#@app.get("/playbyplay/")
#def get_game_play_by_play(gameId: str = Query(..., description="ESPN game ID, e.g., '401706868'")):
#    return get_play_by_play(gameId)
@app.get("/playbyplay/")
def get_play_by_play_endpoint(
        gameId: str = Query(..., description="ESPN game ID, e.g., '401706868'"),
        pretty: bool = Query(False, description="Return pretty-printed JSON")
):
    data = get_play_by_play(gameId)

    if pretty:
        pretty_json = json.dumps(data, indent=4)
        return Response(content=pretty_json, media_type="application/json")

    return data


# Include the router
app.include_router(router)