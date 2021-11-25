from common import *

from src.view.widget.images_list import ImagesListWidget
from src.view.widget.labels_list import LabelsListWidget
from src.view.widget.menu_bar import MenuBar
from src.view.window.editor_window import EditorWidget

MENU_CSS = 'style/style_menu.css'
TITLE = 'Image Annotator'


class MainWindow(QMainWindow):
    centralWidget: QWidget
    rightWidget: QWidget
    layout: QHBoxLayout
    imagesWidget: ImagesListWidget
    menuBar: MenuBar
    widget: QWidget
    box_selector: EditorWidget

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Annotator")
        self.setMinimumSize(QSize(1280, 720))

        self.load_widgets()
        self.layout = QHBoxLayout()

        self.menuBar = MenuBar()

        self.layout.addWidget(self.imagesWidget)
        self.layout.addWidget(self.rightWidget)
        self.widget.setLayout(self.layout)
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)

    def load_widgets(self):
        self.widget = QWidget()

        self.imagesWidget = ImagesListWidget()
        self.imagesWidget.add_image("assets/images/image_de_merde.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")
        self.imagesWidget.add_image("assets/images/image.jpg")

        self.rightWidget = LabelsListWidget()
