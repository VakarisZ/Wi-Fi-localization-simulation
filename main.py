import matplotlib.pyplot as plt

from initial_config import ModelConfig
from model_space.models.prediction_model import PredictionModel
from model_space.models.real_model import RealModel
from model_space.prediction_model.prediction_config import PredictionConfig

real_model = RealModel(ModelConfig())
prediction_model = PredictionModel(PredictionConfig())

plt.draw()
plt.show(block=False)

for i in range(1000):
    real_model.do_iteration(i)
    params = real_model.get_params_for_prediction()
    prediction_model.do_iteration(i, params)
    plt.pause(0.01)

while True:
    pass
