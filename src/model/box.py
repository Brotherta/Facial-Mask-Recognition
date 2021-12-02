from PyQt5.QtCore import QRect

from src.model.label import Label


class Box:

    def __init__(self, rect: QRect, label: Label):
        self.rect = rect
        self.label = label

    def set_label(self, label: Label):
        self.label = label

    def set_rect(self, rect: QRect):
        self.rect = rect
