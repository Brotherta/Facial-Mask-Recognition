from PyQt5.QtWidgets import QFileDialog

from src.view.widget.images_widget import ImageWidgetItem
from src.view.window.editor_window import EditorWidget, ImageFMR
from src.view.window.main_window import MainWindow


class ImagesController:

    def __init__(self, ui):
        self.main_ui: MainWindow = ui
        self.images = []

    def load_new_image(self):
        filenames = QFileDialog.getOpenFileNames(parent=self.main_ui, caption="Open images", filter="Images files (*.jpg *.png)")
        for filename in filenames[0]:
            self.add_image(ImageFMR(filename))

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
        if edited:
            print("edited!")
        else:
            print("not edited !")
        self.main_ui.imagesWidget.close_editor()
        self.main_ui.imagesWidget.confirmEvent.disconnect()

    def on_image_click(self, item: ImageWidgetItem):
        self.main_ui.imagesWidget.confirmEvent.connect(self.image_edited)
        self.main_ui.imagesWidget.open_editor(item)