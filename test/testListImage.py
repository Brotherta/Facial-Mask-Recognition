import sys
from os import listdir, walk
from os.path import isfile, join
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMainWindow, QVBoxLayout, QWidget

class Window(QMainWindow):
    listWidget: QListWidget
    windowLayout : QVBoxLayout
    
    def __init__(self):
        QMainWindow.__init__(self)
        imageFolder = sys.argv[1]

        self.listWidget = QListWidget()
        self.listWidget.setViewMode(QListWidget.ViewMode.IconMode)
        self.listWidget.setIconSize(QSize(330, 180))
        self.listWidget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.listWidget.setAcceptDrops(False)

        for (dirpath, dirnames, filenames) in walk(imageFolder):
            for filename in filenames:
                filepath = dirpath + filename
                listWidgetItem = QListWidgetItem(filename)
                listWidgetItem.setIcon(QIcon(filepath))
                self.listWidget.addItem(listWidgetItem)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)



app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
   


window = Window()
window.setWindowTitle("Image Annotator Image List")
window.show()

app.exec_()

