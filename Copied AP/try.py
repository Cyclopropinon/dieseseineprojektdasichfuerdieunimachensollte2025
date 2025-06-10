import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple PyQt5 Music Player")
        self.setGeometry(100, 100, 400, 200)

        self.media_player = QMediaPlayer()
        self.current_media_content = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Open File Button
        self.open_button = QPushButton("Open Audio File")
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        # Play Button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False) # Initially disabled
        layout.addWidget(self.play_button)

        # Pause Button
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_audio)
        self.pause_button.setEnabled(False) # Initially disabled
        layout.addWidget(self.pause_button)

        # Stop Button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_audio)
        self.stop_button.setEnabled(False) # Initially disabled
        layout.addWidget(self.stop_button)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50) # Default volume
        self.volume_slider.sliderMoved.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        # Connect media player signals
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.stateChanged.connect(self.state_changed)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_path:
            self.current_media_content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.media_player.setMedia(self.current_media_content)
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.media_player.play() # Start playing immediately after opening

    def play_audio(self):
        if self.current_media_content:
            self.media_player.play()

    def pause_audio(self):
        if self.current_media_content:
            self.media_player.pause()

    def stop_audio(self):
        if self.current_media_content:
            self.media_player.stop()

    def set_volume(self, value):
        self.media_player.setVolume(value)

    def media_status_changed(self, status):
        # You can add logic here to handle different media statuses
        # For example, to show a message when the media ends
        if status == QMediaPlayer.EndOfMedia:
            print("Playback finished.")
            self.stop_audio() # Automatically stop when finished

    def state_changed(self, state):
        # Update button states based on media player state
        if state == QMediaPlayer.PlayingState:
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        elif state == QMediaPlayer.PausedState:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else: # StoppedState, BufferingState, etc.
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())