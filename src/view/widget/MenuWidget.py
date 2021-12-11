from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

MENU_CSS = 'style/style_menu.css'


class MenuBar(QMenuBar):

    def __init__(self):
        super().__init__()

        self.fileMenu = QMenu('File', self)
        self.saveMenu = QAction('Save', self)
        self.importMenu = QMenu('Import', self)
        self.importImage = QAction('Import images', self)
        self.importLabels = QAction('Import labels', self)

        self.importMenu.addAction(self.importImage)
        self.importMenu.addAction(self.importLabels)
        self.fileMenu.addMenu(self.importMenu)
        self.fileMenu.addAction(self.saveMenu)

        self.newMenu = QMenu('New', self)
        self.newLabel = QAction('New label', self)
        self.newMenu.addAction(self.newLabel)

        self.helpMenu = QMenu('Help', self)
        self.helpUse = QAction('How to use Image Annotator', self)
        self.helpAbout = QAction('About', self)
        self.helpMenu.addAction(self.helpUse)
        self.helpMenu.addAction(self.helpAbout)

        self.addMenu(self.fileMenu)
        self.addMenu(self.newMenu)
        self.addMenu(self.helpMenu)
