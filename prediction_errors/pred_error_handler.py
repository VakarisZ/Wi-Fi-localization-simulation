import math
from typing import List

from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode
from prediction_errors.pred_results import PredictionResults


class PredErrorHandler:
    def __init__(self):
        self.pred_errors = []

    def add_pred_error(self,
                       real_mn: Point,
                       pred_mn: Point,
                       sn_list: List[StationaryNode]):
        math_error = math.dist([real_mn.x, real_mn.y], [pred_mn.x, pred_mn.y])
        self.pred_errors.append(PredictionResults(sn_count=len(sn_list), error=math_error))
