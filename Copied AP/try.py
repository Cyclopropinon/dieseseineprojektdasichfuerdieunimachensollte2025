from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton

self.setWindowTitle("VeryCreativeProjectName")
self.setGeometry(0, 0, 800 ,500 )
self.showFullScreen()  # Enters full screen mode

# Create central widget and layout
central_widget = QWidget()
self.setCentralWidget(central_widget)

##Layout Initializations
main_vertical_layout = QVBoxLayout(central_widget)
horizontal_layout = QHBoxLayout()
control_center = QVBoxLayout()
imp_buttons = QHBoxLayout()
check_group = QHBoxLayout()
check_columns_1 = QVBoxLayout()
check_columns_2 = QVBoxLayout()
check_columns_3 = QVBoxLayout()
check_columns_4 = QVBoxLayout()


##Widget Initializations
self.plot_widget = VisPyPlotWidget()
button_rms = QPushButton("RMS Signal")
button_raw = QPushButton("Raw Signal")
button_filt = QPushButton("Filtered Signal")
select_channels_label = QLabel("Select Channels")

check_list = []
for i in range(1, 33, 1):
    check_list.append(QCheckBox(str(i)))

all = QRadioButton("All")
none = QRadioButton("None")


spacer = QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Fixed)
main_vertical_layout.addSpacerItem(spacer)

main_vertical_layout.addWidget(horizontal_layout)
main_vertical_layout.addWidget(self.plot_widget)
horizontal_layout.addWidget(control_centre)
horizontal_layout.addWidget(self.plot_widget)

control_centre.addWidget(button_raw)
control_centre.addWidget(button_filt)
control_centre.addWidget(button_rms)
control_centre.addWidget(select_channels_label)
control_centre.addWidget(imp_buttons)
control_centre.addWidget(check_group)

imp_buttons.addWidget(all)
imp_buttons.addWidget(none)

check_group.addWidget(check_columns_1)
check_group.addWidget(check_columns_2)
check_group.addWidget(check_columns_3)
check_group.addWidget(check_columns_4)


for x in range(int(len(check_list)/4)):
    check_columns_1.addWidget(check_list[x])

for y in range(int(len(check_list)/4), int(len(check_list)/2)):
    check_columns_2.addWidget(check_list[y])

for z in range(int(len(check_list)/2), int(len(check_list)*3/4)):
    check_columns_3.addWidget(check_list[z])

for t in range(int(len(check_list)*3/4), int(len(check_list))):
    check_columns_4.addWidget(check_list[t])












'''
# Create control button
self.control_button = QPushButton("Start Plotting")
self.control_button.clicked.connect(self.toggle_plotting)
main_vertical_layout.addWidget(self.control_button)


'''