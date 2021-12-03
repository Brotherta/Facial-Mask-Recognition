from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFileDialog, QInputDialog

from src.model.box import Box
from src.model.image_fmr import ImageFMR
from src.model.label import Label
from src.model.project import Project
from src.view.widget.images_widget import ImageWidgetItem
from src.view.window.editor_window import EditorWidget
from src.view.window.main_window import MainWindow


class ImagesController:

    def __init__(self, ui, main_controller):
        self.project = None
        self.main_controller = main_controller
        self.main_ui: MainWindow = ui
        self.images: list[ImageFMR] = []
        self.main_ui.imagesWidget.assign_label_box.connect(self.add_label_to_box)

    def load_new_image(self):
        filenames = QFileDialog.getOpenFileNames(parent=self.main_ui, caption="Open images", filter="Images files (*.jpg *.png)")
        for filename in filenames[0]:
            self.add_image(ImageFMR(filename))

    def load_images(self, image_name_list, image_folder):
        for image_name in image_name_list:
            self.add_image(ImageFMR(image_folder+"/"+image_name))

    def load_images(self, images: list[ImageFMR]):
        for img in images:
            self.add_image(img)

    def save_images(self):
        for img in self.images:
            print(img.filepath, " : ", len(img.boxs))
            for box in img.boxs:
                if box.label != None:
                    print("\t", box.label.name)
                else:
                    print("\tNo label")

    def add_image(self, image: ImageFMR):
        self.images.append(image)
        self.main_ui.imagesWidget.add_image(image)

    def remove_image(self, filepath):
        for image in self.images:
            if image.filepath == filepath:
                self.images.remove(image)
        '''
        for imageWidget in self.imageListWidget.items():
            if imageWidget.filepath == filepath:
                self.imageListWidget.removeItemWidget(imageWidget)'''

    def image_edited(self, edited: bool):
        self.main_ui.imagesWidget.close_editor()
        self.main_ui.imagesWidget.confirmEvent.disconnect()

    def add_label_to_box(self, box: Box):
        items = list(map(lambda x: x.name, self.main_controller.labels_controller.labels))
        if len(items) > 0:
            text, ok = QInputDialog.getItem(self.main_ui.imagesWidget.editor_popup,
                                                   "Choose a label", "Labels : ",
                                                   items)
            if ok and text:
                for label in self.main_controller.labels_controller.labels:
                    if label.name == text:
                        box.label = label
                        return

    def on_image_click(self, item: ImageWidgetItem):
        self.main_ui.imagesWidget.confirmEvent.connect(self.image_edited)
        self.main_ui.imagesWidget.open_editor(item)
