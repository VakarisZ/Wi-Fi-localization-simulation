from copy import deepcopy
from typing import List

from initial_config import ModelConfig
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
        # TODO do the actual trilateration instead of faking
        if pred_params.mobile_node:
            x, y = pred_params.mobile_node.coords.x, pred_params.mobile_node.coords.x
            return MnLocationPrediction(Point(x, y), deepcopy(pred_params.stationary_nodes))
        else:
            raise Exception("Trilateration not yet implemented, we use actual node parameters instead of predicting.")

    def _do_shadow_alg(self, pred_params: PredictionParams) -> MnLocationPrediction:
        return get_node_prediction(history=self.mn_pred_list,
                                   sn_params=pred_params.stationary_nodes,
                                   mn_speed=self.mn_speed)


