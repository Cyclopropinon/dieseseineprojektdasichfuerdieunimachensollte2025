from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox, QButtonGroup, QFrame
from PyQt5.QtCore import Qt
from .plotView import VisPyPlotWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from .credits import CreditsDialog
from PyQt5.QtGui import QMovie, QFontDatabase, QFont
from .audio import AudioController
from viewmodel.mainViewModel import MainViewModel
import subprocess
import sys
import os


class MainView(QMainWindow):
    """
    Main application window that combines the plot widget and controls.
    """

    def __init__(self):
        """
        Initialize the main window with plot widget and controls.
        """
        super().__init__()

        self.setWindowTitle("VeryCreativeProjectName")
        self.setGeometry(0, 0, 800, 600)
        self.showMaximized()
        ##self.showFullScreen() #Enters Full Screen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""QMainWindow {background-color: #323232; /* Dark Grey */}""")

        ## sets a kuhl border so we can see the dingsdas
        ##central_widget.setStyleSheet("border: 1px solid red;")

        main_horizontal_layout = QHBoxLayout()
        central_widget.setLayout(main_horizontal_layout)

        top_bar = QHBoxLayout()
        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar)
        top_bar_widget.setFixedHeight(180)

        self.on_off_butt = QPushButton("Start")
        self.on_off_butt.setFixedSize(100, 100);
        self.on_off_butt.setObjectName("startButton")
        self.on_off_butt.setStyleSheet("""
                    #startButton {background-color: #4CAF50;color: white;border-radius: 50px;font-size: 20px;font-weight: bold;border: 3px solid #2e6930;}
                    #startButton:hover {background-color: #45a049;}
                """)


        self.status_ip_txt = QLabel("Status: DISCONNECTED  Host: ---------  Port: -----")
        self.status_ip_txt.setStyleSheet("border: 1px solid #ffffff ; background-color: #404040; border-radius: 5px; color: white; font-weight: bold;")
        self.status_ip_txt.setFixedHeight(40)
        self.status_ip_txt.setAlignment(Qt.AlignCenter)
        self.on_off_butt.clicked.connect(self.start_animations)

        self.gif = QLabel()
        self.gif.setStyleSheet("background-color: black")
        self.gif.setFixedSize(350, 180)

        self.my_audio_button = QPushButton("Mute")
        self.my_audio_button.setObjectName("my_audio_button")
        self.my_audio_button.setStyleSheet("""
                                    #my_audio_button {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
                                    #my_audio_button:hover {background-color: #bcbcbc; border-radius: 5px;}
                                    #my_audio_button:pressed {background-color: #7f7f7f;}
                                    """)

        butt_box = QVBoxLayout()
        butt_box.addWidget(self.on_off_butt)
        butt_box.addWidget(self.my_audio_button)

        Werbung = QLabel("Hier könnte Ihre Werbung stehen")
        Werbung.setStyleSheet("color: white;")
        Werbung.setFixedSize(400, 100)
        Werbung.setAlignment(Qt.AlignCenter)
        Werbung.setWordWrap(True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_filename = "werbung.ttf"
        programmatic_font_path = os.path.join(script_dir, font_filename)
        font_id = QFontDatabase.addApplicationFont(programmatic_font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        fontt = QFont(font_family, 30)
        fontt.setBold(True)
        Werbung.setFont(fontt)

        top_bar.addWidget(Werbung)
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
            #control_box_1_widget {border: 3px solid #474747; background-color: #5b5b5b;}
            #control_box_1_widget QPushButton {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
            #control_box_1_widget QPushButton:hover {background-color: #bcbcbc; border-radius: 5px;}
            #control_box_1_widget QPushButton:pressed {background-color: #7f7f7f;}
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

        control_box_2_widget.setObjectName("control_box_2_widget")
        control_box_2_widget.setStyleSheet("""
                    #control_box_2_widget {border: 3px solid #474747; background-color: #5b5b5b;}
                    #control_box_2_widget QPushButton {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
                    #control_box_2_widget QPushButton:hover {background-color: #bcbcbc; border-radius: 5px;}
                    #control_box_2_widget QPushButton:pressed {background-color: #7f7f7f;}
                """)

        control_box_3 = QVBoxLayout()
        control_box_3_widget = QWidget()
        control_box_3_widget.setLayout(control_box_3)

        control_box_3_widget.setObjectName("control_box_3_widget")
        control_box_3_widget.setStyleSheet("""
                    #control_box_3_widget {border: 3px solid #474747; background-color: #5b5b5b;}
                    #control_box_3_widget QPushButton {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
                    #control_box_3_widget QPushButton:hover {background-color: #bcbcbc; border-radius: 5px;}
                    #control_box_3_widget QPushButton:pressed {background-color: #7f7f7f;}
                    #control_box_3_widget QCheckBox {color: white; font-weight: bold;}
                    """)

        select_channels_label = QLabel("Select Channels")
        select_channels_label.setFixedHeight(40)
        select_channels_label.setStyleSheet("border: 1px solid #ffffff ; background-color: #404040; border-radius: 5px; color: white; font-weight: bold;")
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
        control_centre.addSpacing(10)
        control_centre.addWidget(control_box_2_widget)
        control_centre.addSpacing(10)
        control_centre.addWidget(control_box_3_widget)

        self.plot_widget = VisPyPlotWidget()
        vertical_layout.addWidget(self.plot_widget)
        button_raw.clicked.connect(lambda: self.plot_widget.set_filter(0))
        button_filt.clicked.connect(lambda: self.plot_widget.set_filter("butter"))
        button_rms.clicked.connect(lambda: self.plot_widget.set_filter("rms"))

        bottom_bar = QHBoxLayout()
        self.control_button = QPushButton("Start Plotting")
        self.control_button.setObjectName("control_button")
        self.control_button.setStyleSheet("""
                            #control_button {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
                            #control_button:hover {background-color: #bcbcbc; border-radius: 5px;}
                            #control_button:pressed {background-color: #7f7f7f;}
                            """)

        self.credits_butt = QPushButton("Credits")
        self.credits_butt.setObjectName("credits_butt")
        self.credits_butt.setStyleSheet("""
                                    #credits_butt {background-color: #9f9f9f; border-radius: 5px; padding: 3px 6px; color: white; font-weight: bold;}
                                    #credits_butt:hover {background-color: #bcbcbc; border-radius: 5px;}
                                    #credits_butt:pressed {background-color: #7f7f7f;}
                                    """)
        self.credits_butt.clicked.connect(self.show_credits_dialog)

        bottom_bar.addWidget(self.control_button)
        bottom_bar.addSpacing(5)
        bottom_bar.addWidget(self.credits_butt)

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
        method to create and show the CreditsDialog when the button is clicked.
        """

        credits_dialog = CreditsDialog(self)
        credits_dialog.exec_()


    def update_audio_button_ui(self, state: QMediaPlayer.State):
        """
        Updates the UI of the audio button based on the AudioController's state.
        """
        if state == QMediaPlayer.PlayingState:
            if self.audio_controller.get_volume() != 0:
                self.my_audio_button.setText("Mute")
            else:
                self.my_audio_button.setText("Unmute")
                self.my_audio_button.setEnabled(True)
            self.my_audio_button.setEnabled(self.audio_controller.is_media_loaded())

    def start_animations(self):
        """
        is called when the start button is clicked.
        """
        ## GIF
        if not self.is_connected:
            self.on_off_butt.setStyleSheet("""
                                            #startButton {background-color: #e21f1f; color: white;border-radius: 50px;font-size: 20px;font-weight: bold;border: 3px solid #881313;}
                                            #startButton:hover {background-color: #c91b1b;}
                                        """)
            self.on_off_butt.setText("Stop")
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
            self.on_off_butt.setStyleSheet("""
                                #startButton {background-color: #4CAF50;color: white;border-radius: 50px;font-size: 20px;font-weight: bold;border: 3px solid #2e6930;}
                                #startButton:hover {background-color: #45a049;}
                            """)
            self.on_off_butt.setText("Start")
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
            self.on_off_butt.setStyleSheet("""
                                            #startButton {background-color: #4CAF50;color: white;border-radius: 50px;font-size: 20px;font-weight: bold;border: 3px solid #2e6930;}
                                            #startButton:hover {background-color: #45a049;}
                                        """)
            self.on_off_butt.setText("Start")
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
        """
        called when the client is connected to the server and the plotting is active
        """
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
        """
        audio initialization
        """
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
        """
        links the checkboxes to the channels. called when the checkboxes are clicked
        """
        self.sender_button = self.sender()
        button_name = int(self.sender_button.text())
        self.view_model.change_channel(button_name)

        if self.sender_button in self.list_checked:
            self.list_checked.remove(self.sender_button)
        else:
            self.list_checked.append(self.sender_button)

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

    def show_error(self, message):
        subprocess.run(['zenity', '--error', '--text', message])


    def indi_ch(self):
        """
        runs when the plot individial channels button is clicked
        """
        try:
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
        except Exception as e:
            self.show_error(f"Stoopit [nice person], you forgor to switsch on the main button!")

    def clear_selec(self):
        """
        uncheck all checkboxes in the exclusive button group.
        """
        try:
            self.button_group.setExclusive(False)
            for button in self.list_checked:
                button.setChecked(False)
            self.list_checked.clear()
            self.plot_widget.clear_plots()
            self.button_group.setExclusive(self.exclusive_state)
            print("All checkboxes cleared.")
        except Exception as e:
            self.show_error(f"Stoopit [nice person], you forgor to switsch on the main button!")


    def diff_ch(self):
        """
        runs when the differential channels button is clicked
        """
        try:
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

        except Exception as e:
            self.show_error(f"Stoopit [nice person], you forgor to switsch on the main button!")


    def freq_anal(self):
        """
        runs when the frequency domain analysis button is clicked
        """
        try:
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
        except Exception as e:
            self.show_error(f"Stoopit [nice person], you forgor to switsch on the main button!")

    def multi_ch(self):
        """
        runs when the multiple channel plotting button is clicked
        """
        try:
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
        except Exception as e:
            self.show_error(f"Stoopit [nice person], you forgor to switsch on the main button!")




