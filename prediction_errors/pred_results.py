from dataclasses import dataclass


@dataclass
class PredictionResults:
    sn_count: int
    error: float
