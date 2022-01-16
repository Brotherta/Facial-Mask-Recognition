from PyQt5.QtWidgets import QDialog, QProgressBar, QPushButton, QVBoxLayout, QLabel, QMainWindow


# The loading image progress bar dialog
class ProgressLoad(QDialog):

    def __init__(self, editorWindow: QMainWindow):
        super().__init__(parent=editorWindow)

        # Window
        self.setWindowTitle("Importing images. Please wait.")  # Title
        self.layout = QVBoxLayout()  # Vertical layout
        self.adjustSize()  # Adjust the size of the dialog to fit its contents

        # Widgets
        self.labelNbToLoad = QLabel(self)  # Total amount label
        self.currentLoading = QLabel(self)  # Current label loading
        self.progress = QProgressBar(self)  # Progress bar
        self.progress.setGeometry(200, 80, 250, 20)  # Progress bar size
        self.cancel = QPushButton("Cancel import", self)  # A butter to cancel the loading

        # Layout setup
        self.layout.addWidget(self.labelNbToLoad)
        self.layout.addWidget(self.currentLoading)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.cancel)
        self.setLayout(self.layout)
