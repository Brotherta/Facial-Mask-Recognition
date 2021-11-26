from PyQt5.QtCore import pyqtSlot


@pyqtSlot()
def save():
    print("SAVE")


@pyqtSlot()
def import_image():
    print("IMPORT IMAGE")


@pyqtSlot()
def import_label():
    print("IMPORT LABEL")


@pyqtSlot()
def about():
    print("This is the best project give us a 20/20 please.")


@pyqtSlot()
def help_menu():
    print("THERE IS NO HELP")
