from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from services.signal_processor import SignalProcessor

class MainViewModel(QObject):
    """
    ViewModel class that connects the signal data with the visualization.
    
    This class is part of the ViewModel layer in the MVVM architecture. It:
    - Manages the signal data and its updates
    - Controls the plotting state (start/stop)
    - Handles the timing of updates
    - Emits signals to update the view
    
    Signals:
        data_updated: Emitted when new data is available for plotting
    """
    
    # Signals for the view to connect to
    data_updated = pyqtSignal(np.ndarray, np.ndarray)  # time, data
    
    def __init__(self):
        """
        Initialize the ViewModel with signal processor and timer.
        
        Sets up:
        - Signal processor with 10s window and 2048 Hz sampling
        - Timer for 30 Hz updates
        - Initial data generation
        - Fixed time window for display
        """
        super().__init__()
        self.signal_processor = SignalProcessor(window_size=10, sampling_rate=2048)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        
        # Initialize data
        self.time_points, self.raw_data = self.signal_processor.generate_test_signal(duration=60)
        self.current_index = 0
        self.is_plotting = False
        
        # Create fixed time window (0 to 10 seconds)
        self.fixed_time_window = np.linspace(0, 10, self.signal_processor.points_per_window)
        
        # Set update interval to 30 Hz
        self.timer.setInterval(33)  # 1000ms/30Hz ≈ 33ms
        
    def start_plotting(self):
        """
        Start the live plotting.
        
        This method:
        - Sets the plotting state to active
        - Starts the update timer
        """
        if not self.is_plotting:
            self.is_plotting = True
            self.timer.start()
            
    def stop_plotting(self):
        """
        Stop the live plotting.
        
        This method:
        - Sets the plotting state to inactive
        - Stops the update timer
        """
        if self.is_plotting:
            self.is_plotting = False
            self.timer.stop()
            
    def update_data(self):
        """
        Update the data window and emit new data.
        
        This method is called by the timer at 30 Hz. It:
        - Gets the current window of data
        - Pads with zeros if needed
        - Emits the new data for plotting
        - Updates the current index
        - Resets if we reach the end
        """
        window_size = self.signal_processor.points_per_window
        end_idx = min(self.current_index + window_size, len(self.time_points))
        
        # Get the current window of data
        data_window = self.raw_data[self.current_index:end_idx]
        
        # If we don't have enough data to fill the window, pad with zeros
        if len(data_window) < window_size:
            data_window = np.pad(data_window, (0, window_size - len(data_window)))
        
        # Emit the fixed time window and the shifted data
        self.data_updated.emit(self.fixed_time_window, data_window)
        
        # Update the current index (move by 1/30th of a second worth of samples)
        self.current_index += self.signal_processor.sampling_rate // 30
        
        # Reset if we reach the end
        if self.current_index >= len(self.time_points) - window_size:
            self.current_index = 0
            
