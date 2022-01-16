from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QWidget, QHBoxLayout


# This dialog allow the user to create a new project
class NewProjectDialog(QDialog):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()  # Vertical layout
        self.setMinimumSize(600, 300)

        # Project form
        self.widgetForm = QWidget()  # Main widget
        self.layoutForm = QFormLayout()
        self.widgetForm.setLayout(self.layoutForm)

        # Buttons
        self.widgetButtons = QWidget()  # Widget which contains the buttons
        self.layoutButtons = QHBoxLayout()  # Horizontal layout for the buttons
        self.widgetButtons.setLayout(self.layoutButtons)

        # Project name input line
        self.projectName = QLineEdit()
        self.projectName.setMaxLength(100)
        self.projectName.setAlignment(Qt.AlignLeft)

        # Project path input line
        self.projectPath = QLineEdit()
        self.projectPath.setMaxLength(200)
        self.projectPath.setReadOnly(True)  # Read-only because it is assigned from the file explorer
        self.projectPath.setAlignment(Qt.AlignLeft)

        # Form buttons
        self.pathButton = QPushButton("Choose a directory", self)
        self.validateButton = QPushButton("Validate", self)
        self.cancelButton = QPushButton("Cancel", self)

        # Form rows
        self.layoutForm.addRow("Project Name", self.projectName)
        self.layoutForm.addRow("Project Path", self.projectPath)
        self.layoutForm.addRow(self.pathButton)

        # Layout
        self.layoutButtons.addWidget(self.validateButton)
        self.layoutButtons.addWidget(self.cancelButton)
        self.layout.addWidget(self.widgetForm)
        self.layout.addWidget(self.widgetButtons)
        self.setLayout(self.layout)

        self.setWindowTitle("New Project") # Title
