import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class GifWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Looping GIF in PyQt5")
        self.setGeometry(100, 100, 400, 400) # x, y, width, height

        self.central_widget = QLabel(self)
        self.setCentralWidget(self.central_widget)

        # Ensure the label can grow/shrink with content and align center
        self.central_widget.setAlignment(Qt.AlignCenter)

        # --- Load and display the GIF ---
        gif_path = "view/funiStuff/nyancat.gif"  # Make sure this GIF file exists in the same directory

        self.movie = QMovie(gif_path)

        # Optional: Set the cache mode for better performance (CacheAll for smoother looping)
        # However, for simple looping GIFs, this is often not strictly necessary.
        # self.movie.setCacheMode(QMovie.CacheAll)

        # Set the movie to the label
        self.central_widget.setMovie(self.movie)

        # Start the animation
        self.movie.start()

        # Check if the GIF loops (most GIFs are designed to loop by default)
        # If your GIF doesn't loop, it might be due to the GIF file itself
        # having a "play once" setting. You can sometimes change this with GIF editing software.
        # The QMovie class respects the looping property embedded in the GIF.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifWindow()
    window.show()
    sys.exit(app.exec_())