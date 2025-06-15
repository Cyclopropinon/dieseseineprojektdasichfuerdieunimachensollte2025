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
    data_updated = pyqtSignal(np.ndarray, np.ndarray)

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
        self.timer.timeout.connect(self.update_data) # Connect timeout signal to the update_data method

        # Attempt to connect to the TCP server immediately when the ViewModel is initialized.
        # This ensures the client is ready to receive data as soon as plotting starts.
        self.signal_processor.connect()

    def start_plotting(self, state, current_mode):
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
            self.timer.start()
            if current_mode == "indi_ch":
                self.update_data()
            elif current_mode == "diff_ch":
                self.diff_update_data()
            elif current_mode == "freq_ch":
                self.freq_update_data()
            '''elif current_mode == "multi_ch":
                self.multi_update_data()'''



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
            self.new_data_chunk = self.new_packet_all_channels[self.ch]

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

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.data_updated.emit(self.fixed_time_window, current_data_for_plot)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()

    def change_channel(self, ch):
        self.ch = ch

    def receive_list(self, checked_list):
        self.checked_list = checked_list

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
                self.diff_data = self.new_packet_all_channels[int(self.checked_list[0].text())] - self.new_packet_all_channels[int(self.checked_list[1].text())]
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

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.data_updated.emit(self.fixed_time_window, current_data_for_plot)
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
            self.new_data_chunk = self.new_packet_all_channels[self.ch]

            # Extend the data buffer with the new chunk.
            # Due to `maxlen`, older data will be automatically discarded from the left.
            self.data_buffer.extend(self.new_data_chunk)

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

            # Emit the `fixed_time_window` (constant X-axis) and the `current_data_for_plot`
            # (the continuously updated signal data) to the connected view.
            self.data_updated.emit(frequencies, fft_magnitude)
        else:
            # If `receive_data()` returns None, it indicates a problem (e.g., disconnected, timeout).
            # Print a message to the console. You might want to add more robust error handling
            # or UI feedback here (e.g., displaying a "disconnected" status to the user).
            print("No data received from TCP client. Check connection status or server.")
            # Optionally, you can uncomment the line below to stop plotting automatically
            # if no data is received, assuming a continuous stream is essential for the app.
            # self.stop_plotting()