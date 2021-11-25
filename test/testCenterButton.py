import sys
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        connect_button = QPushButton('Connect')
        connect_button.setFixedSize(120, 30)

        connect_progress = QProgressBar()
        connect_progress.setRange(0, 10000)
        connect_progress.setValue(0)

        connect_box = QVBoxLayout(self)
        connect_box.setAlignment(Qt.AlignCenter)  

        connect_box.addWidget(connect_button, alignment=Qt.AlignmentFlag.AlignCenter)  # < ----

        connect_box.addWidget(connect_progress)
        connect_box.setContentsMargins(0, 20, 0, 0)
        self.setGeometry(300, 300, 300, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())