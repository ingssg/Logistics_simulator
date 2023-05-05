from random import randrange

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QLabel, QVBoxLayout, QWidget

from simulator.pathfinding import (Direction, NodePos, Pos, ViewPos, backTrack, dijkstra,
                                   evaluateRoute, evaluateRouteToCell, generateGraph)
from simulator.robot import Robot


class Cell(QGraphicsRectItem):
    def __init__(self, x, y, w, h, color, cellt='cell'):
        super().__init__(x, y, w, h)
        self.setBrush(color)
        self.coordinate = (x//100, y//100)

        self.cellType = cellt
        self.outDirection = {}

        self.setAcceptHoverEvents(True)
        self.infoWindow = CellInfoWindow(self.coordinate, self.cellType)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.infoWindow.show()

    def assign(self, robot: Robot):
        print("error in cell.py :", robot.robotNum,
              "called assign function on empty cell")


class CellInfoWindow(QWidget):
    def __init__(self, coordinate, cellType) -> None:
        super().__init__(None)
        self.setWindowTitle('new simulation')
        self.setLayout(QVBoxLayout())

        self.setWindowIcon(QIcon('./image/info.png'))
        self.setStyleSheet("background-color:rgb(1,35,38); color:rgb(82,242,226);")

        self.layout().addWidget(QLabel(f"Coordinate X : {coordinate[0]}"))
        self.layout().addWidget(QLabel(f"Coordinate Y : {coordinate[1]}"))
        self.layout().addWidget(QLabel(f"Type : {cellType}"))


class StationCell(Cell):
    color = Qt.blue
    cellType = 'workstation'

    def __init__(self, x, y, w, h, chutesPos: list[tuple[int, int]]):
        super().__init__(x, y, w, h, self.color)
        self.chutesPos = chutesPos

    # call view(parent).nextcargo() ??
    def nextCargo(self) -> tuple[int, int]:
        next = randrange(0, len(self.chutesPos))
        return self.chutesPos[next]

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(
            robot.route[len(robot.route)-1], self.nextCargo())
        robot.assignMission(route, 8)


class StationQueueCell(Cell):
    color = Qt.darkBlue
    cellType = 'buffer'

    def __init__(self, x, y, w, h, nextQueue: tuple[int, int]):
        super().__init__(x, y, w, h, self.color)
        self.nextQueue = nextQueue

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(
            robot.route[len(robot.route)-1], self.nextQueue)
        robot.assignMission(route, 0)


class ChuteCell(Cell):
    color = Qt.red
    cellType = "chute"

    def __init__(self, x, y, w, h, returnPos: tuple[int, int]):
        super().__init__(x, y, w, h, self.color)
        self.returnPos = returnPos

    def assign(self, robot: Robot):
        route = evaluateRouteToCell(
            robot.route[len(robot.route)-1], self.returnPos)
        robot.assignMission(route, 0)


class BlockedCell(Cell):
    color = Qt.gray
    cellType = "block"

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)
