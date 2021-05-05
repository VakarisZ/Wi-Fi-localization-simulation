import math

from config import ModelConfig
from model_space.models.model_state import ModelState
from model_space.utils.point import Point
from plotter.plot_window import PlotWindow


class ModelDrawer:
    def __init__(self, model_state: ModelState, title):
        model_config = ModelConfig()
        self.window = PlotWindow(model_config, title)
        self.stationary_nodes = []
        self.mobile_node = None
        self.draw_points(model_state)
        self.lines = []
        self.history_line = None
        self.curve_fit_line = None

        if title == 'Prediction':
            ModelConfig.prediction_plot = self
        else:
            ModelConfig.simulation_plot = self

    def draw_history(self, xdata, ydata):
        self.history_line = self.window.ax.plot(xdata, ydata, 'b-')

    def draw_curve_fit_line(self, xdata, ydata):
        self.curve_fit_line = self.window.ax.plot(xdata, ydata, 'og', markersize=3, alpha=0.5)

    def clean_curve_fit(self):
        if self.history_line:
            self.history_line.pop(0).remove()

    def clean_history(self):
        if self.curve_fit_line:
            self.curve_fit_line.pop(0).remove()

    def draw_state(self, model_state: ModelState):
        self.clean_state()
        self.draw_mobile_node(model_state.mobile_node)
        self.draw_lines_for_stationary_nodes(model_state)

    def clean_state(self):
        if ModelConfig.show_mn_history:
            # change mn style
            mn = self.mobile_node.pop(0)
            mn._color = 'black'
            mn._markersize = 2.5
        else:
            # remove mn
            self.mobile_node.pop(0).remove()
        # remove all lines
        [line.pop(0).remove() for line in self.lines]
        self.lines = []

    def draw_points(self, model_state: ModelState):
        self.draw_stationary_nodes(model_state.stationary_nodes)
        self.draw_mobile_node(model_state.mobile_node)

    def draw_stationary_nodes(self, stationary_nodes):
        for sn in stationary_nodes:
            self.stationary_nodes.append(self.draw_node(sn))
            self.window.add_circle(sn.coords.x, sn.coords.y, sn.range, sn.style['color'])

    def draw_mobile_node(self, mobile_node):
        self.mobile_node = self.draw_node(mobile_node)

    def draw_node(self, node):
        if hasattr(node, 'id'):
            self.window.add_annotation(x=node.coords.x, y=node.coords.y, content=node.id)
        return self.window.add_point(x=node.coords.x,
                                     y=node.coords.y,
                                     color=node.style['color'],
                                     markersize=node.style['markersize'],
                                     marker=node.style['marker'])

    def draw_lines_for_stationary_nodes(self, model_state: ModelState):
        # Remove all lines
        for line in self.lines:
            line.pop(0).remove()
        self.lines = []
        for sn in model_state.stationary_nodes:
            if ModelDrawer.is_mn_reachable_from_sn(sn, model_state.mobile_node):
                self.lines.append(self.window.add_line(sn.coords, model_state.mobile_node.coords))

    @staticmethod
    def is_mn_reachable_from_sn(sn, mn):
        return ModelDrawer.is_in_circle(sn.coords.as_list(), sn.range, mn.coords.as_list())

    @staticmethod
    def is_in_circle(center: Point, radius, point: Point):
        return math.dist(center, point) <= radius

