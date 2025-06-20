from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import app, scene
from vispy.color import Color
import numpy as np


class VisPyPlotWidget(QWidget):
    """
    A widget that displays live plotting using VisPy, supporting multiple lines in a single plot with offsets.

    This class is part of the View layer in the MVVM architecture. It:
    - Creates and manages the VisPy canvas and a single VisPy view.
    - Dynamically creates multiple lines based on the number of data streams.
    - Updates each line with new data, applying an offset.
    """

    def __init__(self, parent=None):
        """
        Initialize the plot widget with VisPy canvas.
        The single view and lines will be created dynamically later.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Create PyQt layout
        layout = QVBoxLayout(self)  # Set layout directly on self

        # Create VisPy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        # Create a single VisPy view for all lines
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'panzoom'

        # Store default ranges
        self._default_x_range = (0, 10)
        self._default_y_range = (-1000, 1000)  # Initial wider range

        # Initialize list to store lines
        self.line_list = []
        self._num_plots = 0 # To keep track of how many lines are currently configured

        # Set initial range for the single view's camera
        self.view.camera.set_range(x=self._default_x_range, y=self._default_y_range)
        self.cleared = True

    def setup_plots(self, num_lines):
        """
        Dynamically creates the specified number of line plots within the single view.
        Each line will have a vertical offset applied.

        This method should be called AFTER the widget is initialized,
        once you know how many lines you need.

        Args:
            num_lines (int): The number of independent lines to create.
            y_offset_per_line (float): The vertical offset to apply between consecutive lines.
        """
        if num_lines <= 0:
            print("Warning: num_lines must be greater than 0.")
            return

        # Clear existing lines if setup_plots is called again
        self.clear_plots()
        self._num_plots = num_lines

        # Create lines within the single view
        for i in range(num_lines):
            # We'll use different colors for clarity if there are many lines
            color = Color((i / num_lines, 0.5, 1 - (i / num_lines), 1))  # Example: gradient color
            line = scene.Line(np.array([[0, 0]]), parent=self.view.scene, color=color, width=2)
            self.line_list.append(line)

        self.canvas.update()  # Force an update after creating elements

    def clear_plots(self):
        """Removes all existing lines from the view."""
        for line in self.line_list:
            # Setting parent to None removes the visual from the scene graph
            line.parent = None
        self.line_list.clear()
        self._num_plots = 0
        self.canvas.update()
        self.cleared = True

    def update_data(self, time_points, data_list, y_offset_per_line=1000):
        """
        Update the plots with new data.

        Args:
            time_points (np.ndarray): Array of time values (shared across all lines).
            data_list (list of np.ndarray): A list where each element is an
                                            array of signal values for a corresponding line.
            y_offset_per_line (float): The vertical offset to apply to each consecutive line.
        """
        # Ensure the number of data arrays matches the number of created lines
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

        # Calculate min/max for auto-scaling
        all_y_values = []

        # Update each line individually with offset
        # TODO bliblablubb filter
        # des ding da ordner tauschn
        # sambling rate ist gehartkoded. müssma ändern!!!!!!!!!!!!!!!!

        for i in range(len(data_list)):
            offset_data = data_list[i] + (i * y_offset_per_line)
            line_data = np.column_stack((time_points, offset_data))
            self.line_list[i].set_data(line_data)
            all_y_values.extend(offset_data)

        # Adjust the y-range of the single view based on the combined data
        if len(all_y_values) > 0:
            min_y, max_y = np.min(all_y_values), np.max(all_y_values)
            # Add a small margin to the range for better visualization
            margin_y = (max_y - min_y) * 0.1 if (max_y - min_y) != 0 else 10
            self.view.camera.set_range(x=self._default_x_range, y=(min_y - margin_y, max_y + margin_y))
        else:
            # Revert to default y-range if no data
            self.view.camera.set_range(x=self._default_x_range, y=self._default_y_range)


        self.canvas.update()  # Force a redraw of the canvas

    def plot_stuff(self, time_points, data_list):
        """
        Convenience method to set up plots and update data in one go.
        Args:
        time_points (np.ndarray): Array of time values.
        data_list (list of np.ndarray): List of signal values for each line.
        y_offset_per_line (float): The vertical offset to apply to each consecutive line.
        """

        self.setup_plots(len(data_list))
        self.update_data(time_points, data_list)
        self.cleared = False

