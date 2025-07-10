from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox, QButtonGroup, QFrame
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
        top_bar_widget.setFixedHeight(180)

        self.on_off_butt = QPushButton("MAIN SWITCH")
        self.on_off_butt.setFixedSize(100, 100);
        self.on_off_butt.setStyleSheet("border-radius: 50%; background-color: lightgreen; border: 5px solid darkgreen;")
        self.status_ip_txt = QLabel("Status: DISCONNECTED  Host: ---------  Port: -----")
        self.status_ip_txt.setFixedHeight(30)
        self.status_ip_txt.setAlignment(Qt.AlignCenter)
        self.on_off_butt.clicked.connect(self.start_animations)

        self.gif = QLabel()
        self.gif.setStyleSheet("background-color: black")
        self.gif.setFixedSize(350, 180)

        self.my_audio_button = QPushButton("Mute")
        butt_box = QVBoxLayout()
        butt_box.addWidget(self.on_off_butt)
        butt_box.addWidget(self.my_audio_button)

        spacer = QSpacerItem(400, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        top_bar.addSpacerItem(spacer)
        top_bar.addLayout(butt_box)
        top_bar.addWidget(self.gif)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(0)

        vertical_layout.addWidget(top_bar_widget)

        control_centre = QVBoxLayout()
        control_centre_widget = QWidget()
        control_centre_widget.setLayout(control_centre)

        control_box_1 = QVBoxLayout()
        control_box_1_widget = QWidget()
        control_box_1_widget.setObjectName("control_box_1_widget")
        control_box_1_widget.setStyleSheet("""
            #control_box_1_widget {
                border: 2px solid #000000; /* Black border */
                background-color: #808080; /* Gray background */
            }
            
            #control_box_1_widget QPushButton:hover {
                background-color: #D3D3D3; /* Darker blue on hover */
                border-radius: 5px;        /* Slightly rounded button corners */
                
            }
        """)
        control_box_1_widget.setLayout(control_box_1)
        control_box_1_butt_group = QButtonGroup()
        control_box_1_butt_group.setExclusive(True)
        butt_plot_indi_ch = QPushButton("Plot Individual Channels")
        control_box_1_butt_group.addButton(butt_plot_indi_ch)
        butt_plot_indi_ch.clicked.connect(self.indi_ch)
        self.butt_diff_ch = QPushButton("Differential Channels")
        control_box_1_butt_group.addButton(self.butt_diff_ch)
        self.butt_diff_ch.clicked.connect(self.diff_ch)
        butt_freq_domain_anal = QPushButton("Frequency Domain Analysis")
        control_box_1_butt_group.addButton(butt_freq_domain_anal)
        butt_freq_domain_anal.clicked.connect(self.freq_anal)
        butt_cross_ch_comp = QPushButton("Cross Channel Analysis")
        control_box_1_butt_group.addButton(butt_cross_ch_comp)
        butt_cross_ch_comp.clicked.connect(self.multi_ch)

        self.diff_ch_state = False

        control_box_1.addWidget(self.status_ip_txt)
        control_box_1.addWidget(butt_plot_indi_ch)
        control_box_1.addWidget(self.butt_diff_ch)
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
        select_channels_label.setFixedHeight(50)
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

        self.check_list = []
        self.list_checked = []
        self.button_group = QButtonGroup(self)
        for i in range(1, 33, 1):
            check_box = QCheckBox(str(i))
            self.check_list.append(check_box)
            self.button_group.addButton(check_box)

        for x in range(int(len(self.check_list) / 2)):
            check_columns_1.addWidget(self.check_list[x])

        for y in range(int(len(self.check_list) / 2), int(len(self.check_list))):
            check_columns_2.addWidget(self.check_list[y])

        check_group.addWidget(check_columns_1_widget)
        check_group.addWidget(check_columns_2_widget)
        control_box_3.addWidget(select_channels_label)
        control_box_3.addLayout(check_group)

        clear_selection_button = QPushButton("Clear Selection")
        clear_selection_button.clicked.connect(self.clear_selec)
        control_box_3.addWidget(clear_selection_button)

        control_centre.addWidget(control_box_1_widget)
        control_centre.addWidget(control_box_2_widget)
        control_centre.addWidget(control_box_3_widget)

        ##vertical_layout.addWidget(self.status_ip_txt)
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


        vertical_layout.addLayout(bottom_bar)


        main_horizontal_layout.addWidget(control_centre_widget)
        main_horizontal_layout.addLayout(vertical_layout)

        self.current_mode = ""
        self.is_connected = False




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
            self.view_model.receive_list(self.list_checked)
            self.view_model.start_plotting(self.current_mode)
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
        if not self.is_connected:
            self.status_ip_txt.setText("Status: CONNECTED  Host: localhost  Port: 12345")
            self.is_connected = True
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
            self.view_model.multi_data_updated.connect(self.plot_widget.plot_stuff)

            ##Linking channel buttons
            for k in range(0, 32, 1):
                self.check_list[k].clicked.connect(self.link_channel)
            self.exclusive_state = False
            self.button_group.setExclusive(False)

        elif self.is_connected and self.plot_widget.cleared:
            self.status_ip_txt.setText("Status: DISCONNECTED  Host: ---------  Port: -----")
            #STOP CONNECTION
            self.is_connected = False
            self.view_model.stop_plotting()
            self.clear_selec()
            self.view_model.signal_processor.close()

            #STOP AUDIO
            self.audio_controller.media_player.stop()

            #PLAY CLOSING GIF
            gif_file = "view/cat_goingtosleep.gif"
            self.movie = QMovie(gif_file)
            self.gif.setMovie(self.movie)
            self.movie.start()

            #CLEAR PLOT
            self.plot_widget.clear_plots()

        elif self.is_connected and not self.plot_widget.cleared:
            self.status_ip_txt.setText("Status: DISCONNECTED  Host: ---------  Port: -----")
            #STOP CONNECTION
            self.is_connected = False
            self.view_model.stop_plotting()
            self.clear_selec()
            self.view_model.signal_processor.close()

            #STOP AUDIO
            self.audio_controller.media_player.stop()

            #PLAY CLOSING GIF
            gif_file = "view/cat_sleep_running.gif"
            self.movie = QMovie(gif_file)
            self.gif.setMovie(self.movie)
            self.movie.start()

            #CLEAR PLOT
            self.plot_widget.clear_plots()

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

    def link_channel(self):
        self.sender_button = self.sender()
        button_name = int(self.sender_button.text())
        self.view_model.change_channel(button_name)

        #CLEAR PLOT AND STOP PLOTTING AND CHANGE BUTTON TEXT
        self.plot_widget.clear_plots()
        self.control_button.setText("Start Plotting")
        self.view_model.stop_plotting()
        #START NEW GIF OF STATIONARY CAT
        gif_file = "view/cat stationary.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.movie.setPaused(True)
        self.audio_controller.media_player.pause()

        if self.diff_ch_state:
            self.diff_ch()




    def indi_ch(self):

        # CLEAR PLOT AND STOP PLOTTING AND CHANGE BUTTON TEXT
        self.plot_widget.clear_plots()
        self.control_button.setText("Start Plotting")
        self.view_model.stop_plotting()
        # START NEW GIF OF STATIONARY CAT
        gif_file = "view/cat stationary.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.movie.setPaused(True)
        self.audio_controller.media_player.pause()

        self.button_group.setExclusive(True)
        self.exclusive_state = True
        self.diff_ch_state = False
        self.clear_selec()
        self.current_mode = "indi_ch"

    def clear_selec(self):
        """
        Slot to uncheck all checkboxes in the exclusive button group.
        Temporarily disables exclusivity to allow unchecking, then re-enables it.
        """
        # Temporarily set exclusive to False to allow unchecking multiple buttons
        self.button_group.setExclusive(False)

        # Iterate through all buttons in the group and uncheck them
        for button in self.list_checked:
            button.setChecked(False)
        self.list_checked.clear()
        self.plot_widget.clear_plots()


        # Re-enable exclusivity
        self.button_group.setExclusive(self.exclusive_state)
        print("All checkboxes cleared.")

    def diff_ch(self):

        # CLEAR PLOT AND STOP PLOTTING AND CHANGE BUTTON TEXT
        self.plot_widget.clear_plots()
        self.control_button.setText("Start Plotting")
        self.view_model.stop_plotting()
        # START NEW GIF OF STATIONARY CAT
        gif_file = "view/cat stationary.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.movie.setPaused(True)
        self.audio_controller.media_player.pause()

        self.button_group.setExclusive(False)
        self.exclusive_state = False
        self.current_mode = "diff_ch"

        if not self.diff_ch_state:
            self.clear_selec()

        self.diff_ch_state = True

        if len(self.list_checked) > 2:
            self.sender_button.setChecked(False)
            self.list_checked.remove(self.sender_button)



    def freq_anal(self):

        # CLEAR PLOT AND STOP PLOTTING AND CHANGE BUTTON TEXT
        self.plot_widget.clear_plots()
        self.control_button.setText("Start Plotting")
        self.view_model.stop_plotting()
        # START NEW GIF OF STATIONARY CAT
        gif_file = "view/cat stationary.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.movie.setPaused(True)
        self.audio_controller.media_player.pause()

        self.button_group.setExclusive(True)
        self.exclusive_state = True
        self.diff_ch_state = False
        self.clear_selec()
        self.current_mode = "freq_ch"


    def multi_ch(self):

        # CLEAR PLOT AND STOP PLOTTING AND CHANGE BUTTON TEXT
        self.plot_widget.clear_plots()
        self.control_button.setText("Start Plotting")
        self.view_model.stop_plotting()
        # START NEW GIF OF STATIONARY CAT
        gif_file = "view/cat stationary.gif"
        self.movie = QMovie(gif_file)
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.movie.setPaused(True)
        self.audio_controller.media_player.pause()

        self.button_group.setExclusive(False)
        self.exclusive_state = False
        self.diff_ch_state = False
        self.clear_selec()
        self.current_mode = "multi_ch"



