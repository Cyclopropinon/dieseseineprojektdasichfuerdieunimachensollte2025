from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from view.plotView import VisPyPlotWidget


class MainView(QMainWindow):
    """
    Main application window that combines the plot widget and controls.

    This class is part of the View layer in the MVVM architecture. It:
    - Creates and manages the main window layout
    - Contains the plot widget and control buttons
    - Connects the ViewModel signals to the View
    - Handles user interactions

    The window provides a simple interface with:
    - A plot widget showing the live signal
    - A button to start/stop the plotting
    """

    def __init__(self, view_model):
        """
        Initialize the main window with plot widget and controls.

        Args:
            view_model: The ViewModel that manages the data and plotting state
        """
        super().__init__()
        self.view_model = view_model

        # Set up the main window
        self.setWindowTitle("deine mudda")
        self.setGeometry(100, 100, 800, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create plot widget
        self.plot_widget = VisPyPlotWidget()
        layout.addWidget(self.plot_widget)

        # Create control button
        self.control_button = QPushButton("Start Plotting")
        self.control_button.clicked.connect(self.toggle_plotting)
        layout.addWidget(self.control_button)

        # Connect view model signals
        self.view_model.data_updated.connect(self.plot_widget.update_data)

    def toggle_plotting(self):
        """
        Toggle the plotting state and update button text.
        """
        if self.view_model.is_plotting:
            self.control_button.setText("Start Plotting")
            self.view_model.stop_plotting()
        else:
            self.control_button.setText("Stop Plotting")
            self.view_model.start_plotting()