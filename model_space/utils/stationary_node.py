from config import StationaryNodeParams
from model_space.utils.node import Node


class StationaryNode(Node):
    def __init__(self, params: StationaryNodeParams):
        super().__init__(coords=params.location_coords,
                         style={'color': 'blue', 'marker': 'o', 'markersize': 5})
        self.range = params.range
        self.id = params.id
        self.distance_to_mn = None
