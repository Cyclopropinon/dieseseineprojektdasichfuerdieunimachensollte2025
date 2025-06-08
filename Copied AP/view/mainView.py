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
        #self.showFullScreen()  # Enters full screen mode

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        ##Layout Initializations
        main_vertical_layout = QVBoxLayout(central_widget)
        horizontal_layout = QHBoxLayout()
        control_centre = QVBoxLayout()
        imp_buttons = QHBoxLayout()
        main_button = QVBoxLayout()
        check_group = QHBoxLayout()
        check_columns_1 = QVBoxLayout()
        check_columns_2 = QVBoxLayout()
        check_columns_3 = QVBoxLayout()
        check_columns_4 = QVBoxLayout()
        top_bar = QHBoxLayout()

        ##Widget Initializations
        self.plot_widget = VisPyPlotWidget()
        button_rms = QPushButton("RMS Signal")
        button_raw = QPushButton("Raw Signal")
        button_filt = QPushButton("Filtered Signal")
        select_channels_label = QLabel("Select Channels")

        check_list = []
        for i in range(1, 33, 1):
            check_list.append(QCheckBox(str(i)))

        all = QPushButton("All")
        none = QPushButton("None")
        on_off_butt = QPushButton("MAIN SWITCH")
        status_txt = QLabel("Status: CONNECTED")
        ip_txt = QLabel("IP: 62.214.70.46")

        spacer = QSpacerItem(1100,100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)

        main_vertical_layout.addLayout(top_bar)
        main_vertical_layout.addLayout(horizontal_layout)
        main_vertical_layout.addWidget(self.plot_widget)
        horizontal_layout.addLayout(control_centre)
        horizontal_layout.addWidget(self.plot_widget)

        top_bar.addLayout(main_button)


        main_button.addWidget(on_off_butt)
        main_button.addWidget(status_txt)
        main_button.addWidget(ip_txt)

        control_centre.addWidget(button_raw)
        control_centre.addWidget(button_filt)
        control_centre.addWidget(button_rms)
        control_centre.addWidget(select_channels_label)
        control_centre.addLayout(imp_buttons)
        control_centre.addLayout(check_group)

        imp_buttons.addWidget(all)
        imp_buttons.addWidget(none)

        check_group.addLayout(check_columns_1)
        check_group.addLayout(check_columns_2)
        check_group.addLayout(check_columns_3)
        check_group.addLayout(check_columns_4)

        for x in range(int(len(check_list) / 4)):
            check_columns_1.addWidget(check_list[x])

        for y in range(int(len(check_list) / 4), int(len(check_list) / 2)):
            check_columns_2.addWidget(check_list[y])

        for z in range(int(len(check_list) / 2), int(len(check_list) * 3 / 4)):
            check_columns_3.addWidget(check_list[z])

        for t in range(int(len(check_list) * 3 / 4), int(len(check_list))):
            check_columns_4.addWidget(check_list[t])

        # Create control button
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




