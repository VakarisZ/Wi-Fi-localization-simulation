from initial_config import ModelConfig
from model_space.utils.mobile_node import MobileNode
from model_space.utils.stationary_node import StationaryNode


class ModelState:

    def __init__(self, initial_config: ModelConfig):
        self.mobile_node = MobileNode(initial_config.mobile_node_params)
        self.stationary_nodes = [StationaryNode(params) for params in initial_config.stationary_node_param_list]
