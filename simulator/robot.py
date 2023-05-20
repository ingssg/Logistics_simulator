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

DEAD_THRESHOLD = 2


class Robot(QGraphicsObject):
    _registry: dict[str, list[Robot]] = {}
    missionFinished = Signal(int, NodePos)

    def __init__(
        self, size: int, rNum: int, rType: int, position: NodePos, speed, simulName: str
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
        self.robotType = rType
        self.robotNum = rNum
        if rType == 0:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_0).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_0).scaled(size, size)
        else:
            self.pixmap_default = QPixmap(ROBOT_EMPTY_1).scaled(size, size)
            self.pixmap_box = QPixmap(ROBOT_CARRY_1).scaled(size, size)
        self.pixmap_current = self.pixmap_default

        self.stopped = True
        self.charging = False
        self.processCount = 0
        self.power = 10
        self.box = 0
        self.sequence = 0
        self.route = [position]
        self.priority = rNum

        self.errors = 0
        self.tempBlocks: list[tuple[int, int]] = []
        # reset when moveoperation

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        painter.drawPixmap(QPointF(0, 0), self.pixmap_current, self.boundingRect())

    def mousePressEvent(self, e):
        print(f"Robot {self.robotNum}")
        print(f"destination {self.route[-1]}")
        print(f"charging {self.charging}")
        print(f"power {self.power}")
        print("current route")
        print(self.route)
        print("---")

    def dumpPixmap(self, box: int):
        if box != 0:
            self.pixmap_current = self.pixmap_box
        else:
            self.pixmap_current = self.pixmap_default

    def debug(self, msg: object):
        print(f"DEBUG Robot{self.robotNum}: {msg}")

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
        # self.tempBlocks=[]

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

    def charge(self):
        if self.power < 20:
            self.charging = True
            self.power += 1
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.charge)
            self.timer.start(self.speed)
        else:
            self.charging = False
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

    def priorThan(self, r: Robot):
        if r.box > 0 and self.box == 0:
            return False
        elif r.charging:
            return False
        else:
            return self.robotNum > r.robotNum

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
            for opR in self._registry[self.simulName]:
                # collision avoidance
                selfnextop = self.route[self.sequence + 1]
                opCurr = opR.getCurrentPos()
                opOperate = opR.getOperatingPos()
                if selfnextop.posTuple() in [
                    opCurr.posTuple(),
                    opOperate.posTuple(),
                ]:
                    # facing check
                    if facingEach(selfnextop, opCurr) or facingEach(
                        selfnextop, opOperate
                    ):
                        # priority check with facing opponent
                        if self.priorThan(opR):
                            self.waitOperation(self.speed)
                            self.debug("wait when facing")
                        else:
                            # tempblocks
                            # self.tempBlocks.append(self.route[self.sequence+1].posTuple())
                            # newRoute = evaluateRoute(
                            #     self.route[self.sequence],
                            #     self.route[-1],
                            #     self.tempBlocks,
                            # )
                            newRoute = evaluateRoute(
                                self.route[self.sequence],
                                self.route[-1],
                                [self.route[self.sequence + 1].posTuple()],
                            )
                            if newRoute is None:
                                self.debug("error cannot route1")
                            else:
                                self.debug("repathfind when facing")
                                self.setRoute(newRoute)
                                self.doNextOperation()
                    # set new route against charging robot
                    elif opR.charging:
                        newRoute = evaluateRoute(
                            self.route[self.sequence],
                            self.route[-1],
                            [self.route[self.sequence + 1].posTuple()],
                        )
                        if newRoute is None:
                            self.debug("error cannot route2")
                        else:
                            self.setRoute(newRoute)
                            self.doNextOperation()
                    else:
                        self.waitOperation(self.speed)
                    return

            self.sequence += 1
            self.moveOperation(self.route[self.sequence].toViewPos().point())
