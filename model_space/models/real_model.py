import math
from copy import deepcopy
from typing import List

from config import ModelConfig, StationaryNodeParams
from model_space.models.model_space import ModelSpace
from model_space.prediction_model.prediction_params import PredictionParams
from model_space.utils.mobile_node_utils.random_param_fetcher import apply_random_error_to_distance
from model_space.utils.node import Node
from model_space.utils.stationary_node import StationaryNode
from plotter.model_drawer import ModelDrawer


class RealModel(ModelSpace):
    def __init__(self, config):
        super().__init__(config, 'Real situation')

    def do_iteration(self, i):
        self.model_state.mobile_node.move()
        for sn in self.model_state.stationary_nodes:
            sn.distance_to_mn = RealModel.calculate_distance_between_nodes(self.model_state.mobile_node, sn)
        if ModelConfig.show_simulation_plots:
            self.model_drawer.draw_state(self.model_state)

    def get_params_for_prediction(self) -> PredictionParams:
        sn_list = self._get_stationary_nodes()
        params = PredictionParams(stationary_nodes=sn_list)
        return params

    def _get_stationary_nodes(self) -> List[StationaryNode]:
        sn_list = []
        mn = self.model_state.mobile_node

        for sn in self.model_state.stationary_nodes:
            if ModelDrawer.is_mn_reachable_from_sn(sn, mn):
                distance = apply_random_error_to_distance(RealModel.calculate_distance_between_nodes(mn, sn))
                sn_params = StationaryNodeParams(location_coords=sn.coords, range=sn.range, id=sn.id)
                new_sn = StationaryNode(sn_params)
                new_sn.distance_to_mn = distance
                sn_list.append(new_sn)

        return sn_list

    @staticmethod
    def calculate_distance_between_nodes(node1: Node, node2: Node) -> float:
        node1_coords = [node1.coords.x, node1.coords.y]
        node2_coords = [node2.coords.x, node2.coords.y]
        return math.dist(node1_coords, node2_coords)
