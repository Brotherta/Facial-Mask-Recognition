import json

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent


class Box(QGraphicsRectItem):

    def __init__(self, x, y, width, height, label=None):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        if (label == None):
            self.setToolTip("None")
        else:
            self.setToolTip(self.label.name)


class BoxEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
