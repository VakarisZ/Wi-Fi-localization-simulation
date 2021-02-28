import math
from typing import Tuple

from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode


def get_correct_prediction(predictions: Tuple[Point, Point], sn: StationaryNode):
    distance0 = math.dist([predictions[0].x, predictions[0].y], [sn.coords.x, sn.coords.y])
    distance1 = math.dist([predictions[1].x, predictions[1].y], [sn.coords.x, sn.coords.y])

    diff0 = abs(distance0 - sn.distance_to_mn)
    diff1 = abs(distance1 - sn.distance_to_mn)

    if diff0 < diff1:
        return predictions[0]
    else:
        return predictions[1]
