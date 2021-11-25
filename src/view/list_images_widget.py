from common import *
from src.controller.list_images_actions import *


class ListImageWidget(QListWidget):
    editor_popup: EditorWidget

    def __init__(self):
        QListWidget.__init__(self)

        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(200, 133))
        # self.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setContentsMargins(QMargins(0, 30, 0, 30))
        self.setSpacing(20)
        self.itemClicked.connect(on_image_click)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(3)
        self.setSizePolicy(size_policy)

    def add_image(self, filepath):
        image_widget_item = ImageWidgetItem(filepath, self)
        self.addItem(image_widget_item)


class ImageWidgetItem(QListWidgetItem):
    filepath: str
    parent: ListImageWidget

    def __init__(self, filepath, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.filepath = filepath
        self.setIcon(QIcon(filepath))
