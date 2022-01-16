import json

from PyQt5.QtWidgets import QGraphicsRectItem


# This class contains the rectangle, and the label associated.
class Box(QGraphicsRectItem):

    def __init__(self, x, y, width, height, label=None):
        super().__init__(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

        # Assign a tooltip to the rectangle
        if label is None:
            self.setToolTip("None")
        else:
            self.setToolTip(self.label.name)


# Allows the json encode
class BoxEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
