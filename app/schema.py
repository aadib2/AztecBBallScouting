# schema.py
from pydantic import BaseModel, Field
from typing import Optional

class ShotDistribution(BaseModel):
    atRim: Optional[float]
    midrange: Optional[float]
    threePoint: Optional[float]

class PlayerStats(BaseModel):
    season: Optional[str] = Field(default=None)
    team: Optional[str] = Field(default=None)
    conference: Optional[str] = Field(default=None)
    class_year: Optional[str] = Field(default=None)
    position: Optional[str] = Field(default=None)
    
    games_played: Optional[str] = Field(default=None)
    games_started: Optional[str] = Field(default=None)
    minutes_played: Optional[str] = Field(default=None)

    field_goals_made: Optional[str] = Field(default=None)
    field_goal_attempts: Optional[str] = Field(default=None)
    fg_percentage: Optional[str] = Field(default=None)

    three_pt_made: Optional[str] = Field(default=None)
    three_pt_attempts: Optional[str] = Field(default=None)
    three_pt_percentage: Optional[str] = Field(default=None)

    two_pt_made: Optional[str] = Field(default=None)
    two_pt_attempts: Optional[str] = Field(default=None)
    two_pt_percentage: Optional[str] = Field(default=None)

    effective_fg_percentage: Optional[str] = Field(default=None)

    free_throws_made: Optional[str] = Field(default=None)
    free_throw_attempts: Optional[str] = Field(default=None)
    free_throw_percentage: Optional[str] = Field(default=None)

    offensive_rebounds: Optional[str] = Field(default=None)
    defensive_rebounds: Optional[str] = Field(default=None)
    total_rebounds: Optional[str] = Field(default=None)

    assists: Optional[str] = Field(default=None)
    steals: Optional[str] = Field(default=None)
    blocks: Optional[str] = Field(default=None)
    turnovers: Optional[str] = Field(default=None)
    personal_fouls: Optional[str] = Field(default=None)
    points: Optional[str] = Field(default=None)

    awards: Optional[str] = Field(default=None)


class TeamStats(BaseModel):
    school_name: Optional[str] = Field(default=None)
    games: Optional[str] = Field(default=None)
    wins: Optional[str] = Field(default=None)
    losses: Optional[str] = Field(default=None)
    win_loss_pct: Optional[str] = Field(default=None)
    simple_rating_system: Optional[str] = Field(default=None)
    strength_of_schedule: Optional[str] = Field(default=None)

    wins_conference: Optional[str] = Field(default=None)
    losses_conference: Optional[str] = Field(default=None)

    wins_home: Optional[str] = Field(default=None)
    losses_home: Optional[str] = Field(default=None)

    wins_away: Optional[str] = Field(default=None)
    losses_away: Optional[str] = Field(default=None)

    points: Optional[str] = Field(default=None)
    opponent_points: Optional[str] = Field(default=None)

    minutes_played: Optional[str] = Field(default=None)
    field_goals: Optional[str] = Field(default=None)
    field_goal_attempts: Optional[str] = Field(default=None)
    field_goal_percentage: Optional[str] = Field(default=None)
    three_point_field_goals: Optional[str] = Field(default=None)
    three_point_field_goals_attempts: Optional[str] = Field(default=None)
    three_point_field_goal_percentage: Optional[str] = Field(default=None)
    free_throws: Optional[str] = Field(default=None)
    free_throw_attempts: Optional[str] = Field(default=None)
    free_throw_percentage: Optional[str] = Field(default=None)
    offensive_rebounds: Optional[str] = Field(default=None)
    total_rebounds: Optional[str] = Field(default=None)
    assists: Optional[str] = Field(default=None)
    steals: Optional[str] = Field(default=None)
    blocks: Optional[str] = Field(default=None)
    turnovers: Optional[str] = Field(default=None)
    personal_fouls: Optional[str] = Field(default=None)


    class Config:
        extra = "ignore"
        allow_population_by_field_name = True