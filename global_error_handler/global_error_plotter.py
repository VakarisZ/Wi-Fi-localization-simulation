from typing import List

import matplotlib.pyplot as plt

from global_error_handler.global_error_aggregate import GlobalErrorAggregate


def plot_global_errors(three_sn_errors: List[GlobalErrorAggregate],
                       two_sn_errors: List[GlobalErrorAggregate],
                       one_sn_errors: List[GlobalErrorAggregate]):
    plot_global_error_aggregates(three_sn_errors, "")


def plot_global_error_aggregates(errors: List[GlobalErrorAggregate], title: str):
    fig, ax = plt.subplots()

    avg_errors = [aggregate.get_avg_error() for aggregate in errors]

    hbars = ax.bar(range(len(avg_errors)), avg_errors, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Performance')
    ax.set_title('How fast do you want to go today?')

    # Label with given captions, custom padding and annotate options
    ax.bar_label(hbars, labels=['±%.2f' % e for e in error],
                 padding=8, color='b', fontsize=14)
    ax.set_xlim(right=16)

    plt.show()
