from PyQt5.QtCore import pyqtSlot

from src.view.editor_widget import EditorWidget


@pyqtSlot()
def on_image_click(item):
    item.parent.editor_popup = EditorWidget()
    item.parent.editor_popup.set_image(item.filepath)
