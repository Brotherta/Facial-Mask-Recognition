from common import *
from src.view.list_images_widget import ListImageWidget
from src.view.list_label_widget import ListLabelsWidget
from src.view.menu_bar import MenuBar

MENU_CSS = 'style/main.css'
TITLE = 'Image Annotator'

class MainWindow(QMainWindow):

    centralWidget: QWidget
    rightWidget: QWidget
    layout: QHBoxLayout
    imagesWidget: ListImageWidget
    menuBar: MenuBar
    widget: QWidget


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Annotator")
        self.setMinimumSize(QSize(1280, 720))

        self.loadWidgets()
        self.layout = QHBoxLayout()

        self.menuBar = MenuBar()

        self.layout.addWidget(self.imagesWidget)
        self.layout.addWidget(self.rightWidget)
        self.widget.setLayout(self.layout)
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)


    def loadWidgets(self):
        self.widget = QWidget()

        self.imagesWidget = ListImageWidget()
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")

        self.rightWidget = ListLabelsWidget()
        
