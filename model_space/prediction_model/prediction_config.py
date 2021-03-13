from copy import deepcopy
from dataclasses import dataclass

from config import ModelConfig


@dataclass
class PredictionConfig:
    area = ModelConfig.area
    mobile_node_params = deepcopy(ModelConfig.mobile_node_params)
    stationary_node_param_list = ModelConfig.stationary_node_param_list
