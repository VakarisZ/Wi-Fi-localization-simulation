from model_space.models.model_space import ModelSpace


class PredictionModel(ModelSpace):
    def __init__(self, config):
        super().__init__(config, 'Prediction')
