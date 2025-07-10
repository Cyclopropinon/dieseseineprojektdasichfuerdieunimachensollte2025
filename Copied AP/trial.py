import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

class CheckBoxColorExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checkbox Color Example')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Checkbox 1: Default style
        checkbox1 = QCheckBox('Default Checkbox', self)
        layout.addWidget(checkbox1)

        # Checkbox 2: Custom indicator color when checked (green)
        checkbox2 = QCheckBox('Green when Checked', self)
        checkbox2.setStyleSheet(
            "QCheckBox::indicator:checked {"
            "background-color: green;"
            "border: 1px solid darkgreen;"
            "}"
            "QCheckBox::indicator:unchecked {"
            "background-color: lightgray;"
            "border: 1px solid gray;"
            "}"
        )
        layout.addWidget(checkbox2)

        # Checkbox 3: Custom indicator color and text color
        checkbox3 = QCheckBox('Blue Indicator & Red Text', self)
        checkbox3.setStyleSheet(
            "QCheckBox {"
            "color: red;"  # Text color
            "}"
            "QCheckBox::indicator {"
            "width: 20px;"
            "height: 20px;"
            "border-radius: 3px;"
            "}"
            "QCheckBox::indicator:checked {"
            "background-color: blue;"
            "border: 1px solid darkblue;"
            "}"
            "QCheckBox::indicator:unchecked {"
            "background-color: lightblue;"
            "border: 1px solid blue;"
            "}"
        )
        layout.addWidget(checkbox3)

        # Checkbox 4: Hover and pressed states
        checkbox4 = QCheckBox('Hover/Pressed Effects', self)
        checkbox4.setStyleSheet(
            "QCheckBox::indicator {"
            "background-color: yellow;"
            "border: 1px solid orange;"
            "}"
            "QCheckBox::indicator:hover {"
            "background-color: lightyellow;"
            "}"
            "QCheckBox::indicator:pressed {"
            "background-color: gold;"
            "}"
            "QCheckBox::indicator:checked {"
            "background-color: purple;"
            "border: 1px solid darkpurple;"
            "}"
        )
        layout.addWidget(checkbox4)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckBoxColorExample()
    ex.show()
    sys.exit(app.exec_())