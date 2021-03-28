import math
from math import acos, cos, sin
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
        predicted_location = two_sn_choice.get_correct_prediction(possible_locations,
                                                                  history[-1].location,
                                                                  mn_speed)
    else:
        predicted_location = one_sn_choice.get_correct_prediction(possible_locations, history)
    return MnLocationPrediction(predicted_location, sn_params)


def calculate_possible_locations(history: List[MnLocationPrediction],
                                 sn_params: List[StationaryNode],
                                 mn_speed: float) -> Tuple[Point, Point]:
    # for two stationary nodes, don't use history
    if len(sn_params) > 1:
        pnt1 = sn_params[0].coords
        pnt2 = sn_params[1].coords
        # Sides are marked according to the point they oppose, e.g. d12 is opposite to point 3, d23 to point 1 etc.
        d12 = math.dist(pnt1.as_list(), pnt2.as_list())
        d13 = sn_params[0].distance_to_mn
        d23 = sn_params[1].distance_to_mn
    else:
        last_location = history[-1]
        # We need to do the calculations with the same sn
        last_sn_params = last_location.sn_list[0]
        current_sn_params = get_sn_from_list(last_sn_params.id, sn_params)
        pnt1 = last_location.location
        pnt2 = current_sn_params.coords
        d12 = math.dist(pnt1.as_list(), pnt2.as_list())  # Distance 12
        d13 = float(mn_speed)  # Distance 13
        d23 = current_sn_params.distance_to_mn  # Distance 23

    return get_third_point_locations(pnt1, pnt2, d12, d13, d23)


def get_third_point_locations(pnt1: Point,
                              pnt2: Point,
                              d12: float,
                              d13: float,
                              d23: float):
    x1 = pnt1.x
    y1 = pnt1.y
    x2 = pnt2.x
    y2 = pnt2.y

    u = x2 - x1
    v = y2 - y1

    cos_ther_result = (d12 ** 2 + d13 ** 2 - d23 ** 2) / (2 * d12 * d13)
    a1 = acos_error_compliant(cos_ther_result)  # Angle 1

    RHS1 = x1 * u + y1 * v + d13 * d12 * cos(a1)
    RHS2 = y2 * u - x2 * v + d13 * d12 * sin(a1)
    x3 = (1 / d12 ** 2) * (u * RHS1 - v * RHS2)
    y3 = (1 / d12 ** 2) * (v * RHS1 + u * RHS2)

    RHS2_alt = y2 * u - x2 * v - d13 * d12 * sin(a1)
    x3_alt = (1 / d12 ** 2) * (u * RHS1 - v * RHS2_alt)
    y3_alt = (1 / d12 ** 2) * (v * RHS1 + u * RHS2_alt)

    p1 = Point(x3, y3)
    p2 = Point(x3_alt, y3_alt)

    return p1, p2


# TODO move this method
def get_sn_from_list(node_id: str, node_list: List[StationaryNode]) -> StationaryNode:
    node = [sn for sn in node_list if sn.id == node_id]
    if not node:
        return node_list[0]
    return node[0]


def acos_error_compliant(value: float):
    if value > 1:
        return acos(1)
    elif value < -1:
        return acos(-1)
    else:
        return acos(value)
