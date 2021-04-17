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

SN_COUNT_TO_LABEL = {
    '1': "One brocker algorithm",
    '2': "Two brockers algorithm",
    '3': "Three brockers algorithm"
}


def get_label_for_algorithm(is_label_added_list: List[bool],
                            sn_count: int):
    if not is_label_added_list[sn_count-1]:
        is_label_added_list[sn_count-1] = True
        return SN_COUNT_TO_LABEL[str(sn_count)]


def plot_errors(errors: List[PredictionResults]) -> Tuple[Figure, List[Axes]]:
    fig, ax = plt.subplots()
    ax.set_title(f"Seed: {ModelConfig.seed}")
    plt.pause(0.01)

    is_labels_added = [False, False, False]
    for i in range(0, len(errors)):
        color = SN_COUNT_TO_COLOR[str(errors[i].sn_count)]
        ax.scatter(i,
                   errors[i].error,
                   marker='o',
                   c=color,
                   label=get_label_for_algorithm(is_labels_added,
                                                 errors[i].sn_count))
    ax.set_ylabel('Error')
    ax.set_xlabel('Time')
    ax.legend()
    plt.show()
    return fig, ax
