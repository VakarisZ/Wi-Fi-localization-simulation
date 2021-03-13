import matplotlib.pyplot as plt

from config import ModelConfig
from model_space.models.prediction_model import PredictionModel
from model_space.models.real_model import RealModel
from model_space.prediction_model.prediction_config import PredictionConfig
from prediction_errors.error_plotter import plot_errors
from prediction_errors.pred_error_handler import PredErrorHandler

seed = ModelConfig.seed

for i in range(ModelConfig.sim_cnt):
    ModelConfig.seed = seed + str(i)

    real_model = RealModel(ModelConfig())
    prediction_model = PredictionModel(PredictionConfig())
    pred_error_handle = PredErrorHandler()
    for j in range(ModelConfig.iteration_count):
        real_model.do_iteration(j)
        params = real_model.get_params_for_prediction()
        prediction_model.do_iteration(j, params)
        pred_error_handle.add_pred_error(real_model.model_state.mobile_node.coords,
                                         prediction_model.model_state.mobile_node.coords,
                                         params.stationary_nodes)
        if ModelConfig.show_simulation_plots:
            plt.pause(0.01)

if ModelConfig.show_error_plots:
    plot_errors(pred_error_handle.pred_errors)

input("Simulation finished")
