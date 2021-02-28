from dataclasses import dataclass

from initial_config import ModelConfig


@dataclass
class PredictionConfig:
    area = ModelConfig.area
    mobile_node_params = ModelConfig.mobile_node_params
    stationary_node_param_list = ModelConfig.stationary_node_param_list
