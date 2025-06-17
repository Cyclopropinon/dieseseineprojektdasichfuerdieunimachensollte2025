from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import app, scene
import numpy as np


class VisPyPlotWidget(QWidget):
    """
    A widget that displays live plotting using VisPy, supporting multiple independent plots.

    This class is part of the View layer in the MVVM architecture. It:
    - Creates and manages the VisPy canvas and an internal VisPy Grid layout.
    - Dynamically creates multiple views and lines based on the number of data streams.
    - Updates each plot with new data.
    """

    def __init__(self, parent=None):
        """
        Initialize the plot widget with VisPy canvas.
        Views and lines will be created dynamically later.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Create PyQt layout
        layout = QVBoxLayout(self)  # Set layout directly on self

        # Create VisPy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        # Create a VisPy Grid widget in the central widget of the canvas
        # This grid will manage the layout of multiple views (subplots)
        self.grid = self.canvas.central_widget.add_grid()

        # Initialize lists to store views and lines
        self.view_list = []
        self.line_list = []

        # Store default ranges
        self._default_x_range = (0, 10)
        self._default_y_range = (-1000, 1000)  # Use the wider range consistently

    def setup_plots(self, num_plots):
        """
        Dynamically creates the specified number of views and line plots,
        arranging them vertically in the VisPy grid.

        This method should be called AFTER the widget is initialized,
        once you know how many plots you need.

        Args:
            num_plots (int): The number of independent plots (views and lines) to create.
        """
        if num_plots <= 0:
            print("Warning: num_plots must be greater than 0.")
            return

        # Clear existing views and lines if setup_plots is called again
        self.clear_plots()

        # Determine how to arrange the plots in the grid (e.g., one plot per row)
        for i in range(num_plots):
            # Add a new view to a new row in the VisPy grid
            # Each view occupies a separate row and the first column (col=0)
            view = self.grid.add_view(row=i, col=0)
            view.camera = 'panzoom'

            # Optionally add a small border/margin for visual separation between plots
            view.border_width = 1
            view.border_color = 'gray'

            self.view_list.append(view)

            # Create a line visual and add it to this specific view's scene
            # We'll use different colors for clarity if there are many lines
            color = scene.Color((i / num_plots, 0.5, 1 - (i / num_plots), 1))  # Example: gradient color
            line = scene.Line(np.array([[0, 0]]), parent=view.scene, color=color, width=2)
            self.line_list.append(line)

            # Set the initial range for this specific view's camera
            view.camera.set_range(x=self._default_x_range, y=self._default_y_range)

            # Optionally add a label for each plot
            label = scene.Label(f"Plot {i + 1}", color='white', font_size=10)
            label.height_max = 20  # Limit label height
            self.grid.add_widget(label, row=i, col=0, row_span=1,
                                 col_span=1)  # Place label in the same grid cell as view
            label.anchor = ('left', 'top')  # Position label at top-left of its cell
            label.parent = view.scene  # Make label part of the view's scene (so it moves with pan/zoom)

        # Adjust grid row/column weights if needed for proper resizing
        self.grid.set_row_stretch(0, 1)  # Give all rows equal stretch

        self.canvas.update()  # Force an update after creating elements

    def clear_plots(self):
        """Removes all existing views and lines from the grid."""
        for view in self.view_list:
            # Setting parent to None removes the visual from the scene graph
            # and from the grid layout where it was added.
            # This also implicitly removes lines within these views if their parent was view.scene
            view.parent = None
            # Manually clear visuals within the view's scene to be safe
            for visual in list(view.scene.children):
                visual.parent = None

        self.view_list.clear()
        self.line_list.clear()
        self.grid._widgets.clear()  # Clear widgets from the grid itself (important for reuse)
        self.canvas.update()

    def update_data(self, time_points, data_list):
        """
        Update the plots with new data.

        Args:
            time_points (np.ndarray): Array of time values (shared across all plots).
            data_list (list of np.ndarray): A list where each element is an
                                            array of signal values for a corresponding line.
        """
        # Ensure the number of data arrays matches the number of created lines
        if len(data_list) != len(self.line_list):
            print(f"Error: Number of data arrays ({len(data_list)}) does not match "
                  f"number of existing plots ({len(self.line_list)}). Call setup_plots first.")
            return

        if len(time_points) == 0:
            empty_data = np.array([[0, 0]])
            for line in self.line_list:
                line.set_data(empty_data)
            self.canvas.update()
            return

        # Update each line individually
        for i in range(len(data_list)):
            line_data = np.column_stack((time_points, data_list[i]))
            self.line_list[i].set_data(line_data)

            # Optionally, adjust the y-range of each individual view based on its data
            # This ensures each subplot's Y-axis scales appropriately to its own signal.
            # If you want a fixed range for all, use self._default_y_range instead.
            min_y, max_y = np.min(data_list[i]), np.max(data_list[i])
            # Add a small margin to the range for better visualization
            margin_y = (max_y - min_y) * 0.1 if (max_y - min_y) != 0 else 10
            self.view_list[i].camera.set_range(x=self._default_x_range, y=(min_y - margin_y, max_y + margin_y))

        self.canvas.update()  # Force a redraw of the canvas

    def plot_stuff(self, time_points, data_list):
        self.setup_plots(len(data_list))
        self.update_data(time_points, data_list)