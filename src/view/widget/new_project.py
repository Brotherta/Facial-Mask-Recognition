from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QWidget, QHBoxLayout


class NewProjectDialog(QDialog):

    def __init__(self, parent_ui):
        super(QDialog, self).__init__()
        self.parent = parent_ui
        self.layout = QVBoxLayout()
        self.layout_form = QFormLayout()
        self.layout_buttons = QHBoxLayout()
        self.setMinimumSize(600, 300)


        self.widget_form = QWidget()
        self.widget_form.setLayout(self.layout_form)

        self.widget_buttons = QWidget()
        self.widget_buttons.setLayout(self.layout_buttons)

        self.project_name = QLineEdit()
        self.project_name.setMaxLength(100)
        self.project_name.setAlignment(Qt.AlignLeft)

        self.project_path = QLineEdit()
        self.project_path.setMaxLength(200)
        self.project_path.setReadOnly(True)
        self.project_path.setAlignment(Qt.AlignLeft)

        self.path_button = QPushButton("Choose a directory", self)
        self.validate_button = QPushButton("Validate", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.layout_form.addRow("Project Name", self.project_name)
        self.layout_form.addRow("Project Path", self.project_path)
        self.layout_form.addRow(self.path_button)

        self.layout_buttons.addWidget(self.validate_button)
        self.layout_buttons.addWidget(self.cancel_button)

        self.layout.addWidget(self.widget_form)
        self.layout.addWidget(self.widget_buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("New Project")

