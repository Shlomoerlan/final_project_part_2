from dataclasses import dataclass



@dataclass(frozen=True)
class TrendAnalysis:
    time_period: str
    count: int
    frequency: float
