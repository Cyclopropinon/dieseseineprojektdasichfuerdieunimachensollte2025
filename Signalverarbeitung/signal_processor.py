import numpy as np
import scipy.signal as signal

class SignalProcessor:
    """
    A class that generates and processes signal data for live plotting.
    
    Attributes:
        window_size (int): Size of the display window in seconds
        sampling_rate (int): Number of samples per second (Hz)
        points_per_window (int): Total number of points in the display window
    """
    
    def __init__(self, sampling_rate=545.5, window_size=10):
        """
        Initialize the signal processor with window and sampling parameters.
        
        Args:
            window_size (int): Size of the display window in seconds (default: 10)
            sampling_rate (int): Sampling rate in Hz (default: 545.5)
        """
        self.window_size = window_size
        self.sampling_rate = sampling_rate
        self.points_per_window = window_size * sampling_rate
        
    def antifilter(self, data):
        """
        Returns the raw data
        """
        return data
        
    def calculate_rms(self, data):
        """
        Calculates the Root Mean Square (RMS) of the signal.
        """
        if self.window_size is None:
            window_size = self.points_per_window
        else:
            window_size = self.window_size

        # Calculate RMS using rolling window
        rms = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - window_size + 1)
            window = data[start_idx:i + 1]
            rms[i] = np.sqrt(np.mean(window ** 2))

        return rms
    
    def butter_filter(self, data):
        """
        Applies the bandpass filter
        """
        nyquist = self.sampling_rate / 2
        low = 20 / nyquist
        high = 250 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        filtered_data = signal.filtfilt(b, a, data)
        return filtered_data
