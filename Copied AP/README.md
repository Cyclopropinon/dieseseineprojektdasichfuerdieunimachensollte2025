# Live Plotting Demo

This project demonstrates real-time data visualization using the MVVM (Model-View-ViewModel) architecture pattern and VisPy for high-performance plotting.

## MVVM Architecture

### What is MVVM?
MVVM (Model-View-ViewModel) is an architectural pattern that separates an application into three main components:

1. **Model**: Handles data and business logic
   - In our case: `SignalProcessor` class that generates and processes the signal data
   - Contains no UI or presentation logic
   - Independent of how data is displayed

2. **View**: User interface and visualization
   - In our case: `MainWindow` and `VisPyPlotWidget` classes
   - Only handles UI elements and user interactions
   - Doesn't know about data processing

3. **ViewModel**: Connects Model and View
   - In our case: `PlotViewModel` class
   - Transforms data from Model into a format the View can display
   - Handles UI logic and state management
   - Uses signals/events to notify View of changes

### Advantages of MVVM
- **Separation of Concerns**: Each component has a specific responsibility
- **Testability**: Components can be tested independently
- **Maintainability**: Changes in one component don't affect others
- **Reusability**: Components can be reused in different contexts
- **Scalability**: Easy to add new features without changing existing code

### Disadvantages of MVVM
- **Complexity**: More initial setup required
- **Learning Curve**: New developers need to understand the pattern
- **Overhead**: Might be overkill for simple applications

### When to Use MVVM
- Complex applications with multiple views
- Applications requiring frequent UI updates
- Projects where testability is important
- Applications with complex business logic
- When working in a team

## Live Plotting

### Why VisPy Instead of Matplotlib?
1. **Performance**: 
   - VisPy uses OpenGL for rendering, making it much faster
   - Can handle thousands of data points at 30+ FPS
   - Matplotlib would struggle with real-time updates

2. **Real-time Capabilities**:
   - VisPy is designed for real-time visualization
   - Matplotlib is better for static plots
   - VisPy has lower latency for updates

3. **Memory Usage**:
   - VisPy is more memory efficient
   - Matplotlib creates new objects for each update
   - VisPy reuses buffers for better performance

### How Live Plotting Works
1. **Data Generation**:
   - Signal is generated at 2048 Hz (samples per second)
   - Total signal length is 60 seconds
   - Window shows 10 seconds at a time

2. **Update Mechanism**:
   - Timer triggers updates at 30 Hz
   - Each update shifts the data window
   - Fixed time window (0-10s) moves through the data
   - Smooth visualization with minimal CPU usage

3. **Performance Considerations**:
   - Fixed window size prevents memory growth
   - Efficient data structures (numpy arrays)
   - OpenGL-based rendering for smooth updates

## Project Structure
```
live_plotting/
├── main.py              # Application entry point
├── services/            # Model layer
│   └── signal_processor.py
├── view/               # View layer
│   ├── main_window.py
│   └── plot_widget.py
└── viewmodel/          # ViewModel layer
    └── plot_viewmodel.py
```

## Requirements
- Python 3.8+
- PyQt5
- VisPy
- NumPy

## Installation
1. Create virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
```bash
python main.py
```

## Usage
1. Click "Start Plotting" to begin visualization
2. The plot shows a 10-second window of data
3. The signal moves through the window in real-time
4. Click "Stop Plotting" to pause the visualization 