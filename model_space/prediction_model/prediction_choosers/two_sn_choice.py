import math
from typing import Tuple

from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode


def get_correct_prediction(predictions: Tuple[Point, Point],
                           last_position: Point,
                           speed: float):
    diff0 = abs(math.dist(predictions[0].as_list(), last_position.as_list()) - speed)
    diff1 = abs(math.dist(predictions[1].as_list(), last_position.as_list()) - speed)

    if diff0 < diff1:
        return predictions[0]
    else:
        return predictions[1]
