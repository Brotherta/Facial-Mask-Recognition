from src import *

from src.view.window.main_window import MainWindow
from qt_material import apply_stylesheet


def load_stylesheet(css_file):
    f = open(css_file, 'r')
    content = f.read()

    return content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    window = MainWindow()
    window.show()
    app.exec_()
