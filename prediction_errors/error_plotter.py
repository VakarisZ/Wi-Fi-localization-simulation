from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import ModelConfig
from prediction_errors.pred_results import PredictionResults

SN_COUNT_TO_COLOR = {
    '1': "#ff0000",
    '2': "#0066ff",
    '3': "#00cc00"
}


def plot_errors(errors: List[PredictionResults]) -> Tuple[Figure, List[Axes]]:
    fig, ax = plt.subplots()
    ax.set_title(f"Seed: {ModelConfig.seed}")
    plt.pause(0.01)
    for i in range(0, len(errors)):
        color = SN_COUNT_TO_COLOR[str(errors[i].sn_count)]
        ax.scatter(i, errors[i].error, marker='o', c=color)
    ax.set_ylabel('Error')
    ax.set_xlabel('Time')
    plt.show()
    return fig, ax
