import sys
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *

MENU_CSS = 'style/main.css'


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    
    def load_stylesheet(self, css_file):
        f = open(css_file, 'r')
        content = f.read()

        return content
        

    def initUI(self):

        css = self.load_stylesheet(css_file=MENU_CSS)
        self.setStyleSheet(str(css))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        self.mainMenu=self.menuBar()
        
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)

        impMenu.addAction(impAct)

        newAct = QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

      
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')
        self.show()
        


def main():
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
