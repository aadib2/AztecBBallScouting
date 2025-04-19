# schema.py
from pydantic import BaseModel
from typing import Optional

class ShotDistribution(BaseModel):
    atRim: Optional[float]
    midrange: Optional[float]
    threePoint: Optional[float]

class PlayerStats(BaseModel):
    playerName: Optional[str]
    team: Optional[str]
    offensiveEfficiency: Optional[float]
    defensiveEfficiency: Optional[float]
    pace: Optional[float]
    effectiveFGPercentage: Optional[float]
    adjustedFGPercentage: Optional[float]
    turnoverPercentage: Optional[float]
    offensiveReboundPercentage: Optional[float]
    defensiveReboundPercentage: Optional[float]
    freeThrowAttemptRate: Optional[float]
    assistToTurnoverRatio: Optional[float]
    threePointAttemptRate: Optional[float]
    threePointReliance: Optional[float]
    usageRate: Optional[float]
    offensiveRating: Optional[float]
    defensiveRating: Optional[float]
    assistPercentage: Optional[float]
    turnoverRate: Optional[float]
    plusMinus: Optional[float]
    opponentShotDistribution: Optional[ShotDistribution]
