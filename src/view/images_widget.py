from common import *


class ImagesWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)

        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(100, 55))
        self.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(QMargins(0, 10, 0, 10))
        
    def add_image(self, filepath):
        listWidgetItem = QListWidgetItem()
        listWidgetItem.setIcon(QIcon(filepath))
        listWidgetItem.setSizeHint(QSize(120, 65))
        self.addItem(listWidgetItem)
        
    
        