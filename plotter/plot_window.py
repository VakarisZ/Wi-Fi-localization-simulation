import matplotlib.pyplot as plt

from config import ModelConfig
from model_space.utils.point import Point


class PlotWindow:
    def __init__(self, params: ModelConfig, title):
        # Plot are setup
        figsize = 7, 7
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set(xlim=(params.area.x_min - ModelConfig.draw_margin,
                          params.area.x_max + ModelConfig.draw_margin),
                    ylim=(params.area.y_min - ModelConfig.draw_margin,
                          params.area.y_max + ModelConfig.draw_margin))
        self.ax.set_title(title)
        self.add_walls()
        # Set reference for global plot to be available everywhere

    def add_point(self, x, y, color='red', markersize=5, marker='o'):
        return self.ax.plot(x, y, color=color, marker=marker, markersize=markersize)

    def add_circle(self, x, y, radius, color, fill=False):
        circle = plt.Circle((x, y), radius, color=color, fill=fill)
        self.ax.add_artist(circle)

    def add_line(self, point1: Point, point2: Point, color='black', markersize=1, marker='o'):
        return self.ax.plot([point1.x, point2.x],
                            [point1.y, point2.y],
                            color=color, markersize=markersize, marker=marker)

    def add_walls(self):
        coords = ModelConfig.area
        ul_pnt = Point(coords.x_min, coords.y_max)
        ur_pnt = Point(coords.x_max, coords.y_max)
        ll_pnt = Point(coords.x_min, coords.y_min)
        lr_pnt = Point(coords.x_max, coords.y_min)

        self.add_line(ul_pnt, ur_pnt, ModelConfig.wall_color)
        self.add_line(ul_pnt, ll_pnt, ModelConfig.wall_color)
        self.add_line(lr_pnt, ur_pnt, ModelConfig.wall_color)
        self.add_line(lr_pnt, ll_pnt, ModelConfig.wall_color)

    def add_annotation(self, x, y, content):
        plt.annotate(content, (x, y))

    def redraw_point(self, point, new_x, new_y):
        new_point = self.add_point(new_x, new_y,
                                   color=point[0].get_color(),
                                   markersize=point[0].get_markersize())
        point.pop(0).remove()
        return new_point

