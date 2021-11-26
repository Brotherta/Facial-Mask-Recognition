from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

from src.controller.action.menu import import_label


class LabelsListWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)
        self.setMaximumWidth(150)
        self.setSpacing(15)
        self.itemClicked.connect(import_label)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        self.setSizePolicy(size_policy)

    def add_label(self, label_name):
        label_widget_item = LabelWidgetItem(label_name, self)
        self.addItem(label_widget_item)


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, name, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.setText(name)
