import matplotlib.pyplot as plt

from initial_config import ModelConfig


class PlotWindow:
    def __init__(self, params: ModelConfig, title):
        # Plot are setup
        figsize = 7, 7
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set(xlim=(params.area.x_min, params.area.x_max),
                    ylim=(params.area.y_min, params.area.y_max))
        self.ax.set_title(title)

    def add_point(self, x, y, color='red', markersize=5, marker='o'):
        return self.ax.plot(x, y, color=color, marker=marker, markersize=markersize)

    def add_circle(self, x, y, radius, color, fill=False):
        circle = plt.Circle((x, y), radius, color=color, fill=fill)
        self.ax.add_artist(circle)

    def add_line(self, point1, point2, color='black', markersize=1, marker='o'):
        return self.ax.plot([point1.x, point2.x],
                            [point1.y, point2.y],
                            color=color, markersize=markersize, marker=marker)

    def redraw_point(self, point, new_x, new_y):
        new_point = self.add_point(new_x, new_y,
                                   color=point[0].get_color(),
                                   markersize=point[0].get_markersize())
        point.pop(0).remove()
        return new_point

