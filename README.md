# Applied Programming - Final Project


## Overview:

This is a PyQt5 application for real-time visualization of 32-channel signal data, which uses an MVVM architecture pattern.

## Application Features:

1). TCP Communication:
  - Handles data chunks of 32 channels × 18 samples
  - Data format: Each chunk contains:
     - 32 channels of data
     - 18 samples per channel
     - Total chunk size: 32 × 18 = 576 values
    
2). Live Plotting using VisPy:
  - With Channel Selection mechanism
  - Multi-Channel Plotting
  - Frequency Domain Analysis
  - Differential (Bipolar) Channel Analysis
    
3). Data Visualisation:
  - Raw Signal
  - Filtered Signal
  - RMS Signal

4). Server-Client Control Button:
  - For efficient data transmission

5). Start/Stop Plotting Button:
  - For better data analysis

6). Status Bar:
  - To display the current status of the connection

7). Zenity Error Management:
  - For a better user experience

## File Structure:

    dieseseineprojektdasichfuerdieunimachensollte2025/
    ├── main.py
    ├── recording.pkl
    ├── run.sh
    ├── README.md
    ├── view/
    |   ├── mainView.py
    |   ├── plotView.py
    |   ├── credits.py
    |   ├── audio.py
    |   ├── nyancat.gif
    |   ├── Sad_Cat_Thumbs_Up.png
    |   ├── Nyan Cat.mp3
    |   ├── cat_waking_up.gif
    |   ├── cat-meow-6226.mpy
    |   ├── cat stationary.gif
    |   ├── cat_sleep_running.gif
    |   ├── cat_goingtosleep.gif
    |   └── wrbung.ttf
    ├── viewmodel/
    |   └── mainViewModel.py
    ├── services/
    |   ├── tcp_server.py
    |   └── tcp_client.py
    └── Signalverarbeitung/
        └── signal_processor.py












## Dependencies:
- matplotlib
- numpy
- pyqt5
- scipy
- vispy
- zenity

## How to use the program??

Step 1 --> Run the 'run.sh' file.

Step 2 --> Click the green 'Start' button to connect the TCP Client to the server.

Step 3 --> Select one of the four available functions located in the top-left of the window.

Step 4 --> Select either 'Raw Signal', 'Filtered Signal', or 'RMS Signal'

Step 5 --> Select the channels that need to be plotted.
           
- Plot Individual Channels -- Only 1 channel can be selected.
- Differential Channels -- Only 2 channels can be selected. The channel selected last will be subtracted from the channel that is                  selected first.
- Frequency Domain Analysis -- Only 1 channel can be selected.
- Cross-Channel Analysis -- Any number of channels can be selected. (The more channels selected, the more laggy the program becomes!)

Step 6 --> Click the 'Start/Stop Button' to start the plotting or to pause the plotting.

## Additional Instructions:

1). Please turn your display into 'Dark/Night Mode' for a better user experience.

2). Use the Mute/Unmute button to mute/unmute the audio.

3). Click the credits button to view the credits for this project.

4). Click the 'Clear Selection' button to clear the channel checkboxes.

