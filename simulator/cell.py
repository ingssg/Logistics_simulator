from random import randrange

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import (
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QLabel,
    QStyleOptionGraphicsItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from simulator.pathfinding import (
    evaluateRouteToCell,
)
from simulator.robot import Robot

IMAGE_N = "image/u_arrow.png"
IMAGE_S = "image/d_arrow.png"
IMAGE_E = "image/r_arrow.png"
IMAGE_W = "image/l_arrow.png"
IMAGE_H = "image/r_l_arrow.png"
IMAGE_V = "image/u_d_arrow.png"
IMAGE_A = "image/all_arrow.png"

cell_colors = {
    "cell": QColor(0, 0, 0, 0),
    "chute": QColor("red"),
    "buffer": QColor("blue"),
    "workstation": QColor("green"),
    "block": QColor("lightgray"),
    "chargingstation": QColor("yellow"),
}


class Cell(QGraphicsObject):
    def __init__(self, loc, outdir, cellType="cell", parent=None):
        super().__init__(parent)
        self.setPos(loc[0] * 100, loc[1] * 100)
        self.nodeLoc = loc

        self.cellType = cellType
        self.color = cell_colors[cellType]
        if outdir == (1, 0, 0, 0):
            self.pixmap = IMAGE_N
        elif outdir == (0, 0, 1, 0):
            self.pixmap = IMAGE_S
        elif outdir == (0, 1, 0, 0):
            self.pixmap = IMAGE_E
        elif outdir == (0, 0, 0, 1):
            self.pixmap = IMAGE_W
        elif outdir == (1, 0, 1, 0):
            self.pixmap = IMAGE_V
        elif outdir == (0, 1, 0, 1):
            self.pixmap = IMAGE_H
        elif outdir == (1, 1, 1, 1):
            self.pixmap = IMAGE_A
        else:
            self.pixmap = IMAGE_N

        self.setAcceptHoverEvents(True)
        self.infoWindow = CellInfoWindow(self.pos().toTuple(), cellType)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 100, 100)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        painter.fillRect(self.boundingRect(), self.color)
        painter.drawPixmap(QPointF(0, 0), QPixmap(self.pixmap).scaled(100, 100))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.infoWindow.show()


class CellInfoWindow(QWidget):
    def __init__(self, coordinate, cellType) -> None:
        super().__init__(None)
        self.setWindowTitle("new simulation")
        self.setLayout(QVBoxLayout())

        self.setWindowIcon(QIcon("./image/info.png"))
        self.setStyleSheet("background-color:rgb(1,35,38); color:rgb(82,242,226);")

        self.layout().addWidget(QLabel(f"Coordinate X : {coordinate[0]}"))
        self.layout().addWidget(QLabel(f"Coordinate Y : {coordinate[1]}"))
        self.layout().addWidget(QLabel(f"Type : {cellType}"))


class StationCell(Cell):
    color = Qt.blue
    cellType = "workstation"

    def __init__(self, x, y, w, h, chutesPos: list[tuple[int, int]]):
        super().__init__(x, y, w, h, self.color)
        self.chutesPos = chutesPos

    # call view(parent).nextcargo() ??
    def nextCargo(self) -> tuple[int, int]:
        next = randrange(0, len(self.chutesPos))
        return self.chutesPos[next]

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(robot.route[len(robot.route) - 1], self.nextCargo())
        robot.assignMission(route, 8)


class StationQueueCell(Cell):
    color = Qt.darkBlue
    cellType = "buffer"

    def __init__(self, x, y, w, h, nextQueue: tuple[int, int]):
        super().__init__(x, y, w, h, self.color)
        self.nextQueue = nextQueue

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(robot.route[len(robot.route) - 1], self.nextQueue)
        robot.assignMission(route, 0)


class ChuteCell(Cell):
    color = Qt.red
    cellType = "chute"

    def __init__(self, x, y, w, h, returnPos: tuple[int, int]):
        super().__init__(x, y, w, h, self.color)
        self.returnPos = returnPos

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(robot.route[len(robot.route) - 1], self.returnPos)
        robot.assignMission(route, 0)


class BlockedCell(Cell):
    color = Qt.gray
    cellType = "block"

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)
