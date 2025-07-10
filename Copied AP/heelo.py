import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

Werbung = QLabel("Hier könnte Ihre Werbung stehen")
Werbung.setFixedSize(400, 100)
Werbung.setAlignment(Qt.AlignCenter)
Werbung.setWordWrap(True)

# Get the directory of the current script file
# (e.g., /Users/anshulpandey/Desktop/hello/dieseseineprojektdasichfuerdieunimachensollte2025/Copied AP/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the components for your font file
font_filename = "werbung.ttf"
font_subfolder = "view" # Assuming 'view' is a subfolder inside script_dir

# Construct the full path
programmatic_font_path = os.path.join(script_dir, font_subfolder, font_filename)

print(f"Current script directory: '{script_dir}'")
print(f"Constructed font path: '{programmatic_font_path}'")

# --- THIS IS THE LINE TO FIX ---
# It MUST be the full path to the .ttf file itself, including the filename
known_working_absolute_path_for_comparison = "/Users/anshulpandey/Desktop/hello/dieseseineprojektdasichfuerdieunimachensollte2025/Copied AP/view/werbung.ttf" # <--- **FIXED HERE**

print(f"Known working absolute path (for comparison): '{known_working_absolute_path_for_comparison}'")

# Compare the paths
paths_are_identical = (programmatic_font_path == known_working_absolute_path_for_comparison)
print(f"Are the two path strings identical? {paths_are_identical}")




font_id = QFontDatabase.addApplicationFont(programmatic_font_path) # Use the programmatically generated path

if font_id == -1:
    print(f"ERROR: Could not load font from '{programmatic_font_path}'.")
    print("Even with correct path, loading failed. Check font file integrity or system permissions.")
    fontt = QFont("Arial", 24)
    fontt.setBold(True)
    Werbung.setFont(fontt)
    print("Using 'Arial' as a fallback font.")
else:
    try:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
            fontt = QFont(font_family, 24)
            fontt.setBold(True)
            Werbung.setFont(fontt)
            print(f"SUCCESS: Loaded font: '{font_family}' from '{programmatic_font_path}'")
        else:
            print(f"WARNING: Font loaded (ID: {font_id}), but no font families found. Corrupted font file?")
            fontt = QFont("Arial", 24)
            fontt.setBold(True)
            Werbung.setFont(fontt)
            print("Using 'Arial' as a fallback font.")
    except IndexError:
        print(f"ERROR: IndexError when getting font family for ID {font_id}. Font might be corrupted or malformed.")
        fontt = QFont("Arial", 24)
        fontt.setBold(True)
        Werbung.setFont(fontt)
        print("Using 'Arial' as a fallback font.")

layout.addWidget(Werbung)

window.setWindowTitle("Werbung Display Final Test")
window.show()
sys.exit(app.exec_())