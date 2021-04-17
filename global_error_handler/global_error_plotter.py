import matplotlib.pyplot as plt

from global_error_handler.sn_method_error_container import SnMethodErrorContainer


def plot_global_errors(three_sn_errors: SnMethodErrorContainer,
                       two_sn_errors: SnMethodErrorContainer,
                       one_sn_errors: SnMethodErrorContainer):
    plot_global_error_aggregates(three_sn_errors, 'Trilateration errors')
    plot_global_error_aggregates(two_sn_errors, 'Two brockers prediction errors')
    plot_global_error_aggregates(one_sn_errors, 'One brocker prediction errors')


def get_bar_labels(count: int):
    labels = []
    for i in range(count):
        count = i + 1
        if count % 5 == 0 or count == 1:
            labels.append(f"{count}")
        else:
            labels.append('')
    return labels


def plot_global_error_aggregates(errors: SnMethodErrorContainer, title: str):
    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(16, 9)

    avg_errors = [round(error_on_iteration.get_avg_error(), 2) for error_on_iteration in errors.errors_on_iteration]
    error_counts = [len(error_aggregate.errors) for error_aggregate in errors.errors_on_iteration]

    ax[0].bar(x=range(0, len(avg_errors) * 2, 2),
              height=avg_errors,
              align='center',
              linewidth=len(avg_errors) * [20])
    ax[0].set_xticks(range(0, len(avg_errors) * 2, 2))

    ax[0].set_xticklabels(get_bar_labels(len(avg_errors)))
    ax[0].set_xlabel('Iteration')
    ax[0].set_ylabel('Average error on iteration')
    ax[0].set_title(title)

    ax[0].plot([0, len(avg_errors) * 2], [errors.avg_sn_method_error, errors.avg_sn_method_error],
               color='red',
               marker='o',
               label='Avg. error for this method')
    ax[0].plot([0, len(avg_errors) * 2], [errors.avg_pred_error, errors.avg_pred_error],
               color='black',
               marker='o',
               label='Avg. error for all predictions')
    ax[0].legend()

    rects = ax[1].bar(x=range(0, len(avg_errors) * 2, 2),
                      height=error_counts,
                      align='center',
                      linewidth=len(avg_errors) * [20])
    ax[1].set_xlabel('Iteration')
    ax[1].set_ylabel('Prediction count')
    ax[1].set_xticks(range(0, len(avg_errors) * 2, 2))
    ax[1].bar_label(rects, error_counts)

    plt.show()
    plt.pause(0.01)
