from PyQt5.QtCore import pyqtSlot

from src.view.window.editor_window import EditorWidget


@pyqtSlot()
def on_image_click(item):
    item.parent.editor_popup = EditorWidget()
    item.parent.editor_popup.set_image(item.filepath)
