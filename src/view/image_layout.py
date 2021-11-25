from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QWidget


class EditorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(200, 80))
        self.setStyleSheet("QListWidget { border: 1px solid red }")
        

    