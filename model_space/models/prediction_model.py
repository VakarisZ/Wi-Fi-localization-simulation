from model_space.models.model_space import ModelSpace
from model_space.prediction_model.mn_predictor import MnPredictor
from model_space.prediction_model.prediction_params import PredictionParams


class PredictionModel(ModelSpace):
    def __init__(self, config):
        super().__init__(config, 'Prediction')
        self.mn_predictor = MnPredictor([])

    def do_iteration(self, i, params: PredictionParams):
        self.mn_predictor.do_prediction(params)
        self.set_state_to_prediction()
        self.model_drawer.draw_state(self.model_state)

    def set_state_to_prediction(self):
        pred = self.mn_predictor.mn_pred_list[-1]
        self.model_state.mobile_node.coords.x = pred.location.x
        self.model_state.mobile_node.coords.y = pred.location.y
