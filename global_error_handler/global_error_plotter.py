import matplotlib.pyplot as plt

from global_error_handler.sn_method_error_container import SnMethodErrorContainer


def plot_global_errors(three_sn_errors: SnMethodErrorContainer,
                       two_sn_errors: SnMethodErrorContainer,
                       one_sn_errors: SnMethodErrorContainer):
    plot_global_error_aggregates(three_sn_errors, 'Three SN errors')
    plot_global_error_aggregates(two_sn_errors, 'Two SN errors')
    plot_global_error_aggregates(one_sn_errors, 'One SN errors')


def plot_global_error_aggregates(errors: SnMethodErrorContainer, title: str):
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 9)

    avg_errors = [error_on_iteration.get_avg_error() for error_on_iteration in errors.errors_on_iteration]
    error_counts = [str(len(error_aggregate.errors)) for error_aggregate in errors.errors_on_iteration]

    ax.bar(x=range(0, len(avg_errors)*2, 2),
           height=avg_errors,
           align='center',
           tick_label=error_counts,
           linewidth=len(avg_errors)*[20])
    ax.set_xlabel('Iteration')
    ax.set_title(title)

    ax.plot([0,  len(avg_errors)*2], [errors.avg_sn_method_error, errors.avg_sn_method_error],
            color='red',
            marker='o')
    ax.plot([0, len(avg_errors) * 2], [errors.avg_pred_error, errors.avg_pred_error],
            color='black',
            marker='o')

    plt.show()
