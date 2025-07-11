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
        self.setMinimumHeight(300)
        self.setStyleSheet("background-color: #323232; color: white;")
        layout = QVBoxLayout()

        self.dialog_image_label = QLabel(self)
        dialog_pixmap = QPixmap('view/Sad_Cat_Thumbs_Up.png')

        if not dialog_pixmap.isNull():

            scaled_dialog_pixmap = dialog_pixmap.scaled(150, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.dialog_image_label.setPixmap(scaled_dialog_pixmap)
            self.dialog_image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.dialog_image_label)
        else:
            print("Error: Could not load image for dialog. Please check the path and file format.")

        credits_text = """
        <h2 style='text-align: center; color: white;'>Credits</h2>

        <h3 style='color: white;'>Developed By:</h3>
        <ul style='color: white;'>
            <li>Anshul Pandey</li>
            <li>Lorenz Taschner</li>
        </ul>

        <p style='text-align: center; color: white;'>&copy; 2025 All Rights Reserved.</p>
        """
        credits_label = QLabel(credits_text)
        credits_label.setTextFormat(Qt.RichText)
        credits_label.setWordWrap(True)
        credits_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)

        layout.addWidget(credits_label)
        ok_button = QPushButton("OK")
        ok_button.setObjectName("ok_button")
        ok_button.setStyleSheet("""#ok_button {background-color: #9f9f9f;}
                                            #ok_button:hover {background-color: #bcbcbc;}
                                            #ok_button:pressed {background-color: #7f7f7f;}
                                            """)
        ok_button.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)