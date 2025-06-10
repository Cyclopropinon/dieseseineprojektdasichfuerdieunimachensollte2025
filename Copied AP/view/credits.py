import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CreditsDialog(QDialog):
    """
    A custom QDialog class to display project credits.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credits")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)# Set a minimum width for the dialog

        # Create a vertical layout for the dialog content
        layout = QVBoxLayout()

        # Add an image to the Credits Dialog
        self.dialog_image_label = QLabel(self)  # Create a QLabel for the image in the dialog


        dialog_pixmap = QPixmap('view/Sad_Cat_Thumbs_Up.png') # load a local image

        if not dialog_pixmap.isNull():
            # Scale the pixmap for the dialog
            scaled_dialog_pixmap = dialog_pixmap.scaled(150, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.dialog_image_label.setPixmap(scaled_dialog_pixmap)
            self.dialog_image_label.setAlignment(Qt.AlignCenter)  # Center the image
            layout.addWidget(self.dialog_image_label)  # Add the image label to the dialog's layout
        else:
            print("Error: Could not load image for dialog. Please check the path and file format.")

        # Credit text
        credits_text = """
        <h2 style='text-align: center;'>Credits</h2>

        <h3>Developed By:</h3>
        <ul>
            <li>Anshul Pandey</li>
            <li>Lorenz Taschner</li>
        </ul>

        <h3>Special Thanks To:</h3>
        <ul>
            <li>Gemini :)</li>
            
        </ul>

        <p style='text-align: center;'>&copy; 2025 All Rights Reserved.</p>
        """

        # Create a QLabel to display the credit text
        # Set Qt.TextSelectableByMouse to allow copying the text
        credits_label = QLabel(credits_text)
        credits_label.setTextFormat(Qt.RichText)  # Enable HTML formatting
        credits_label.setWordWrap(True)  # Ensure text wraps within the label
        credits_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)

        layout.addWidget(credits_label)

        # Add an "OK" button to close the dialog
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Connect to the accept slot to close the dialog

        # Create a horizontal layout for the button to center it
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to center
        button_layout.addWidget(ok_button)
        button_layout.addStretch()  # Push button to center

        layout.addLayout(button_layout)

        self.setLayout(layout)