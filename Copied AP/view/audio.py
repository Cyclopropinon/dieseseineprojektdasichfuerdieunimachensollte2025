import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal

class AudioController(QObject):
    """
    Manages audio playback logic for a fixed file path.
    This class acts as a ViewModel/Controller, separating audio concerns
    from the main UI window. It emits signals for UI updates.
    """

    # Define a custom signal to notify the UI about state changes
    # This signal will carry the current QMediaPlayer.State
    audio_state_changed = pyqtSignal(QMediaPlayer.State)
    volume_changed = pyqtSignal(int)

    def __init__(self, audio_file_path: str, parent=None):
        """
        Initializes the AudioController.

        Args:
            audio_file_path (str): The fixed path to the audio file.
            parent (QObject, optional): The parent QObject for this controller.
                                        Defaults to None.
        """
        super().__init__(parent)

        self._audio_file_path = audio_file_path
        self.media_player = QMediaPlayer(self) # Pass self as parent for QMediaPlayer
        self.current_media_content = None

        self.media_player.volumeChanged.connect(self.volume_changed.emit)

        self.media_player.mediaStatusChanged.connect(self._handle_media_status_changed)
        self.media_player.stateChanged.connect(self._handle_state_changed)

        self._load_fixed_audio()

    def _load_fixed_audio(self):
        """
        Internal method to load the audio file from the predefined path.
        Checks if the file exists and sets the media player's content.
        """
        if os.path.exists(self._audio_file_path):
            self.current_media_content = QMediaContent(QUrl.fromLocalFile(self._audio_file_path))
            self.media_player.setMedia(self.current_media_content)
            print(f"AudioController: Loaded audio from: {self._audio_file_path}")
        else:
            print(f"AudioController: Error: Audio file not found at '{self._audio_file_path}'")
            # In a real app, you might emit a specific error signal here.
            self.current_media_content = None # Ensure content is None if file not found

    def toggle_playback(self):
        """
        Toggles between playing and stopping audio.
        This method will be called by your UI button.
        """
        if self.current_media_content is None:
            print("AudioController: No media loaded, cannot toggle playback.")
            return

        if self.media_player.state() == QMediaPlayer.PlayingState and self.media_player.volume() != 0:
            self.media_player.setVolume(0)
            print("AudioController: Stopped playback (Set Volume 0).")

        elif self.media_player.state() == QMediaPlayer.PlayingState and self.media_player.volume() == 0:
            self.media_player.setVolume(100)
            print("AudioController: Set Volume 100.")
        else:
            # If not playing, then play. This covers StoppedState.
            self.media_player.play()
            print("AudioController: Started playing.")

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

    def _handle_media_status_changed(self, status):
        """
        Internal slot to handle changes in the media player's status.
        Triggers stop when media reaches its end.
        """
        if status == QMediaPlayer.EndOfMedia:
            print("AudioController: Playback finished.")
            self.media_player.stop() # Automatically stop when finished

    def _handle_state_changed(self, state):
        """
        Internal slot to handle changes in the media player's state.
        Emits a custom signal for the UI to react to.
        """
        print(f"AudioController: State changed to: {state}")
        self.audio_state_changed.emit(state) # Emit the signal for the UI to consume

    def get_volume(self):
        return self.media_player.volume()

