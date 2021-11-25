from common import *
from src.view.images_widget import ImagesWidget
from src.view.label_widget import LabelsWidget
from src.view.menu_bar import MenuBar

MENU_CSS = 'style/main.css'
TITLE = 'Image Annotator'

class MainWindow(QMainWindow):

    centralWidget: QWidget
    rightWidget: QWidget
    layout: QHBoxLayout
    imagesWidget: ImagesWidget
    menuBar: MenuBar
    widget: QWidget


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Annotator")
        self.setMinimumSize(QSize(720, 480))

        self.loadWidgets()
        self.layout = QHBoxLayout()

        self.menuBar = MenuBar()

        self.layout.addWidget(self.imagesWidget)
        self.layout.addWidget(self.centralWidget)
        self.layout.addWidget(self.rightWidget)
        self.widget.setLayout(self.layout)
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)

    def loadWidgets(self):
        self.widget = QWidget()

        self.imagesWidget = ImagesWidget()
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")

        self.centralWidget = QWidget()
        centralPolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        centralPolicy.setHorizontalStretch(1)
        self.centralWidget.setSizePolicy(centralPolicy)

        self.rightWidget = LabelsWidget()
        droitePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        droitePolicy.setHorizontalStretch(1)
        self.rightWidget.setSizePolicy(centralPolicy)
