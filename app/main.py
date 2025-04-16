from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from app.scraper import scrape_player_data


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/player-stats/")
def get_player_stats(player: str = Query(...)):
    stats = scrape_player_data(player)
    return {"player": player, "stats": stats}