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
    Slot,
)
from PySide6.QtGui import QPainter, QPixmap
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

ROBOT_EMPTY_0 = "image/robot_empty.png"
ROBOT_CARRY_0 = "image/robot_gas.png"
ROBOT_EMPTY_1 = "image/robot_another.png"
ROBOT_CARRY_1 = "image/robot_mineral.png"

SIZE = 100

DEAD_THRESHOLD = 7


class Robot(QGraphicsObject):
    # problem when 2 or more simulator starts shit
    # use dict
    _registry: list[Robot] = []

    missionFinished = Signal(int, NodePos)
    # conveyed = Signal(int)

    def __init__(self, size: int, rNum: int, rType: int, position: NodePos, speed):
        super().__init__()
        self._registry.append(self)
        self.setPos(position.toViewPos().x, position.toViewPos().y)
        self.setTransformOriginPoint(50, 50)
        self.setRotation(position.degree())

        self.size = size
        self.speed = speed
        self.robotType = rType
        self.robotNum = rNum
        if rType == 0:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_0).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_0).scaled(size, size)
        else:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_1).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_1).scaled(size, size)
        self.pixmap_current = self.pixmap_default

        self.processCount = 0
        self.power = 10
        self.stopped = False
        self.box = 0
        self.sequence = 0
        self.route = [position]
        self.priority = rNum

        self.deadlockedCounter = 0

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        painter.drawPixmap(QPointF(0, 0), self.pixmap_current, self.boundingRect())

    def dumpPixmap(self, box: int):
        if box != 0:
            self.pixmap_current = self.pixmap_box
        else:
            self.pixmap_current = self.pixmap_default

    def debug(self, msg: str):
        print(f"Robot {self.robotNum} : {msg}")

    def setRoute(self, route):
        self.route = route
        self.sequence = 0

    def rotateOperation(self, degree: int, duration: int):
        self.stopped = False
        self.power -= 1

        anim = QVariantAnimation(self)
        currRot = int(self.rotation())
        anim.setStartValue(currRot)
        anim.setEndValue(currRot + degree)
        anim.setDuration(duration)
        anim.setEasingCurve(QEasingCurve.Linear)
        anim.valueChanged.connect(self.setRotation)
        anim.finished.connect(self.doNextOperation)
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
        anim.finished.connect(self.doNextOperation)
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def dumpOperation(self, duration: int):
        self.stopped = True
        self.setRoute(self.route[-1:])

        self.processCount += 1
        self.box = 0
        self.dumpPixmap(self.box)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.doNextOperation)
        self.timer.start(duration)

    def waitOperation(self, duration: int):
        self.stopped = True

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.doNextOperation)
        self.timer.start(duration)

    def chargeOperation(self, cell: Cell):
        cell.occupy()
        self.setRoute(self.route[-1:])
        self.stopped = True

        while self.power < 20:
            self.debug(f"power {self.power} route {self.route}")
            sleep(1)
            self.power += 1
        cell.deOccupy()
        self.finishMission()

    def assignMission(self, route: list[NodePos], box: int = 0):
        self.setRoute(route)
        self.box = box
        self.dumpPixmap(self.box)

        self.priority = self.robotNum

        self.doNextOperation()

    def finishMission(self):
        if self.box:
            self.dumpOperation(750)
        else:
            self.missionFinished.emit(self.robotNum, self.route[len(self.route) - 1])

    def getCurrentPos(self):
        if self.sequence == 0 or self.stopped:
            return self.route[self.sequence]
        return self.route[self.sequence - 1]

    def getOperatingPos(self):
        if self.stopped:
            return self.getCurrentPos()
        return self.route[self.sequence]

    """
    일직선상에서 마주보는 로봇일때
    """

    def doNextOperation(self):
        if self.sequence + 1 == len(self.route):
            self.finishMission()
            return

        if (
            degreeDiff := self.route[self.sequence + 1].degree()
            - self.route[self.sequence].degree()
        ) != 0:
            self.sequence += 1
            self.rotateOperation(degreeDiff, self.speed)
        else:
            for opR in self._registry:
                if self.route[self.sequence + 1].posTuple() in [
                    opR.getCurrentPos().posTuple(),
                    opR.getOperatingPos().posTuple(),
                ]:
                    self.waitOperation(self.speed)
                    return

            self.sequence += 1
            self.moveOperation(self.route[self.sequence].toViewPos().point())

    # @Slot()
    # def doNextOperation(self):
    #     if self.sequence + 1 == len(self.route):
    #         self.finishMission()
    #         return

    #     if self.deadlockedCounter >= DEAD_THRESHOLD:
    #         # this idea is not testable
    #         # find all robots
    #         bots: list[Robot] = []
    #         selfPos = self.route[self.sequence].point().toTuple()
    #         for r in self._registry:
    #             neighborPos = r.route[r.sequence].point().toTuple()
    #             if r.stopped:
    #                 if (
    #                     neighborPos == (selfPos[0], selfPos[1] - 1)
    #                     or neighborPos == (selfPos[0], selfPos[1] + 1)
    #                     or neighborPos == (selfPos[0] - 1, selfPos[1])
    #                     or neighborPos == (selfPos[0] + 1, selfPos[1])
    #                 ):
    #                     bots.append(r)

    #         for r in bots:
    #             # i think tempblocked should be nodepos
    #             # each cell can assign "align" mission to robot
    #             # to dump or get box
    #             route = evaluateRoute(
    #                 r.route[r.sequence],
    #                 r.route[len(r.route) - 1],
    #                 tempBlocked=[r.route[r.sequence + 1].point().toTuple()],
    #             )
    #             r.assignMission()

    #     # robot is reached this cell just right now!
    #     degreeDiff = (
    #         self.route[self.sequence + 1].degree() - self.route[self.sequence].degree()
    #     )

    #     if degreeDiff != 0:
    #         self.stopped = False
    #         self.sequence += 1
    #         self.rotateOperation(degreeDiff, self.speed)
    #     else:
    #         self.evadeCollision()

    # def evadeCollision(self):
    #     self_op_dest = self.route[self.sequence + 1]

    #     for r in self._registry:
    #         if r.robotNum == self.robotNum:
    #             continue

    #         opCurrPos = r.currRobotPosWait()
    #         opOperPos = r.getOperatingPos()

    #         # maybe do not use of these...

    #         """
    #         1 0 2
    #         1 wait
    #         2 proceed

    #         / 0 1
    #         0
    #         2
    #         """
    #         # self is finished operation just right now!
    #         # self.seq is not accumulated!

    #         if not r.stopped and self_op_dest.point() == opOperPos.point():
    #             print("op")
    #             self.waitOperation(self.speed + 30)
    #             return

    #         elif self_op_dest.point() == opCurrPos.point():
    #             if facingEach(self_op_dest, opCurrPos):
    #                 print("facing")

    #                 # if tempblocked is one of deadlocked robots destination??
    #                 if self.route[len(self.route) - 1].point() == opCurrPos.point():
    #                     self.priority += 1

    #                 if self.priority < r.priority:
    #                     # call maybe..upper conflict resolver?
    #                     print("evaluate")
    #                     # if tempblocked is one of deadlocked robots destination??
    #                     # tempblocked should be nodepos?
    #                     route = evaluateRoute(
    #                         self.route[self.sequence],
    #                         self.route[len(self.route) - 1],
    #                         tempBlocked=[opCurrPos.point().toTuple()],
    #                     )
    #                     self.assignMission(route, self.box)
    #                     return
    #                 else:
    #                     print(self.robotNum, "evaluate else", self.priority, r.priority)
    #                     self.waitOperation(self.speed + 30)
    #                     return

    #             else:
    #                 print("not facing")
    #                 self.waitOperation(self.speed + 30)
    #                 return

    #     self.stopped = False
    #     self.sequence += 1
    #     self.moveOperation(self.route[self.sequence].toViewPos().point(), self.speed)
    #     return
