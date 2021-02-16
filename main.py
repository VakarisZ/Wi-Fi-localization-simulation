import matplotlib.pyplot as plt

from initial_config import ModelConfig
from model_space.models.prediction_model import PredictionModel
from model_space.models.real_model import RealModel

real_model = RealModel(ModelConfig())
prediction_model = PredictionModel(ModelConfig())

plt.draw()
plt.show(block=False)

for i in range(1000):
    real_model.do_iteration(i)
    # prediction_model.do_iteration(i)
    plt.pause(0.01)

while True:
    pass
