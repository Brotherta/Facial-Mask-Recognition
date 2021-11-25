from common import *

from src.view.window.main_window import MainWindow

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()