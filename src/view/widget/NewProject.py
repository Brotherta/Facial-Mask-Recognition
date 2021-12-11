from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QWidget, QHBoxLayout


class NewProjectDialog(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.layoutForm = QFormLayout()
        self.layoutButtons = QHBoxLayout()
        self.setMinimumSize(600, 300)

        self.widgetForm = QWidget()
        self.widgetForm.setLayout(self.layoutForm)

        self.widgetButtons = QWidget()
        self.widgetButtons.setLayout(self.layoutButtons)

        self.projectName = QLineEdit()
        self.projectName.setMaxLength(100)
        self.projectName.setAlignment(Qt.AlignLeft)

        self.projectPath = QLineEdit()
        self.projectPath.setMaxLength(200)
        self.projectPath.setReadOnly(True)
        self.projectPath.setAlignment(Qt.AlignLeft)

        self.pathButton = QPushButton("Choose a directory", self)
        self.validateButton = QPushButton("Validate", self)
        self.cancelButton = QPushButton("Cancel", self)

        self.layoutForm.addRow("Project Name", self.projectName)
        self.layoutForm.addRow("Project Path", self.projectPath)
        self.layoutForm.addRow(self.pathButton)

        self.layoutButtons.addWidget(self.validateButton)
        self.layoutButtons.addWidget(self.cancelButton)

        self.layout.addWidget(self.widgetForm)
        self.layout.addWidget(self.widgetButtons)

        self.setLayout(self.layout)
        self.setWindowTitle("New Project")
