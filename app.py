from src import *
from src.controller.main_controller import ImageAnnotatorController

from src.view.window.main_window import MainWindow
from qt_material import apply_stylesheet

from src.view.window.project_window import ProjectWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    main_window = MainWindow()
    project_window = ProjectWindow()
    controller = ImageAnnotatorController(main_window, project_window)
    project_window.show()
    app.exec_()
