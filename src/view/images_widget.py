from common import *


class ImagesWidget(QListWidget):
    
    def __init__(self):
        QListWidget.__init__(self)
        
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setIconSize(QSize(330, 180))
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(False)
        
    def add_image(self, filepath):
        listWidgetItem = QListWidgetItem(filepath)
        listWidgetItem.setIcon(QIcon(filepath))
        self.addItem(listWidgetItem)
        
    
        