import math
from copy import deepcopy
from math import acos, cos, atan2, sin
from typing import List, Tuple

from model_space.prediction_model.utils.prediction_dto import MnLocationPrediction
from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode
from model_space.prediction_model.prediction_choosers import two_sn_choice, one_sn_choice


def get_node_prediction(history: List[MnLocationPrediction],
                        sn_params: List[StationaryNode],
                        mn_speed: float) -> MnLocationPrediction:
    possible_locations = calculate_possible_locations(history, sn_params, mn_speed)
    if len(sn_params) > 1:
        predicted_location = two_sn_choice.get_correct_prediction(possible_locations, sn_params[1])
    else:
        predicted_location = one_sn_choice.get_correct_prediction(possible_locations, history)
    return MnLocationPrediction(predicted_location, deepcopy(sn_params))


def calculate_possible_locations(history: List[MnLocationPrediction],
                                 sn_params: List[StationaryNode],
                                 mn_speed: float) -> Tuple[Point, Point]:
    last_location = history[-1]
    # We need to do the calculations with the same sn
    last_sn_params = last_location.sn_list[0]
    current_sn_params = get_sn_from_list(last_sn_params.id, sn_params)

    return get_possible_points(last_location,
                               current_sn_params,
                               mn_speed)


def get_possible_points(last_location: MnLocationPrediction,
                        current_sn: StationaryNode,
                        mn_speed: float) -> Tuple[Point, Point]:
    x1 = last_location.location.x  # X1
    y1 = last_location.location.y  # Y1
    x2 = current_sn.coords.x  # X2
    y2 = current_sn.coords.y  # Y2

    d12 = math.dist([x2, y2], [x1, y1])  # Distance 12
    d13 = mn_speed  # Distance 13
    d23 = current_sn.distance_to_mn  # Distance 23

    a1 = acos((d12 ** 2 + d13 ** 2 - d23 ** 2) / (2 * d12 * d13))  # Angle 1

    x3 = x1 + d13 * cos(atan2(x2 - x1, y2 - y1) + a1)  # X3
    x3_alt = x1 + d13 * cos(atan2(x2 - x1, y2 - y1) - a1)  # X3 alt
    y3 = y1 + d13 * sin(atan2(x2 - x1, y2 - y1) + a1)  # Y3
    y3_alt = y1 + d13 * sin(atan2(x2 - x1, y2 - y1) - a1)  # Y3 alt

    p1 = Point(x3, y3)
    p2 = Point(x3_alt, y3_alt)

    return p1, p2


# TODO move this method
def get_sn_from_list(node_id: str, node_list: List[StationaryNode]) -> StationaryNode:
    node = [sn for sn in node_list if sn.id == node_id]
    if not node:
        return node_list[0]
    return node[0]
