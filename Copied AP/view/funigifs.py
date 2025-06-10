from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class FuniWidget(QWidget):
	"""
	Widget to display funi stuff on da sceen :D
	"""

	def __init__(self, parent=None):
		super(FuniWidget, self).__init__(parent)
		self.enabled = False
		self.fileextension = ""
		self.filename = ""
		self.movie = None

		# Label to display the gif
		self.label = QLabel(self)
		self.label.setAlignment(Qt.AlignCenter)

		layout = QVBoxLayout()
		layout.addWidget(self.label)
		self.setLayout(layout)

	def enable(self, filename):
		"""
		Enables the widget & loads the gif
		"""
		self.filename = filename
		self.fileextension = filename.split('.')[-1].lower()
		if self.fileextension != 'gif':
			print("Only GIF files are supported.")
			return

		self.movie = QMovie(filename)
		self.label.setMovie(self.movie)
		self.enabled = True

	def play(self, filename=None):
		"""
		Plays / resumes the gif
		"""
		if filename:
			self.enable(filename)

		if self.enabled and self.movie:
			self.movie.start()

	def pause(self, filename=None):
		"""
		Pauses the gif
		"""
		if self.enabled and self.movie:
			self.movie.setPaused(True)