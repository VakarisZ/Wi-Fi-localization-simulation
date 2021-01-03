from initial_config import ModelConfig


class ModelState:

    def __init__(self, initial_config: ModelConfig):
        self.mobile_node = initial_config.mobile_node
        self.stationary_nodes = initial_config.stationary_nodes
