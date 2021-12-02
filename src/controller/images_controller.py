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

    def __init__(self, ui, label_controllers):
        self.project = None
        self.label_controllers = label_controllers
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

    def save_images(self):
        for img in self.images:
            print(img.filepath, " : ", len(img.boxs))
            for box in img.boxs:
                print("\t", box.label.name)

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
        items = list(map(lambda x: x.name, self.label_controllers.labels))
        if len(self.label_controllers.labels) > 0:
            box.label = Label(QInputDialog.getItem(self.main_ui.imagesWidget.editor_popup,
                                                   "Choose a label", "Labels : ",
                                                   items))

    def on_image_click(self, item: ImageWidgetItem):
        self.main_ui.imagesWidget.confirmEvent.connect(self.image_edited)
        self.main_ui.imagesWidget.open_editor(item)
