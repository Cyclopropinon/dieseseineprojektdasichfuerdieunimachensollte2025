from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
import collections # Import collections for deque
from services.tcp_client import EMGTCPClient

class MainViewModel(QObject):
    """
    ViewModel class that connects the signal data with the visualization for live streaming.

    This class is part of the ViewModel layer in the MVVM architecture. It:
    - Manages incoming live signal data by buffering it in a fixed-size window.
    - Controls the plotting state (start/stop) to animate the scrolling data.
    - Handles the timing of updates, requesting new data chunks from the TCP client.
    - Emits signals to update the view with the current fixed-size data window.

    Signals:
        data_updated: Emitted when new data (time_points, data_values) is available for plotting.
                      The 'time_points' array will always represent a fixed time window (e.g., 0 to 10 seconds),
                      and 'data_values' will contain the corresponding live signal data, ensuring a continuous
                      scrolling display.
    """

    # Signals for the view to connect to.
    # The signal carries two numpy arrays: the time points for the current window
    # and the corresponding data values for that window.
    multi_data_updated = pyqtSignal(np.ndarray, list)

    def __init__(self):
        """
        Initialize the ViewModel with the signal processor and QTimer.

        This constructor sets up:
        - The signal processor (EMGTCPClient) for live data acquisition.
        - Calculates the effective sampling rate based on the client's packet size and ViewModel's update rate.
        - A QTimer for periodic updates, configured for smooth animation (e.g., 30 Hz).
        - The definition of the fixed time window (X-axis range) for the plot.
        - A deque-based buffer to efficiently manage the live incoming data for the display window.
        """
        super().__init__() # Call the base class constructor

        # Initialize the signal processor (EMGTCPClient).
        # This will use the EMGTCPClient class as provided by you, without modifications.
        self.signal_processor = EMGTCPClient()
        # Define the update interval for the plot (e.g., 30 Hz).
        # An update rate of 30 Hz means an interval of approximately 33 milliseconds (1000ms / 30Hz).
        self.update_interval_ms = 33
        # Calculate the effective sampling rate based on the EMGTCPClient's packet size
        # and how frequently the ViewModel requests data.
        # If the ViewModel requests data every `update_interval_ms`, and each packet
        # contains `SAMPLES_PER_PACKET` samples per channel, then the effective
        # sampling rate for the *displayed stream* is:
        # samples_per_packet * (1000ms / update_interval_ms)
        # E.g., 18 samples/packet * (1000ms / 33ms) ~= 18 * 30.3 = 545.4 Hz
        # We'll use 30 as a cleaner approximation if 33ms is the exact interval.
        self.effective_sampling_rate = self.signal_processor.SAMPLES_PER_PACKET * \
                                       int(1000 / self.update_interval_ms)


        # Define the fixed time window for display on the plot (e.g., 10 seconds).
        # This will be the constant duration of the X-axis for the plot.
        self.display_window_seconds = 10

        # Calculate the exact number of samples that fit into the defined display window
        # based on the effective sampling rate.
        self.samples_per_display_window = int(self.display_window_seconds * self.effective_sampling_rate)

        # Create the fixed time array for the X-axis of the plot (e.g., 0 to 10 seconds).
        # Using endpoint=False ensures consistency where the last sample is at (N-1)/Fs.
        self.fixed_time_window = np.linspace(
            0, self.display_window_seconds, self.samples_per_display_window, endpoint=False
        )

        # Use a collections.deque for efficient fixed-size buffering of live data.
        # 'maxlen' ensures the buffer automatically discards older data when new data is added,
        # maintaining a constant size equal to the display window.
        self.data_buffer = collections.deque(maxlen=self.samples_per_display_window)
        # Initialize the buffer with zeros to fill the initial plot display.
        # This prevents an empty plot before the first live data arrives.
        self.data_buffer.extend(np.zeros(self.samples_per_display_window, dtype=np.float32))

        # Flag to control the plotting state (whether the timer is running or stopped).
        self.is_plotting = False

        # Set up the QTimer for periodic updates to the plot.
        self.timer = QTimer(self) # Pass self as parent for proper QObject hierarchy management
        self.timer.setInterval(self.update_interval_ms)

        self.timer.timeout.connect(self.dispatch_method) # Connect timeout signal to the update_data method

        # Attempt to connect to the TCP server immediately when the ViewModel is initialized.
        # This ensures the client is ready to receive data as soon as plotting starts.
        self.signal_processor.connect()
        self.list_of_ch = []
        self.buffers = {}

    def start_plotting(self, current_mode):
        """
        Starts the live plotting simulation.

        This method:
        - Sets the internal plotting state to active.
        - Starts the QTimer, which will periodically call `update_data()`.
        - Calls `update_data()` immediately once to populate the plot without delay,
          ensuring the view is updated as soon as plotting begins.
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

        This method:
        - Sets the internal plotting state to inactive.
        - Stops the QTimer, halting further data emissions and plot updates.
        - Closes the TCP connection cleanly by calling the signal processor's close method.
        """
        if self.is_plotting:
            self.is_plotting = False
            self.data_buffer.clear()
            self.timer.stop()
            ##self.signal_processor.close() # Close TCP connection cleanly

    def update_data(self):
        """
        Updates the data window for the plot by fetching new live data and emitting it.

        This method is called by the QTimer at the specified update frequency. It:
        - Fetches a new data packet (containing data for all channels) from the EMGTCPClient.
        - Extracts data from the first channel (index 0) of the received packet.
        - Appends this new chunk of single-channel data to the right of the internal data buffer (deque).
        - The deque's 'maxlen' property automatically ensures the buffer maintains
          the fixed `samples_per_display_window` size by removing older elements.
        - Converts the deque content to a NumPy array for compatibility with the signal.
        - Emits the `fixed_time_window` and the current content of the data buffer
          via the `data_updated` signal, allowing the view to refresh its plot.
        - If no data is received (e.g., due to connection issues or timeouts),
          it prints a message.
        """
        # Fetch new data packet from the client.
        # This will return a (CHANNELS, SAMPLES_PER_PACKET) NumPy array or None.
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            # Extract data from the first channel (index 0) for plotting.
            # If you need to plot a different channel, change the index here.
            self.new_data_chunk = self.new_packet_all_channels[self.ch - 1, :]
            self.list_of_ch.clear()

            # Extend the data buffer with the new chunk.
            # Due to `maxlen`, older data will be automatically discarded from the left.

            self.data_buffer.extend(self.new_data_chunk)

            # In rare cases (e.g., very slow initial data, or if receive_data
            # returns an unexpectedly short chunk due to network issues), the buffer
            # might be less than `maxlen`. This loop pads with zeros to ensure the
            # buffer always matches `samples_per_display_window` for consistent plotting.
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0) # Pad with zeros (ensure float type for consistency)

            # Convert the deque to a numpy array for emission.
            # Specify dtype for consistency, especially if padding with integers.
            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)
            self.list_of_ch.append(current_data_for_plot)

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()

    def change_channel(self, channel_text):
        self.ch = channel_text

    def receive_list(self, checked_list):
        self.checked_list = list(checked_list)
        self.create_buffers()

    def dispatch_method(self):
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
                Updates the data window for the plot by fetching new live data and emitting it.

                This method is called by the QTimer at the specified update frequency. It:
                - Fetches a new data packet (containing data for all channels) from the EMGTCPClient.
                - Extracts data from the first channel (index 0) of the received packet.
                - Appends this new chunk of single-channel data to the right of the internal data buffer (deque).
                - The deque's 'maxlen' property automatically ensures the buffer maintains
                  the fixed `samples_per_display_window` size by removing older elements.
                - Converts the deque content to a NumPy array for compatibility with the signal.
                - Emits the `fixed_time_window` and the current content of the data buffer
                  via the `data_updated` signal, allowing the view to refresh its plot.
                - If no data is received (e.g., due to connection issues or timeouts),
                  it prints a message.
                """
        # Fetch new data packet from the client.
        # This will return a (CHANNELS, SAMPLES_PER_PACKET) NumPy array or None.
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            # Extract data from the first channel (index 0) for plotting.
            # If you need to plot a different channel, change the index here.
            if len(self.checked_list) == 2:
                self.diff_data = self.new_packet_all_channels[int(self.checked_list[0].text())-1, :] - self.new_packet_all_channels[int(self.checked_list[1].text())-1, :]
                self.list_of_ch.clear()
                print(self.checked_list[0].text(), self.checked_list[1].text())
            # Extend the data buffer with the new chunk.
            # Due to `maxlen`, older data will be automatically discarded from the left.
            self.data_buffer.extend(self.diff_data)

            # In rare cases (e.g., very slow initial data, or if receive_data
            # returns an unexpectedly short chunk due to network issues), the buffer
            # might be less than `maxlen`. This loop pads with zeros to ensure the
            # buffer always matches `samples_per_display_window` for consistent plotting.
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0)  # Pad with zeros (ensure float type for consistency)

            # Convert the deque to a numpy array for emission.
            # Specify dtype for consistency, especially if padding with integers.
            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)
            self.list_of_ch.append(current_data_for_plot)
            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()

    def freq_update_data(self):
        """
                Updates the data window for the plot by fetching new live data and emitting it.

                This method is called by the QTimer at the specified update frequency. It:
                - Fetches a new data packet (containing data for all channels) from the EMGTCPClient.
                - Extracts data from the first channel (index 0) of the received packet.
                - Appends this new chunk of single-channel data to the right of the internal data buffer (deque).
                - The deque's 'maxlen' property automatically ensures the buffer maintains
                  the fixed `samples_per_display_window` size by removing older elements.
                - Converts the deque content to a NumPy array for compatibility with the signal.
                - Emits the `fixed_time_window` and the current content of the data buffer
                  via the `data_updated` signal, allowing the view to refresh its plot.
                - If no data is received (e.g., due to connection issues or timeouts),
                  it prints a message.
                """
        # Fetch new data packet from the client.
        # This will return a (CHANNELS, SAMPLES_PER_PACKET) NumPy array or None.
        self.new_packet_all_channels = self.signal_processor.receive_data()

        if self.new_packet_all_channels is not None:
            # Extract data from the first channel (index 0) for plotting.
            # If you need to plot a different channel, change the index here.
            self.new_data_chunk = self.new_packet_all_channels[self.ch-1, :]
            self.list_of_ch.clear()
            self.data_buffer.extend(self.new_data_chunk)

            # Extend the data buffer with the new chunk.
            # Due to `maxlen`, older data will be automatically discarded from the left.

            # In rare cases (e.g., very slow initial data, or if receive_data
            # returns an unexpectedly short chunk due to network issues), the buffer
            # might be less than `maxlen`. This loop pads with zeros to ensure the
            # buffer always matches `samples_per_display_window` for consistent plotting.
            while len(self.data_buffer) < self.samples_per_display_window:
                self.data_buffer.append(0.0)  # Pad with zeros (ensure float type for consistency)

            # Convert the deque to a numpy array for emission.
            # Specify dtype for consistency, especially if padding with integers.
            current_data_for_plot = np.array(self.data_buffer, dtype=np.float32)


            ###
            yf = np.fft.fft(current_data_for_plot)
            xf = np.fft.fftfreq(self.samples_per_display_window, 1 / self.effective_sampling_rate)

            # Get magnitude of positive frequencies only
            fft_magnitude = 2.0 / self.samples_per_display_window * np.abs(yf[:self.samples_per_display_window // 2])
            frequencies = xf[:self.samples_per_display_window // 2]
            ###
            self.list_of_ch.append(fft_magnitude)

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.multi_data_updated.emit(frequencies, self.list_of_ch)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()

    def multi_update_data(self):
        # Fetch new data packet from the client.
        # This will return a (CHANNELS, SAMPLES_PER_PACKET) NumPy array or None.
        self.new_packet_all_channels = self.signal_processor.receive_data()
        if self.new_packet_all_channels is not None:
            # Extract data from the first channel (index 0) for plotting.
            # If you need to plot a different channel, change the index here.
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

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.multi_data_updated.emit(self.fixed_time_window, self.list_of_ch)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()

    def create_buffers(self):

        active_channel_indices = {int(checkbox_obj.text()) - 1 for checkbox_obj in self.checked_list}

        # 1. Remove buffers for channels that are no longer active
        keys_to_remove = [idx for idx in self.buffers if idx not in active_channel_indices]
        for idx in keys_to_remove:
            del self.buffers[idx]
            print(f"DEBUG: Removed buffer for channel {idx + 1} (no longer active).")

        # 2. Create or reset buffers for currently active channels
        for channel_index in active_channel_indices:
            if channel_index not in self.buffers:
                # Create a new deque if it doesn't exist for this channel
                new_buffer = collections.deque(maxlen=self.samples_per_display_window)
                new_buffer.extend(np.zeros(self.samples_per_display_window, dtype=np.float32))  # Initialize with zeros
                self.buffers[channel_index] = new_buffer
                print(f"DEBUG: Created new buffer for channel {channel_index + 1}.")
            else:
                # If it exists, clear and re-initialize it to ensure it starts fresh
                # (e.g., if re-starting plotting after a pause, or switching modes)
                self.buffers[channel_index].clear()
                self.buffers[channel_index].extend(np.zeros(self.samples_per_display_window, dtype=np.float32))
                print(f"DEBUG: Reset existing buffer for channel {channel_index + 1}.")

        print(f"DEBUG: Buffers now active for channels: {[idx + 1 for idx in sorted(list(active_channel_indices))]}")
