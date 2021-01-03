from model_space.models.model_space import ModelSpace


class RealModel(ModelSpace):
    def __init__(self, config):
        super().__init__(config, 'Real situation')
