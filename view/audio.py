import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal

class AudioController(QObject):
    """
    Manages audio playback logic for a fixed file path, now with looping capability.
    """

    audio_state_changed = pyqtSignal(QMediaPlayer.State)
    volume_changed = pyqtSignal(int)
    media_loaded_status_changed = pyqtSignal(bool)


    def __init__(self, audio_file_path: str, parent=None):
        """
        Initializes the AudioController.
        """
        super().__init__(parent)

        self._audio_file_path = audio_file_path
        self.media_player = QMediaPlayer(self)
        self.current_media_content = None

        self._is_looping = False
        self.media_player.mediaStatusChanged.connect(self._handle_media_status_changed)
        self.media_player.stateChanged.connect(self._handle_state_changed)
        self.media_player.volumeChanged.connect(self.volume_changed.emit)
        self.media_player.error.connect(self._handle_error)
        self._load_fixed_audio()

    def _load_fixed_audio(self):
        """
        Internal method to load the audio file from the predefined path.
        """
        if not os.path.exists(self._audio_file_path):
            print(f"AudioController: Error: Audio file not found at '{self._audio_file_path}'")
            self.current_media_content = None
            self.media_loaded_status_changed.emit(False)
            return

        try:
            self.current_media_content = QMediaContent(QUrl.fromLocalFile(self._audio_file_path))
            self.media_player.setMedia(self.current_media_content)
            print(f"AudioController: Loaded audio from: {self._audio_file_path}")
            self.media_loaded_status_changed.emit(True)
        except Exception as e:
            print(f"AudioController: Error loading audio file '{self._audio_file_path}': {e}")
            self.current_media_content = None
            self.media_loaded_status_changed.emit(False)


    def toggle_playback(self):
        """
        Toggles between playing, pausing, muting, and unmuting audio.
        """
        if self.current_media_content is None:
            print("AudioController: No media loaded, cannot toggle playback.")
            return

        current_state = self.media_player.state()
        current_volume = self.media_player.volume()

        if current_state == QMediaPlayer.PlayingState:
            if current_volume != 0:
                self.media_player.setVolume(0)
                print("AudioController: Muted playback.")
            else:
                self.media_player.setVolume(100)
                print("AudioController: Unmuted playback.")

    def get_current_state(self) -> QMediaPlayer.State:
        """
        Returns the current state of the media player.
        """
        return self.media_player.state()

    def is_media_loaded(self) -> bool:
        """
        Checks if media content has been successfully loaded.
        """
        return self.current_media_content is not None

    def _handle_media_status_changed(self, status: QMediaPlayer.MediaStatus):
        """
        Internal slot to handle changes in the media player's status.
        """
        if status == QMediaPlayer.EndOfMedia:
            if self._is_looping:
                self.media_player.setPosition(0)
                self.media_player.play()
                print("AudioController: Audio looped: Playing from start.")
            else:
                print("AudioController: Playback finished (looping disabled).")
                self.media_player.stop()
        elif status == QMediaPlayer.InvalidMedia or status == QMediaPlayer.NoMedia:
            print(f"AudioController: Media error status: {status}")
            self.current_media_content = None
            self.media_loaded_status_changed.emit(False)

    def _handle_state_changed(self, state: QMediaPlayer.State):
        """
        Internal slot to handle changes in the media player's state.
        """
        print(f"AudioController: State changed to: {state}")
        self.audio_state_changed.emit(state) # Emit the signal for the UI to consume

    def _handle_error(self, error: QMediaPlayer.Error):
        """Handles and prints errors reported by QMediaPlayer."""
        print(f"AudioController: QMediaPlayer Error occurred: {error}")
        self.current_media_content = None
        self.media_loaded_status_changed.emit(False)

    def get_volume(self):
        """Returns the current volume (0-100)."""
        return self.media_player.volume()

    def set_volume(self, volume: int):
        """Sets the volume (0-100)."""
        self.media_player.setVolume(max(0, min(100, volume)))

    def set_looping(self, enable: bool):
        """Enables or disables audio looping."""
        self._is_looping = enable
        print(f"AudioController: Looping set to: {enable}")

    def is_looping(self) -> bool:
        """Returns True if looping is currently enabled."""
        return self._is_looping

