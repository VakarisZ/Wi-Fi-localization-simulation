from config import ModelConfig
from model_space.models.model_state import ModelState
from plotter.model_drawer import ModelDrawer


class ModelSpace:
    def __init__(self, model_config: ModelConfig, title):
        self.model_state = ModelState(model_config)
        if ModelConfig.show_simulation_plots:
            self.model_drawer = ModelDrawer(self.model_state, title)
