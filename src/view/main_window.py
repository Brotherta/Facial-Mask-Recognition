from common import *
from src.view.images_widget import ImagesWidget
from src.view.menu_bar import MenuBar


MENU_CSS = 'style/main.css'
TITLE = 'Image Annotator'


class MainWindow(QMainWindow):
    
    widget: QWidget
    layout: QHBoxLayout
    imagesWidget: ImagesWidget
    menuBar: MenuBar
    
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(720, 480)
        self.setWindowTitle("Image Annotator")
        
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        
        self.imagesWidget = ImagesWidget()
        self.menuBar = MenuBar()
        
        self.widget.setLayout(self.layout)
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)
        
    