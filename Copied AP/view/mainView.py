from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox
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
        self.showMaximized()  # Enters max screen mode

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        ## sets a kuhl border so we can see the dingsdas
        ##central_widget.setStyleSheet("border: 1px solid red;")

        main_horizontal_layout = QHBoxLayout()
        central_widget.setLayout(main_horizontal_layout)

        top_bar = QHBoxLayout()
        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar)
        top_bar_widget.setFixedHeight(150)




        gif_button = QVBoxLayout()
        gif_button_widget = QWidget()
        gif_button_widget.setLayout(gif_button)

        on_off_butt = QPushButton("MAIN SWITCH")
        on_off_butt.setFixedSize(100, 100);
        on_off_butt.setStyleSheet("border-radius: 50%; background-color: lightgreen; border: 5px solid darkgreen;")
        status_ip_txt = QLabel("Status: CONNECTED \n IP: 62.214.70.46:8080"  )

        gif = QWidget()
        gif_button.addWidget(gif)
        gif_button.addWidget(status_ip_txt)

        spacer = QSpacerItem(500, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)
        top_bar.addWidget(on_off_butt)
        top_bar.addWidget(gif_button_widget)

        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(top_bar_widget)

        control_centre = QVBoxLayout()
        control_centre_widget = QWidget()
        control_centre_widget.setLayout(control_centre)

        control_box_1 = QVBoxLayout()
        control_box_1_widget = QWidget()
        control_box_1_widget.setLayout(control_box_1)
        butt_plot_indi_ch = QPushButton("Plot Individual Channels")
        butt_diff_ch = QPushButton("Differential Channels")
        butt_freq_domain_anal = QPushButton("Frequency Domain Analysis")
        butt_cross_ch_comp = QPushButton("Cross Channel Analysis")

        control_box_1.addWidget(butt_plot_indi_ch)
        control_box_1.addWidget(butt_diff_ch)
        control_box_1.addWidget(butt_freq_domain_anal)
        control_box_1.addWidget(butt_cross_ch_comp)

        control_box_2 = QVBoxLayout()
        control_box_2_widget = QWidget()
        control_box_2_widget.setLayout(control_box_2)
        button_rms = QPushButton("RMS Signal")
        button_raw = QPushButton("Raw Signal")
        button_filt = QPushButton("Filtered Signal")

        control_box_2.addWidget(button_raw)
        control_box_2.addWidget(button_filt)
        control_box_2.addWidget(button_rms)

        control_box_3 = QVBoxLayout()
        control_box_3_widget = QWidget()
        control_box_3_widget.setLayout(control_box_3)
        select_channels_label = QLabel("Select Channels")
        select_channels_label.setStyleSheet("border: 2px solid white")
        select_channels_label.setAlignment(Qt.AlignCenter)

        check_group = QHBoxLayout()

        check_columns_1 = QVBoxLayout()
        check_columns_1_widget = QWidget()
        check_columns_1_widget.setLayout(check_columns_1)
        check_columns_1_widget.setFixedWidth(60)

        check_columns_2 = QVBoxLayout()
        check_columns_2_widget = QWidget()
        check_columns_2_widget.setLayout(check_columns_2)
        check_columns_2_widget.setFixedWidth(60)

        check_list = []
        for i in range(1, 33, 1):
            check_list.append(QCheckBox(str(i)))

        for x in range(int(len(check_list) / 2)):
            check_columns_1.addWidget(check_list[x])

        for y in range(int(len(check_list) / 2), int(len(check_list))):
            check_columns_2.addWidget(check_list[y])

        check_group.addWidget(check_columns_1_widget)
        check_group.addWidget(check_columns_2_widget)
        control_box_3.addWidget(select_channels_label)
        control_box_3.addLayout(check_group)

        clear_selection_button = QPushButton("Clear Selection")
        control_box_3.addWidget(clear_selection_button)

        control_centre.addWidget(control_box_1_widget)
        control_centre.addWidget(control_box_2_widget)
        control_centre.addWidget(control_box_3_widget)

        self.plot_widget = VisPyPlotWidget()
        vertical_layout.addWidget(self.plot_widget)

        bottom_bar = QHBoxLayout()
        self.control_button = QPushButton("Start Plotting")
        self.control_button.clicked.connect(self.toggle_plotting)
        credits_butt = QPushButton("Credits")
        export_butt = QPushButton("Export")

        bottom_bar.addWidget(self.control_button)
        bottom_bar.addWidget(credits_butt)
        bottom_bar.addWidget(export_butt)

        vertical_layout.addLayout(bottom_bar)

        main_horizontal_layout.addWidget(control_centre_widget)
        main_horizontal_layout.addLayout(vertical_layout)


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





