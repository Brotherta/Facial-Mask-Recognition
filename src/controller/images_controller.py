from src.view.widget.images_widget import ImageWidgetItem
from src.view.window.editor_window import EditorWidget
from src.view.window.main_window import MainWindow


class ImagesController:

    def __init__(self, ui):
        self.main_ui: MainWindow = ui

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
