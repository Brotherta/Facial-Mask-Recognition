from PyQt5 import QtCore

from src import *
from src.view.window.editor_window import EditorWidget, ImageFMR


class ImagesListWidget(QListWidget):
    confirmEvent = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(ImagesListWidget, self).__init__()

        self.editor_popup: EditorWidget
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(200, 133))
        self.setSpacing(20)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(3)
        self.setSizePolicy(size_policy)

    def add_image(self, image: ImageFMR):
        image_widget_item = ImageWidgetItem(image, self)
        self.addItem(image_widget_item)

    def open_editor(self, item):
        self.editor_popup = EditorWidget(item.image.filepath, self)
        self.editor_popup.exec()

    def close_editor(self):
        self.editor_popup.close()


class ImageWidgetItem(QListWidgetItem):
    image: ImageFMR
    parent: ImagesListWidget

    def __init__(self, image: ImageFMR, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.image = image
        self.setIcon(QIcon(image.filepath))
