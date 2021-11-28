from src import *

from src.controller.action.menu import *

MENU_CSS = 'style/style_menu.css'


class MenuBar(QMenuBar):
    file_menu: QMenu
    import_menu: QMenu
    save_menu: QAction
    import_image: QAction
    import_labels: QAction

    help_menu: QMenu
    help_use: QAction
    help_about: QAction

    new_menu: QMenu
    new_label: QAction

    def __init__(self, annotator):
        super().__init__()
        self.annotator = annotator
        self.init_menu()

    def init_menu(self):
        self.file_menu = QMenu('File', self)
        self.save_menu = QAction('Save', self)
        self.import_menu = QMenu('Import', self)
        self.import_image = QAction('Import images', self)
        self.import_labels = QAction('Import labels', self)

        self.import_menu.addAction(self.import_image)
        self.import_menu.addAction(self.import_labels)
        self.file_menu.addMenu(self.import_menu)
        self.file_menu.addAction(self.save_menu)

        self.new_menu = QMenu('New', self)
        self.new_label = QAction('New label', self)
        self.new_menu.addAction(self.new_label)

        self.new_label.triggered.connect(self.annotator.create_label)

        self.help_menu = QMenu('Help', self)
        self.help_use = QAction('How to use Image Annotator', self)
        self.help_about = QAction('About', self)
        self.help_menu.addAction(self.help_use)
        self.help_menu.addAction(self.help_about)

        self.help_about.triggered.connect(about)


        self.addMenu(self.file_menu)
        self.addMenu(self.new_menu)
        self.addMenu(self.help_menu)
