from __future__ import annotations
from time import sleep
from typing import TYPE_CHECKING
from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QPoint,
    QPointF,
    QRectF,
    QTimer,
    QVariantAnimation,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import (
    QGraphicsObject,
    QStyleOptionGraphicsItem,
)

if TYPE_CHECKING:
    from simulator.cell import Cell

from simulator.pathfinding import (
    NodePos,
    evaluateRoute,
    facingEach,
)

ROBOT_EMPTY_0 = "image/belt.png"
ROBOT_CARRY_0 = "image/belt_logis.png"
ROBOT_EMPTY_1 = "image/dump.png"
ROBOT_CARRY_1 = "image/dump_logis.png"

SIZE = 100

DEAD_THRESHOLD = 2


class Robot(QGraphicsObject):
    _registry: dict[str, list[Robot]] = {}
    missionFinished = Signal(int, NodePos)
    robotClicked = Signal(int)

    def __init__(
        self,
        size: int,
        rNum: int,
        rType: int,
        position: NodePos,
        speed,
        simulName: str,
        initDest: NodePos,
    ):
        super().__init__()
        self.setPos(position.toViewPos().x, position.toViewPos().y)
        self.setTransformOriginPoint(50, 50)
        self.setRotation(position.degree())
        self.setAcceptHoverEvents(True)
        self._registry[simulName].append(self)

        self.simulName = simulName
        self.size = size
        self.speed = speed
        self.robotNum = rNum
        self.processCount = 0
        self.power = 1000
        self.box = 0
        self.robotType = rType
        if rType == 0:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_0).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_0).scaled(size, size)
        else:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_1).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_1).scaled(size, size)
        self.pixmap_current = self.pixmap_default

        self.charging = False
        self.stopped = False
        # if simulation finished, robot dont move

        self.dest: NodePos = initDest
        self.currentPos: NodePos = position
        self.operatingPos: NodePos = position
        self.routeCache: list[NodePos] = []
        self.waitCount = 0

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        painter.drawPixmap(QPointF(0, 0), self.pixmap_current, self.boundingRect())
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Arial", 16))
        painter.drawText(QPointF(60, 80), str(self.robotNum))

    def mousePressEvent(self, e):
        print(f"Robot {self.robotNum}")
        print(f"dest {self.dest}")
        print(f"power {self.power}")
        print("---")
        robotinfo = {
            "num": self.robotNum,
            "destination": self.route[-1],
            "power": self.power,
            "charging": self.charging,
        }
        self.robotClicked.emit(self.robotNum)

    def dumpPixmap(self, box: int):
        if box != 0:
            self.pixmap_current = self.pixmap_box
        else:
            self.pixmap_current = self.pixmap_default

    def debug(self, msg: object):
        print(f"DEBUG Robot{self.robotNum}: {msg}")

    def rotateOperation(self, degree: int):
        self.stopped = False
        self.power -= 1

        if self.currentPos.direction == 0 and degree == 270:
            endValue = -90
        else:
            endValue = degree

        anim = QVariantAnimation(self)
        currRot = int(self.rotation())
        anim.setStartValue(currRot)
        anim.setEndValue(endValue)
        anim.setDuration(self.speed)
        anim.setEasingCurve(QEasingCurve.Linear)
        anim.valueChanged.connect(self.setRotation)
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def moveOperation(self, destination: QPoint):
        self.stopped = False
        self.power -= 1

        anim = QVariantAnimation(self)
        anim.setStartValue(QPoint(int(self.pos().x()), int(self.pos().y())))
        anim.setEndValue(destination)
        anim.setDuration(self.speed)
        anim.setEasingCurve(QEasingCurve.Linear)
        anim.valueChanged.connect(self.setPos)
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def doConveyOperation(self, nextPos: NodePos):
        if nextPos == self.currentPos:
            self.waitOperation()
            return

        self.waitCount = 0
        if (nextPos.degree() - self.currentPos.degree()) != 0:
            self.rotateOperation(nextPos.degree())
        else:
            self.moveOperation(self.operatingPos.toViewPos().point())

    # def dumpOperation(self):
    #     self.stopped = True
    #     # self.setRoute(self.route[-1:])

    #     self.processCount += 1
    #     self.box = 0
    #     self.dumpPixmap(self.box)

    #     self.timer = QTimer(self)
    #     self.timer.setSingleShot(True)
    #     # self.timer.timeout.connect(self.doNextOperation)
    #     self.timer.start(self.speed)

    def waitOperation(self):
        # self.stopped = True
        self.waitCount += 1

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        # self.timer.timeout.connect(self.doNextOperation)
        self.timer.start(self.speed)

    # def charge(self):
    #     if self.power < 20:
    #         self.charging = True
    #         self.power += 1
    #         self.timer = QTimer(self)
    #         self.timer.setSingleShot(True)
    #         self.timer.timeout.connect(self.charge)
    #         self.timer.start(self.speed)
    #     else:
    #         self.charging = False
    #         self.finishMission()

    def setDest(self, dest, box):
        self.box = box
        self.dumpPixmap(self.box)

        self.dest = dest
        self.routeCache = []
        # self.doNextOperation()

    # operation 뒤에 붙는 donextoperation 지우면 메인스레드에서 관리할수있음
    # def doNextOperation(self):
    #     self.currentPos = self.operatingPos

    #     if self.currentPos == self.dest:
    #         self.finishMission()
    #         return

    #     booked = []
    #     for opRobot in self._registry[self.simulName]:
    #         if opRobot.robotNum != self.robotNum:
    #             booked.extend(
    #                 [opRobot.currentPos.posTuple(), opRobot.operatingPos.posTuple()]
    #             )
    #     route = evaluateRoute(self.currentPos, self.dest, booked)
    #     self.debug(booked)
    #     self.debug(route)
    #     if route is not None:
    #         self.routeCache = route
    #     else:
    #         if self.routeCache:
    #             curr = self.routeCache.index(self.currentPos)
    #             self.currentPos = self.routeCache[curr]
    #             self.operatingPos = self.routeCache[curr + 1]

    #             if self.operatingPos in booked:
    #                 self.waitOperation()

    #                 return

    #             if (
    #                 degreeDiff := self.operatingPos.degree() - self.currentPos.degree()
    #             ) != 0:
    #                 self.rotateOperation(degreeDiff)
    #                 return
    #             else:
    #                 self.moveOperation(self.operatingPos.toViewPos().point())
    #                 return

    #         t, c = self.parent().findCell(self.currentPos)

    #         if t == "buffer" or t == "workstation":
    #             # can rotate if not aligned
    #             # not now
    #             self.waitOperation()
    #         else:
    #             self.debug(f"resolve curr {self.currentPos} dest {self.dest}")
    #         return

    #     currPos = route[0]
    #     nextPos = route[1]
    #     self.currentPos = currPos
    #     self.operatingPos = nextPos

    #     if (degreeDiff := self.operatingPos.degree() - self.currentPos.degree()) != 0:
    #         self.rotateOperation(degreeDiff)
    #     else:
    #         self.moveOperation(nextPos.toViewPos().point())

    # def finishMission(self):
    #     if self.box:
    #         self.dumpOperation()
    #     else:
    #         self.missionFinished.emit(self.robotNum, self.currentPos)
