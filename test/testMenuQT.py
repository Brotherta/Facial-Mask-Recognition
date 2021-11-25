import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        self.mainMenu=self.menuBar()
        self.setStyleSheet("""
            QMenuBar {
                background-color: rgb(49,49,49);
                color: rgb(255,255,255);
                border: 1px solid #000;
            }

            QMenuBar::item {
                background-color: rgb(49,49,49);
                color: rgb(255,255,255);
            }

            QMenuBar::item::selected {
                background-color: rgb(30,30,30);
            }

            QMenu {
                background-color: rgb(49,49,49);
                color: rgb(255,255,255);
                border: 1px solid #000;           
            }

            QMenu::item::selected {
                background-color: rgb(30,30,30);
            }
        """)

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
