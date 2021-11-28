from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from src.controller.images_controller import ImagesController
from src.controller.labels_controller import LabelsController
from src.controller.menu_controller import MenuController
from src.model.labels import Labels
from src.view.widget.labels_widget import LabelsListWidget
from src.view.window.main_window import MainWindow


class ImageAnnotatorController:

    def __init__(self, ui):
        self.main_ui: MainWindow = ui
        self.labels = Labels()
        self.menu_controller = MenuController(ui)
        self.labels_controller = LabelsController(ui)
        self.images_controller = ImagesController(ui)

        self.connect_event_menu_bar()
        self.connect_event_label_widget()
        self.connect_event_images_widget()

    def connect_event_menu_bar(self):
        pass
        # truc muche de la bar.

    def connect_event_label_widget(self):
        labels_widget = self.main_ui.labelsWidget
        del_action = labels_widget.delete_item_action

        self.main_ui.menuBar.new_label.triggered.connect(self.labels_controller.create_label)
        labels_widget.itemDoubleClicked.connect(self.labels_controller.rename_label)
        del_action.triggered.connect(
            lambda: self.labels_controller.del_label(labels_widget.currentItem())
        )
        labels_widget.delEvent.connect(
            lambda: self.labels_controller.del_label(labels_widget.currentItem())
        )

    def connect_event_images_widget(self):
        images_widget = self.main_ui.imagesWidget
        images_widget.itemDoubleClicked.connect(
            lambda: self.images_controller.on_image_click(images_widget.currentItem())
        )
