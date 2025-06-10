from PyQt5.QtWidgets import QWidget, QVBoxLayout

class FuniWidget(QWidget):
	"""
	"""

	enabled = False
	fileextension = ""
	
	def __init__(self, parent=None):
		"""
		"""
		super().__init__(parent)
		
		# Create layout
		layout = QVBoxLayout()
		self.setLayout(layout)
		
		# blabla
		
	def enable(self, filename):
		"""
		"""
		# blabla
