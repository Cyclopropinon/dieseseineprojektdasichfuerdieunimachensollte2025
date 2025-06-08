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
        
    def calculate_rms(self, data, window_size=None):
        """
        Calculate the Root Mean Square (RMS) of the signal.
        
        Args:
            data (np.ndarray): Input signal data
            window_size (int, optional): Size of the RMS window in samples
            
        Returns:
            np.ndarray: RMS values
        """
        if window_size is None:
            window_size = self.points_per_window
            
        # Calculate RMS using rolling window
        rms = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - window_size + 1)
            window = data[start_idx:i + 1]
            rms[i] = np.sqrt(np.mean(window ** 2))
            
        return rms
    
    def generate_test_signal(self, duration=60):
        """
        Generate a test signal for live plotting demonstration.
        
        This method creates a sine wave with:
        - Period of 2 seconds (0.5 Hz)
        - Amplitude of 3 (oscillates between -3 and 3)
        - Added Gaussian noise for realism
        
        Args:
            duration (int): Total duration of the signal in seconds (default: 60)
            
        Returns:
            tuple: (time_points, signal_data)
                - time_points: Array of time values in seconds
                - signal_data: Array of signal values
        """
        # Create time points for the entire signal duration
        t = np.linspace(0, duration, duration * self.sampling_rate)
        
        # Generate sine wave with 2s period (0.5 Hz) and amplitude 3
        signal = 3 * np.sin(2 * np.pi * 0.5 * t)
        
        # Add small random noise for realism
        signal += np.random.normal(0, 0.2, len(t))
        
        return t, signal