from initial_config import ModelConfig
from model_space.models.model_state import ModelState
from plotter.model_drawer import ModelDrawer


class ModelSpace:
    def __init__(self, model_config: ModelConfig, title):
        self.model_state = ModelState(model_config)
        self.model_drawer = ModelDrawer(self.model_state, title)

    def do_iteration(self, i):
        self.model_state.mobile_node.move()
        self.model_drawer.draw_state(self.model_state)
