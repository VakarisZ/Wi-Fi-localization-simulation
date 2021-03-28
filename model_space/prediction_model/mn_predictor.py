from copy import deepcopy
from typing import List

from config import ModelConfig
from model_space.prediction_model.prediction_params import PredictionParams
from model_space.prediction_model.shadow_predictor import get_node_prediction
from model_space.prediction_model.utils.prediction_dto import MnLocationPrediction
from model_space.utils.point import Point


MAX_PRED_LIST_LENGTH = ModelConfig.mn_history_count


class MnPredictor:
    def __init__(self, mn_pred_list: List[MnLocationPrediction],
                 max_pred_list_len=MAX_PRED_LIST_LENGTH):
        self.mn_pred_list = mn_pred_list
        self.max_pred_list_len = max_pred_list_len
        self.mn_speed = ModelConfig.mobile_node_params.speed

    def do_prediction(self, pred_params: PredictionParams):
        prediction = self.get_mn_prediction(pred_params)

        if len(self.mn_pred_list) > self.max_pred_list_len:
            self.mn_pred_list.pop(0)

        self.mn_pred_list.append(prediction)

    def get_mn_prediction(self, pred_params: PredictionParams) -> MnLocationPrediction:
        if len(pred_params.stationary_nodes) > 2:
            prediction = MnPredictor._do_trilateration(pred_params)
        # We can't do trilateration, because less than 3 ranges are obtained
        else:
            prediction = self._do_shadow_alg(pred_params)
        return prediction

    @staticmethod
    def _do_trilateration(pred_params: PredictionParams) -> MnLocationPrediction:
        # A function to apply trilateration formulas to return the (x,y) intersection point of three circles
        sn_list = pred_params.stationary_nodes
        x1, y1 = sn_list[0].coords.x, sn_list[0].coords.y
        r1 = sn_list[0].distance_to_mn

        x2, y2 = sn_list[1].coords.x, sn_list[1].coords.y
        r2 = sn_list[1].distance_to_mn

        x3, y3 = sn_list[2].coords.x, sn_list[2].coords.y
        r3 = sn_list[2].distance_to_mn

        A = 2 * x2 - 2 * x1
        B = 2 * y2 - 2 * y1
        C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
        D = 2 * x3 - 2 * x2
        E = 2 * y3 - 2 * y2
        F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
        x = (C * E - F * B) / (E * A - B * D)
        y = (C * D - A * F) / (B * D - A * E)
        return MnLocationPrediction(Point(x, y), sn_list)

    def _do_shadow_alg(self, pred_params: PredictionParams) -> MnLocationPrediction:
        return get_node_prediction(history=self.mn_pred_list,
                                   sn_params=pred_params.stationary_nodes,
                                   mn_speed=self.mn_speed)


