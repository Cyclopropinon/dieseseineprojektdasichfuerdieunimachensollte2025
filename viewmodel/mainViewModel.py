from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
import collections # Import collections for deque
from services.tcp_client import EMGTCPClient

class MainViewModel(QObject):
    """
    ViewModel class that connects the signal data with the visualization for live streaming.

    It:
    - Manages incoming live signal data by buffering it in a fixed-size window.
    - Controls the plotting state (start/stop) to animate the scrolling data.
    - Handles the timing of updates, requesting new data chunks from the TCP client.
    - Emits signals to update the view with the current fixed-size data window.

    """

    multi_data_updated = pyqtSignal(np.ndarray, list)

    def __init__(self):
        """
        Initialize the ViewModel with the signal processor and QTimer.
        """
        super().__init__()


        self.signal_processor = EMGTCPClient()
        self.update_interval_ms = 33
        self.effective_sampling_rate = self.signal_processor.SAMPLES_PER_PACKET * \
                                       int(1000 / self.update_interval_ms)
        self.display_window_seconds = 10
        self.samples_per_display_window = int(self.display_window_seconds * self.effective_sampling_rate)
        self.fixed_time_window = np.linspace(
            0, self.display_window_seconds, self.samples_per_display_window, endpoint=False
        )


        self.data_buffer = collections.deque(maxlen=self.samples_per_display_window)
        self.data_buffer.extend(np.zeros(self.samples_per_display_window, dtype=np.float32))

        self.is_plotting = False

        self.timer = QTimer(self)
        self.timer.setInterval(self.update_interval_ms)

        self.timer.timeout.connect(self.dispatch_method)

        self.signal_processor.connect()
        self.list_of_ch = []
        self.buffers = {}

    def start_plotting(self, current_mode):
        """
        Starts the live plotting simulation.
        """
        if not self.is_plotting:
            self.is_plotting = True
            self.data_buffer.clear()
            self.timer.start()
            self.current_mode = current_mode
            self.dispatch_method()


    def stop_plotting(self):
        """
        Stops the live plotting simulation.
        """
        if self.is_plotting:
            self.is_plotting = False
            self.data_buffer.clear()
            self.timer.stop()

    def update_data(self):
        """
        Updates the data window for the plot by fetching new live data and emitting it.
        """
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            self.new_data_chunk = self.new_packet_all_channels[self.ch - 1, :]
            self.list_of_ch.clear()
            self.data_buffer.extend(self.new_data_chunk)
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0)

            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)
            self.list_of_ch.append(current_data_for_plot)

            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            print("No data received from TCP client. Check connection status or server.")

    def change_channel(self, channel_text):
        self.ch = channel_text

    def receive_list(self, checked_list):
        """
        Receives the list of checked channel checkboxes
        """
        self.checked_list = list(checked_list)
        self.create_buffers()

    def dispatch_method(self):
        """
        Decides which method to reun based on the feature selected by user
        """
        if self.current_mode == "indi_ch":
            self.update_data()
        elif self.current_mode == "diff_ch":
            self.diff_update_data()
        elif self.current_mode == "freq_ch":
            self.freq_update_data()
        elif self.current_mode == "multi_ch":
            self.multi_update_data()
        else:
            print("current mode not defined")

    def diff_update_data(self):
        """
            Updates the data window for the plot by fetching new live data and emits the differential data.
        """
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            if len(self.checked_list) == 2:
                self.diff_data = self.new_packet_all_channels[int(self.checked_list[0].text())-1, :] - self.new_packet_all_channels[int(self.checked_list[1].text())-1, :]
                self.list_of_ch.clear()
                print(self.checked_list[0].text(), self.checked_list[1].text())
            self.data_buffer.extend(self.diff_data)
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0)

            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)
            self.list_of_ch.append(current_data_for_plot)
            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            print("No data received from TCP client. Check connection status or server.")

    def freq_update_data(self):
        """
            Updates the data window for the plot by fetching new live data and emitting the freq magnitude data.
        """
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            self.new_data_chunk = self.new_packet_all_channels[self.ch-1, :]
            self.list_of_ch.clear()
            self.data_buffer.extend(self.new_data_chunk)
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0)
            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)

            yf = np.fft.fft(current_data_for_plot)
            xf = np.fft.fftfreq(self.samples_per_display_window, 1 / self.effective_sampling_rate)

            fft_magnitude = 2.0 / self.samples_per_display_window * np.abs(yf[:self.samples_per_display_window // 2])
            frequencies = xf[:self.samples_per_display_window // 2]
            self.list_of_ch.append(fft_magnitude)
            self.multi_data_updated.emit(frequencies, self.list_of_ch)
        else:
            print("No data received from TCP client. Check connection status or server.")

    def multi_update_data(self):
        """
        Updates the data window for the plot by fetching new live data and emitting all the data for channels that are selected.
        """
        self.new_packet_all_channels = self.signal_processor.receive_data()
        if self.new_packet_all_channels is not None:
            self.list_of_ch.clear()
            for i in self.checked_list:
                channel_index = int(i.text()) - 1
                self.new_data_chunk = self.new_packet_all_channels[channel_index, :]
                current_channel_buffer = self.buffers[channel_index]
                current_channel_buffer.extend(self.new_data_chunk)
                while len(current_channel_buffer) < self.samples_per_display_window:
                    current_channel_buffer.append(0.0)

                current_data_for_plot = np.array(current_channel_buffer, dtype=np.float32)
                self.list_of_ch.append(current_data_for_plot)

            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            print("No data received from TCP client. Check connection status or server.")

    def create_buffers(self):
        """
        Creates buffers for all the channels selected
        """
        active_channel_indices = {int(checkbox_obj.text()) - 1 for checkbox_obj in self.checked_list}

        keys_to_remove = [idx for idx in self.buffers if idx not in active_channel_indices]
        for idx in keys_to_remove:
            del self.buffers[idx]
            print(f"DEBUG: Removed buffer for channel {idx + 1} (no longer active).")

        for channel_index in active_channel_indices:
            if channel_index not in self.buffers:
                new_buffer = collections.deque(maxlen=self.samples_per_display_window)
                new_buffer.extend(np.zeros(self.samples_per_display_window, dtype=np.float32))
                self.buffers[channel_index] = new_buffer
                print(f"DEBUG: Created new buffer for channel {channel_index + 1}.")
            else:
                self.buffers[channel_index].clear()
                self.buffers[channel_index].extend(np.zeros(self.samples_per_display_window, dtype=np.float32))
                print(f"DEBUG: Reset existing buffer for channel {channel_index + 1}.")

        print(f"DEBUG: Buffers now active for channels: {[idx + 1 for idx in sorted(list(active_channel_indices))]}")
