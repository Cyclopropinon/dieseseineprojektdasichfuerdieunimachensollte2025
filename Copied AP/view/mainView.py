from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
from .plotView import VisPyPlotWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from .credits import CreditsDialog
from PyQt5.QtGui import QMovie
from .audio import AudioController
from viewmodel.mainViewModel import MainViewModel
import sys
import os


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

    def __init__(self):
        """
        Initialize the main window with plot widget and controls.

        Args:
            view_model: The ViewModel that manages the data and plotting state
        """
        super().__init__()

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

        self.gif_box = QVBoxLayout()
        gif_box_widget = QWidget()
        gif_box_widget.setLayout(self.gif_box)

        self.on_off_butt = QPushButton("MAIN SWITCH")
        self.on_off_butt.setFixedSize(100, 100);
        self.on_off_butt.setStyleSheet("border-radius: 50%; background-color: lightgreen; border: 5px solid darkgreen;")
        status_ip_txt = QLabel("Status: CONNECTED \n IP: 62.214.70.46:8080")
        self.on_off_butt.clicked.connect(self.start_animations)


        '''
        
        gif_path = "view/nyancat.gif"
        self.movie = QMovie(gif_path)
        gif = QLabel()
        gif.setMovie(self.movie)
        self.movie.start()
        
        '''

        '''
        cat_waking_up = "view/cat_waking_up.gif"
        self.movie = QMovie(cat_waking_up)
        gif = QLabel()
        gif.setMovie(self.movie)
        self.movie.start()
        '''

        self.gif = QLabel()
        self.gif_box.addWidget(self.gif)
        self.gif_box.addWidget(status_ip_txt)

        '''
        self.audio_file = ""
        self.audio_file_path = os.path.join(os.getcwd(), self.audio_file)
        self.audio_controller = AudioController(self.audio_file_path, parent=self)
        self.init_window_ui()
        self.audio_controller.set_looping(False)

        self.audio_controller.audio_state_changed.connect(self.update_audio_button_ui)
        self.audio_controller.volume_changed.connect(lambda vol: self.update_audio_button_ui(self.audio_controller.get_current_state()))

        self.update_audio_button_ui(self.audio_controller.get_current_state())
        self.my_audio_button.setEnabled(self.audio_controller.is_media_loaded())
        '''
        self.my_audio_button = QPushButton("Mute")
        self.gif_box.addWidget(self.my_audio_button)

        spacer = QSpacerItem(500, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)
        top_bar.addWidget(self.on_off_butt)
        top_bar.addWidget(gif_box_widget)

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
        button_raw.clicked.connect(lambda: self.plot_widget.set_filter(0))
        button_filt.clicked.connect(lambda: self.plot_widget.set_filter("butter"))
        button_rms.clicked.connect(lambda: self.plot_widget.set_filter("rms"))

        bottom_bar = QHBoxLayout()
        self.control_button = QPushButton("Start Plotting")

        self.credits_butt = QPushButton("Credits")
        self.credits_butt.clicked.connect(self.show_credits_dialog)
        export_butt = QPushButton("Export")

        bottom_bar.addWidget(self.control_button)
        bottom_bar.addWidget(self.credits_butt)

        bottom_bar.addWidget(export_butt)

        '''if self.view_model.signal_processor.connected and self.view_model.is_plotting:
            self.plotting_connected()'''


        vertical_layout.addLayout(bottom_bar)

        main_horizontal_layout.addWidget(control_centre_widget)
        main_horizontal_layout.addLayout(vertical_layout)




    def toggle_plotting(self):
        """
        Toggle the plotting state and update button text.
        """
        if self.view_model.is_plotting:
            self.control_button.setText("Start Plotting")
            self.view_model.stop_plotting()
            self.audio_controller.media_player.pause()
            self.movie.setPaused(True)

        else:
            self.control_button.setText("Stop Plotting")
            self.view_model.start_plotting()
            if self.view_model.signal_processor.connected:
                self.plotting_connected()

    def show_credits_dialog(self):
        """
        Slot method to create and show the CreditsDialog when the button is clicked.
        """
        # Create an instance of the CreditsDialog, passing self as the parent
        credits_dialog = CreditsDialog(self)
        # Show the dialog modally (blocks interaction with parent window until closed)
        credits_dialog.exec_()


    def update_audio_button_ui(self, state: QMediaPlayer.State):
        """
        Updates the UI of the audio button based on the AudioController's state.
        This method is a slot connected to the AudioController's audio_state_changed signal.
        """
        if state == QMediaPlayer.PlayingState:
            if self.audio_controller.get_volume() != 0:
                self.my_audio_button.setText("Mute")
            else:
                self.my_audio_button.setText("Unmute")
                self.my_audio_button.setEnabled(True)
            # Only enable if media content was successfully loaded by the controller
            self.my_audio_button.setEnabled(self.audio_controller.is_media_loaded())

    def start_animations(self):
        ## GIF
        gif_file = "view/cat_waking_up.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()

        ##Audio
        self.init_audio("view/cat-meow-6226.mp3")
        self.audio_controller.media_player.play()
        self.audio_controller.set_looping(False)


        ##Connect
        self.view_model = MainViewModel()
        self.control_button.clicked.connect(self.toggle_plotting)
        self.view_model.data_updated.connect(self.plot_widget.update_data)
        self.on_off_butt.setEnabled(False)

    def plotting_connected(self):
        ## GIF
        gif_file = "view/nyancat.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()

        ##Audio
        if self.current_file != "view/Nyan Cat.mp3":
            self.init_audio("view/Nyan Cat.mp3")
            self.audio_controller.media_player.play()
            self.audio_controller.set_looping(True)

        else:
            self.audio_controller.media_player.play()
            self.audio_controller.set_looping(True)


    def init_audio (self, audio_file):
        self.audio_file_path = os.path.join(os.getcwd(), audio_file)
        self.audio_controller = AudioController(self.audio_file_path, parent=self)
        self.my_audio_button.clicked.connect(self.audio_controller.toggle_playback)

        self.audio_controller.audio_state_changed.connect(self.update_audio_button_ui)
        self.audio_controller.volume_changed.connect(
            lambda vol: self.update_audio_button_ui(self.audio_controller.get_current_state()))

        self.update_audio_button_ui(self.audio_controller.get_current_state())
        self.my_audio_button.setEnabled(self.audio_controller.is_media_loaded())
        self.current_file = audio_file
