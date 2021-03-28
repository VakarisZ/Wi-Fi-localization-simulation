import random

import matplotlib.pyplot as plt

from config import ModelConfig
from global_error_handler.error_grouper import group_errors_to_method_and_iteration
from global_error_handler.global_error_container import GlobalErrorContainer
from global_error_handler.global_error_plotter import plot_global_errors
from model_space.models.prediction_model import PredictionModel
from model_space.models.real_model import RealModel
from model_space.prediction_model.prediction_config import PredictionConfig
from prediction_errors.error_plotter import plot_errors
from prediction_errors.pred_error_handler import PredErrorHandler

seed = ModelConfig.seed

all_errors = GlobalErrorContainer()

for i in range(ModelConfig.sim_cnt):
    if ModelConfig.sim_cnt > 1:
        ModelConfig.seed = seed + str(i)
    random.seed(ModelConfig.seed)

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
            plt.pause(0.001)

    if ModelConfig.show_error_plots:
        big_errors = [error for error in pred_error_handle.pred_errors if error.error > 1]
        if big_errors:
            fig, ax = plot_errors(pred_error_handle.pred_errors)
            plt.close(fig)

    all_errors.add_error_list(pred_error_handle.pred_errors)

if ModelConfig.show_error_plots:
    three_sn_errors, two_sn_errors, one_sn_errors = group_errors_to_method_and_iteration(all_errors.error_lists)
    plot_global_errors(three_sn_errors, two_sn_errors, one_sn_errors)



#input("Simulation finished")
