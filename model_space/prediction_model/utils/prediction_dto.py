from dataclasses import dataclass
from typing import List

from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode


@dataclass
class MnLocationPrediction:
    location: Point
    sn_list: List[StationaryNode]
