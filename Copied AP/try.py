from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
from .plotView import VisPyPlotWidget

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
        self.setWindowTitle("VeryCreativeProjectName")
        self.setGeometry(0, 0, 800, 600)
        self.showFullScreen()  # Enters full screen mode

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_vertical_layout = QVBoxLayout()
        central_widget.setLayout(main_vertical_layout)

        top_bar_widget = QWidget()
        top_bar = QHBoxLayout()
        top_bar_widget.setLayout(top_bar)
        top_bar_widget.setFixedHeight(150)

        spacer = QSpacerItem(1100, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)

        main_button_widget = QWidget()
        main_button = QVBoxLayout()
        main_button_widget.setLayout(main_button)

        on_off_butt = QPushButton("MAIN SWITCH")
        status_txt = QLabel("Status: CONNECTED")
        ip_txt = QLabel("IP: 62.214.70.46")

        main_button.addWidget(on_off_butt)
        main_button.addWidget(status_txt)
        main_button.addWidget(ip_txt)

        top_bar.addWidget(main_button_widget)

        main_vertical_layout.addWidget(top_bar_widget)

        horizontal_layout = QHBoxLayout()
        horizontal_layout_widget = QWidget()
        horizontal_layout_widget.setLayout(horizontal_layout)

        control_centre = QVBoxLayout()
        control_centre_widget = QWidget()
        control_centre_widget.setLayout(control_centre)

        button_rms = QPushButton("RMS Signal")
        button_raw = QPushButton("Raw Signal")
        button_filt = QPushButton("Filtered Signal")
        select_channels_label = QLabel("Select Channels")

        control_centre.addWidget(button_raw)
        control_centre.addWidget(button_filt)
        control_centre.addWidget(button_rms)
        control_centre.addWidget(select_channels_label)

        imp_buttons = QVBoxLayout()
        imp_buttons_widget = QWidget()
        imp_buttons_widget.setLayout(imp_buttons)

        all = QPushButton("All")
        none = QPushButton("None")

        imp_buttons.addWidget(all)
        imp_buttons.addWidget(none)

        control_centre.addWidget(imp_buttons_widget)

        check_group = QHBoxLayout()
        check_group_widget = QWidget()
        check_group_widget.setLayout(check_group)

        check_columns_1 = QVBoxLayout()
        check_columns_1_widget = QWidget()
        check_columns_1_widget.setLayout(check_columns_1)

        check_columns_2 = QVBoxLayout()
        check_columns_2_widget = QWidget()
        check_columns_2_widget.setLayout(check_columns_2)

        check_list = []
        for i in range(1, 33, 1):
            check_list.append(QCheckBox(str(i)))

        for x in range(int(len(check_list) / 2)):
            check_columns_1.addWidget(check_list[x])

        for y in range(int(len(check_list) / 2), int(len(check_list))):
            check_columns_2.addWidget(check_list[y])

        check_group.addWidget(check_columns_1)
        check_group.addWidget(check_columns_2)
        control_centre.addWidget(check_group)

        horizontal_layout.addWidget(control_centre_widget)
        horizontal_layout.addWidget(self.plot_widget)

        self.control_button = QPushButton("Start Plotting")
        self.control_button.clicked.connect(self.toggle_plotting)
        main_vertical_layout.addWidget(self.control_button)

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





