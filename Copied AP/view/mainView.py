from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
from .plotView import VisPyPlotWidget
from .funigifs import FuniWidget


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
        self.showMaximized()  # Enters max screen mode

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        ## sets a kuhl border so we can see the dingsdas
        central_widget.setStyleSheet("border: 1px solid red;")

        main_vertical_layout = QVBoxLayout()
        central_widget.setLayout(main_vertical_layout)

        top_bar = QHBoxLayout()
        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar)
        top_bar_widget.setFixedHeight(150)


        spacer = QSpacerItem(1150, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)

        main_button = QHBoxLayout()
        main_button_widget = QWidget()
        main_button_widget.setLayout(main_button)

        on_off_butt = QPushButton("MAIN SWITCH")
        on_off_butt.setFixedSize(100, 100);
        on_off_butt.setStyleSheet("border-radius: 50%; background-color: lightgreen; border: 5px solid darkgreen;")
        #status_ip_txt = QLabel("Status: CONNECTED \n IP: 127.0.0.1:8080")
        status_ip_txt = FuniWidget()
        status_ip_txt.enable("funiStuff/nyancat.gif")
        status_ip_txt.play()
        status_ip_txt.show()


        main_button.addWidget(on_off_butt)
        main_button.addWidget(status_ip_txt)

        main_vertical_layout.addWidget(top_bar_widget)

        top_bar.addWidget(main_button_widget)

        horizontal_layout = QHBoxLayout()

        control_centre = QVBoxLayout()
        control_centre_widget = QWidget()
        control_centre_widget.setLayout(control_centre)
        control_centre_widget.setFixedWidth(250)

        self.control_button = QPushButton("Start Plotting")
        self.control_button.clicked.connect(self.toggle_plotting)
        self.control_button.setFixedHeight(50)
        button_rms = QPushButton("RMS Signal")
        button_raw = QPushButton("Raw Signal")
        button_filt = QPushButton("Filtered Signal")
        select_channels_label = QLabel("Select Channels")
        select_channels_label.setStyleSheet("border: 2px solid white")
        select_channels_label.setAlignment(Qt.AlignCenter)

        control_centre.addWidget(self.control_button)

        control_centre.addWidget(button_raw)
        control_centre.addWidget(button_filt)
        control_centre.addWidget(button_rms)
        control_centre.addWidget(select_channels_label)

        imp_buttons = QHBoxLayout()

        all = QPushButton("All")
        all.setFixedSize(60, 40)
        all.setStyleSheet("background-color: darkgrey; border: 2px solid black;")
        none = QPushButton("None")
        none.setFixedSize(60, 40)
        none.setStyleSheet("background-color: darkgrey; border: 2px solid black;")

        imp_buttons.addWidget(all)
        imp_buttons.addWidget(none)

        control_centre.addLayout(imp_buttons)

        check_group = QHBoxLayout()

        check_columns_1 = QVBoxLayout()
        check_columns_1_widget = QWidget()
        check_columns_1_widget.setLayout(check_columns_1)
        check_columns_1_widget.setFixedWidth(55)

        check_columns_2 = QVBoxLayout()
        check_columns_2_widget = QWidget()
        check_columns_2_widget.setLayout(check_columns_2)
        check_columns_2_widget.setFixedWidth(55)



        check_list = []
        for i in range(1, 33, 1):
            check_list.append(QCheckBox(str(i)))

        for x in range(int(len(check_list) / 2)):
            check_columns_1.addWidget(check_list[x])


        for y in range(int(len(check_list) / 2), int(len(check_list))):
            check_columns_2.addWidget(check_list[y])

        check_group.addWidget(check_columns_1_widget)
        check_group.addWidget(check_columns_2_widget)
        control_centre.addLayout(check_group)

        horizontal_layout.addWidget(control_centre_widget)
        self.plot_widget = VisPyPlotWidget()
        horizontal_layout.addWidget(self.plot_widget)

        main_vertical_layout.addLayout(horizontal_layout)

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





