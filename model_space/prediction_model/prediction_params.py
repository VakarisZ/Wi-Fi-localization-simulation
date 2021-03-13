from dataclasses import dataclass
from typing import List

from model_space.utils.stationary_node import StationaryNode


@dataclass
class PredictionParams:
    stationary_nodes: List[StationaryNode]
