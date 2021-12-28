from PyQt5.QtCore import QPoint

from src.model.Box import Box


def load_stylesheet(css_file):
    with open(css_file, 'r') as f:
        content = f.read()
    return content


class Intersection:

    @staticmethod
    def getArea(UL: QPoint, UR: QPoint, DL: QPoint) -> int:
        return (UR.x() - UL.x()) * (DL.y() - UL.y())

    @staticmethod
    def isInRect(point: QPoint, rect: Box) -> bool:
        x = point.x()
        y = point.y()
        if (rect.x < x < rect.x + rect.width
                and rect.y < y < rect.y + rect.height):
            return True
        return False

    @staticmethod
    def isIntersection(up: QPoint, down: QPoint, left: QPoint, right: QPoint):
        if (left.x() < up.x() < right.x()
                and up.y() < left.y() < down.y()):
            return QPoint(up.x(), left.y())
        else:
            return None