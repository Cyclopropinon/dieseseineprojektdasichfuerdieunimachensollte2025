import numpy as np

class SignalProcessor:
    """
    A class that generates and processes signal data for live plotting.
    
    This class is part of the Model layer in the MVVM architecture. It handles:
    - Signal generation with specified parameters
    - Signal processing and window management
    - No UI or visualization logic
    
    Attributes:
        window_size (int): Size of the display window in seconds
        sampling_rate (int): Number of samples per second (Hz)
        points_per_window (int): Total number of points in the display window
    """
    
    def __init__(self, window_size=10, sampling_rate=2048):
        """
        Initialize the signal processor with window and sampling parameters.
        
        Args:
            window_size (int): Size of the display window in seconds (default: 10)
            sampling_rate (int): Sampling rate in Hz (default: 2048)
        """
        self.window_size = window_size
        self.sampling_rate = sampling_rate
        self.points_per_window = window_size * sampling_rate
        
    def antifilter(self, data):
        return data
        
    def calculate_rms(self, data):
        """
        Calculate the Root Mean Square (RMS) of the signal.
        
        Args:
            data (np.ndarray): Input signal data
            window_size (int, optional): Size of the RMS window in samples
            
        Returns:
            np.ndarray: RMS values
        """
        #if window_size is None:
        window_size = self.points_per_window
            
        # Calculate RMS using rolling window
        rms = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - window_size + 1)
            window = data[start_idx:i + 1]
            rms[i] = np.sqrt(np.mean(window ** 2))
            
        return rms
    
    def butter_filter(self, data):
        t = np.arange(channel_data.shape[1]) / sampling_rate
        # Apply bandpass filter
        nyquist = sampling_rate / 2
        low = 20 / nyquist
        high = 450 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        filtered_data = signal.filtfilt(b, a, channel_data[20, :])
        return filtered_data
