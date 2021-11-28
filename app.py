from src import *
from src.controller.annotator import ImageAnnotatorController

from src.view.window.main_window import MainWindow
from qt_material import apply_stylesheet


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    annotator = ImageAnnotatorController()
    window = MainWindow(annotator)
    annotator.set_ui(window)
    window.show()
    app.exec_()
