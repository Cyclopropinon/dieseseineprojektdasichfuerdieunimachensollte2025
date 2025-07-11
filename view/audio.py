import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal

class AudioController(QObject):
    """
    Manages audio playback logic for a fixed file path, now with looping capability.
    This class acts as a ViewModel/Controller, separating audio concerns
    from the main UI window. It emits signals for UI updates.
    """

    # Define custom signals to notify the UI about changes
    audio_state_changed = pyqtSignal(QMediaPlayer.State)
    volume_changed = pyqtSignal(int)
    # New signal to indicate if media was successfully loaded or not
    media_loaded_status_changed = pyqtSignal(bool)


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

        # --- New looping-related attribute ---
        self._is_looping = False # Flag to control whether the audio should loop

        # Connect QMediaPlayer signals to controller's internal handlers
        self.media_player.mediaStatusChanged.connect(self._handle_media_status_changed)
        self.media_player.stateChanged.connect(self._handle_state_changed)
        self.media_player.volumeChanged.connect(self.volume_changed.emit) # Emit volume_changed signal directly
        self.media_player.error.connect(self._handle_error) # Basic error handling

        self._load_fixed_audio()

    def _load_fixed_audio(self):
        """
        Internal method to load the audio file from the predefined path.
        Checks if the file exists and sets the media player's content.
        Emits media_loaded_status_changed based on success/failure.
        """
        if not os.path.exists(self._audio_file_path):
            print(f"AudioController: Error: Audio file not found at '{self._audio_file_path}'")
            self.current_media_content = None
            self.media_loaded_status_changed.emit(False) # Notify UI of failure
            return

        try:
            self.current_media_content = QMediaContent(QUrl.fromLocalFile(self._audio_file_path))
            self.media_player.setMedia(self.current_media_content)
            print(f"AudioController: Loaded audio from: {self._audio_file_path}")
            self.media_loaded_status_changed.emit(True) # Notify UI of success
        except Exception as e:
            print(f"AudioController: Error loading audio file '{self._audio_file_path}': {e}")
            self.current_media_content = None
            self.media_loaded_status_changed.emit(False) # Notify UI of failure


    def toggle_playback(self):
        """
        Toggles between playing, pausing, muting, and unmuting audio.
        This method will be called by your UI button.
        """
        if self.current_media_content is None:
            print("AudioController: No media loaded, cannot toggle playback.")
            return

        current_state = self.media_player.state()
        current_volume = self.media_player.volume()

        if current_state == QMediaPlayer.PlayingState:
            if current_volume != 0:
                # If currently playing and not muted, mute it
                self.media_player.setVolume(0)
                print("AudioController: Muted playback.")
            else:
                # If currently playing but muted, unmute (e.g., to 100%)
                self.media_player.setVolume(100) # Unmute to full volume
                print("AudioController: Unmuted playback.")
        '''elif current_state == QMediaPlayer.PausedState:
            self.media_player.play()
            print("AudioController: Resumed playing.")
        else: # Covers QMediaPlayer.StoppedState and others
            self.media_player.play()
            print("AudioController: Started playing.")'''

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
        THIS IS THE CORE LOOPING FUNCTION.
        When the audio reaches its end (EndOfMedia) and looping is enabled,
        it resets the position and plays it again.
        """
        if status == QMediaPlayer.EndOfMedia:
            if self._is_looping:
                self.media_player.setPosition(0) # Reset to beginning
                self.media_player.play()         # Play again
                print("AudioController: Audio looped: Playing from start.")
            else:
                print("AudioController: Playback finished (looping disabled).")
                self.media_player.stop() # Automatically stop when finished if not looping
        elif status == QMediaPlayer.InvalidMedia or status == QMediaPlayer.NoMedia:
            print(f"AudioController: Media error status: {status}")
            self.current_media_content = None # Mark as not loaded on error
            self.media_loaded_status_changed.emit(False) # Notify UI of failure

    def _handle_state_changed(self, state: QMediaPlayer.State):
        """
        Internal slot to handle changes in the media player's state.
        Emits a custom signal for the UI to react to.
        """
        print(f"AudioController: State changed to: {state}")
        self.audio_state_changed.emit(state) # Emit the signal for the UI to consume

    def _handle_error(self, error: QMediaPlayer.Error):
        """Handles and prints errors reported by QMediaPlayer."""
        # Note: error_string is often implicitly available or handled by the signal itself in newer PyQt5
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

