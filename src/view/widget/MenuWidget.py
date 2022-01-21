from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

MENU_CSS = 'style/style_menu.css'


# The program menu bar. Contains buttons like import image or save project
class MenuBar(QMenuBar):

    def __init__(self):
        super().__init__()

        # File menu
        self.fileMenu = QMenu('File', self)
        self.saveMenu = QAction('Save', self)  # Save action
        self.fileMenu.addAction(self.saveMenu)
        # Import sub menu
        self.importMenu = QMenu('Import', self)
        self.importImage = QAction('Import images', self)
        self.importLabels = QAction('Import labels', self)
        self.importMenu.addAction(self.importImage)
        self.importMenu.addAction(self.importLabels)
        self.fileMenu.addMenu(self.importMenu)

        # New menu
        self.newMenu = QMenu('New', self)
        self.newLabel = QAction('New label', self)
        self.newMenu.addAction(self.newLabel)

        # Help menu
        self.helpMenu = QMenu('Help', self)
        self.helpUse = QAction('How to use Image Annotator', self)
        self.helpAbout = QAction('About', self)
        self.helpMenu.addAction(self.helpUse)
        self.helpMenu.addAction(self.helpAbout)

        # Settings menu
        self.settingsMenu = QMenu('Settings', self)
        self.setLightMode = QAction('Switch to light mode', self)
        self.setDarkMode = QAction('Switch to dark mode', self)
        self.settingsMenu.addAction(self.setLightMode)
        self.settingsMenu.addAction(self.setDarkMode)

        # Models Menu
        self.modelsMenu = QMenu('Models', self)
        self.createModelExisting = QAction('Create a new model from existing images', self)
        self.createModel = QAction('Create a new model from annotations', self)
        self.loadModel = QAction('Load a model', self)
        self.predictImage = QAction('Predict images', self)
        self.stopTraining = QAction('Stop the running training.', self)
        self.modelsMenu.addAction(self.createModel)
        self.modelsMenu.addAction(self.createModelExisting)
        self.modelsMenu.addAction(self.loadModel)
        self.modelsMenu.addAction(self.stopTraining)
        self.modelsMenu.addAction(self.predictImage)
    



        # Add menus to the menu bar
        self.addMenu(self.fileMenu)
        self.addMenu(self.newMenu)
        self.addMenu(self.settingsMenu)
        self.addMenu(self.modelsMenu)
        self.addMenu(self.helpMenu)
        
