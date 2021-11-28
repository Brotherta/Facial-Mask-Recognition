from src import *
from src.controller.main_controller import ImageAnnotatorController

from src.view.window.main_window import MainWindow
from qt_material import apply_stylesheet


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    main_window = MainWindow()
    controller = ImageAnnotatorController(main_window)
    main_window.show()
    app.exec_()
