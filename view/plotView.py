from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import app, scene
from vispy.color import Color
import numpy as np
from Signalverarbeitung.signal_processor import SignalProcessor

class VisPyPlotWidget(QWidget):
    """
    A widget that displays live plotting using VisPy, supporting multiple lines in a single plot with offsets.
    """

    def __init__(self, parent=None):
        """
        Initialize the plot widget with VisPy canvas.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.sp = SignalProcessor(545.5)
        self.filter = self.sp.antifilter

        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'panzoom'

        self._default_x_range = (0, 10)
        self._default_y_range = (-1000, 1000)

        self.line_list = []
        self._num_plots = 0

        self.view.camera.set_range(x=self._default_x_range, y=self._default_y_range)
        self.cleared = True

    def set_filter(self, f):
        print("set_filter(" + str(f) + ")")
        if f == 0:
            self.filter = self.sp.antifilter
        elif f == "rms":
            self.filter = self.sp.calculate_rms
        elif f == "butter":
            self.filter = self.sp.butter_filter
        else:
            self.filter = self.sp.antifilter

        
    def setup_plots(self, num_lines):
        """
        Creates the specified number of line plots within the single view.
        """
        if num_lines <= 0:
            print("Warning: num_lines must be greater than 0.")
            return

        self.clear_plots()
        self._num_plots = num_lines

        for i in range(num_lines):
            color = Color((i / num_lines, 0.5, 1 - (i / num_lines), 1))
            line = scene.Line(np.array([[0, 0]]), parent=self.view.scene, color=color, width=2)
            self.line_list.append(line)

        self.canvas.update()

    def clear_plots(self):
        """
        Removes all existing lines from the view.
        """
        for line in self.line_list:
            line.parent = None
        self.line_list.clear()
        self._num_plots = 0
        self.canvas.update()
        self.cleared = True

    def update_data(self, time_points, data_list, y_offset_per_line=1000):
        """
        Update the plots with new data.
        """
        if len(data_list) != self._num_plots:
            print(f"Error: Number of data arrays ({len(data_list)}) does not match "
                  f"number of existing lines ({self._num_plots}). Call setup_plots first.")
            return

        if len(time_points) == 0:
            empty_data = np.array([[0, 0]])
            for line in self.line_list:
                line.set_data(empty_data)
            self.canvas.update()
            return
        all_y_values = []

        for i in range(len(data_list)):
            filtered_data = self.filter(data_list[i])
            offset_data = filtered_data + (i * y_offset_per_line)
            line_data = np.column_stack((time_points, offset_data))
            self.line_list[i].set_data(line_data)
            all_y_values.extend(offset_data)

        if len(all_y_values) > 0:
            min_y, max_y = np.min(all_y_values), np.max(all_y_values)
            margin_y = (max_y - min_y) * 0.1 if (max_y - min_y) != 0 else 10
            self.view.camera.set_range(x=self._default_x_range, y=(min_y - margin_y, max_y + margin_y))
        else:
            self.view.camera.set_range(x=self._default_x_range, y=self._default_y_range)


        self.canvas.update()

    def plot_stuff(self, time_points, data_list):
        """
        set up plots and update data in one go.
        """

        self.setup_plots(len(data_list))
        self.update_data(time_points, data_list)
        self.cleared = False

