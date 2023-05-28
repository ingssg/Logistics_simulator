from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING
from random import randint
from time import time
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QCloseEvent, QIcon, QColor, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QTimer, Qt, Signal, Slot
from db.db import CellData, Warehouse, queryMap, colorText
from simulator.cell import Cell

if TYPE_CHECKING:
    from simulation.simulation_form import SimulationParameter
from simulation.simulation_observer import SimulationObserver, SimulationReport
from simulator.pathfinding import (
    Direction,
    NodePos,
    dijkstra,
    evaluateRoute,
    evaluateRouteToCell,
    gen,
)
from simulator.robot import Robot

CELLSIZE = 100
SPEED = 500
CHARGEREQUIRED = 10
ERRORTHRESHOLD = 5

WORK = "workstation"
CHUTE = "chute"
BUFFER = "buffer"
CELL = "cell"
CHARGE = "chargingstation"
BLOCK = "block"

ENTER = "enter"


class Simulator(QWidget):
    simulationFinished = Signal(SimulationReport)

    def __init__(self, params: SimulationParameter) -> None:
        super().__init__(None)
        self.setWindowTitle(params.name)
        self.setWindowIcon(QIcon("./image/logo.png"))
        self.setGeometry(130, 50, 1000, 550)
        self.setStyleSheet("background-color:rgb(1,35,38); color:rgb(82,242,226);")

        self.setLayout(QHBoxLayout())
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.layout().addWidget(self.view)

        self.simulationFinished.connect(SimulationObserver.getInstance().forwardReport)

        self.cells: dict[str, list[Cell]] = {}
        self.workBufferDict: dict[tuple, list[Cell]] = {}
        self.robots: list[Robot] = []
        if params.speed == "1":
            self.speed = SPEED
        elif params.speed == "2":
            self.speed = SPEED // 2
        else:  # 0.5
            self.speed = SPEED * 2
        self.logistics = params.logistics
        self.logisticsLeft = params.logistics

        self.map = queryMap()
        self.generateMap(self.map)

        for w in self.cells[WORK]:
            self.trackBuffers(w)

        Robot._registry[self.windowTitle()] = []
        for i in range(params.belt + params.dump):
            t = 0 if i < params.belt else 1
            self.deployRobot(NodePos(*self.cells[BUFFER][i].nodeLoc, Direction.E), t)

        sideInfo = QWidget()
        sideInfo_layout = QVBoxLayout()
        sideInfo.setLayout(sideInfo_layout)
        sideInfo.setFixedSize(200, 500)
        # 빨강 : 2
        color1 = QColor(255, 0, 0)
        self.add_color_info(sideInfo_layout, color1, colorText(2))
        # 노랑 : 1
        color2 = QColor(255, 255, 0)
        self.add_color_info(sideInfo_layout, color2, colorText(1))
        # 초록 : 3
        color3 = QColor(0, 255, 0)
        self.add_color_info(sideInfo_layout, color3, colorText(3))
        # 파랑 : 4
        color4 = QColor(0, 0, 255)
        self.add_color_info(sideInfo_layout, color4, colorText(4))
        # 다크그레이 : 5
        color5 = QColor(169, 169, 169)
        self.add_color_info(sideInfo_layout, color5, colorText(5))

        self.logisticsLabel = QLabel(f"Left : {self.logisticsLeft}")
        sideInfo_layout.addWidget(self.logisticsLabel)

        self.layout().addWidget(sideInfo)

        self.start()

    def closeEvent(self, event: QCloseEvent):
        self.simulationFinishHandler()

    def generateMap(self, map: Warehouse):
        for c in map.cells:
            cell = Cell(c.pos, c.outDir, c.cellType)
            cell.setParent(self)
            if c.cellType not in self.cells:
                self.cells[c.cellType] = []
            self.cells[c.cellType].append(cell)
            self.scene.addItem(cell)

        self.cells[ENTER] = []
        for w in self.cells[WORK]:
            self.cells[ENTER].append(self.findLastBuffer(w))

        for i in range(map.grid[0] + 1):
            self.scene.addLine(i * CELLSIZE, 0, i * CELLSIZE, map.grid[1] * CELLSIZE)
        for i in range(map.grid[1] + 1):
            self.scene.addLine(0, i * CELLSIZE, map.grid[0] * CELLSIZE, i * CELLSIZE)

    # useless
    def findLastBuffer(self, w: Cell):
        hold = w
        p = w.nodeLoc
        changed = False
        while changed:
            changed = False
            for b in self.cells[BUFFER]:
                # n s w e
                # outdir n -> buffer should be s of workstation
                if (
                    (b.nodeLoc == (p[0], p[1] + 1) and b.outDirs == (1, 0, 0, 0))
                    or (b.nodeLoc == (p[0], p[1] - 1) and b.outDirs == (0, 1, 0, 0))
                    or (b.nodeLoc == (p[0] + 1, p[1]) and b.outDirs == (0, 0, 1, 0))
                    or (b.nodeLoc == (p[0] - 1, p[1]) and b.outDirs == (0, 0, 0, 1))
                ):
                    hold = b
                    p = b.nodeLoc
                    changed = True
                    break
        return hold

    def trackBuffers(self, work: Cell):
        self.workBufferDict[work.nodeLoc] = []
        hold = work
        p = work.nodeLoc
        added = True
        while added:
            added = False
            for b in self.cells[BUFFER]:
                if (
                    (b.nodeLoc == (p[0], p[1] + 1) and b.outDirs == (1, 0, 0, 0))
                    or (b.nodeLoc == (p[0], p[1] - 1) and b.outDirs == (0, 1, 0, 0))
                    or (b.nodeLoc == (p[0] + 1, p[1]) and b.outDirs == (0, 0, 1, 0))
                    or (b.nodeLoc == (p[0] - 1, p[1]) and b.outDirs == (0, 0, 0, 1))
                ):
                    hold = b
                    p = b.nodeLoc
                    self.workBufferDict[work.nodeLoc].append(hold)
                    added = True
                    break

    def deployRobot(self, pos: NodePos, type: int):
        r = Robot(
            CELLSIZE,
            len(self.robots),
            type,
            pos,
            self.speed,
            self.windowTitle(),
            self.getNearestEntrance(pos),
        )
        r.setParent(self)
        r.missionFinished.connect(self.missionFinishHandler)
        self.robots.append(r)
        self.scene.addItem(r)

    def findCell(self, pos: NodePos):
        for k, v in self.cells.items():
            for c in v:
                if c.nodeLoc == pos.posTuple():
                    return k, c
        return None, None

    def getNearestEntrance(self, src: NodePos):
        nodes, edges = gen()
        dist, prevs = dijkstra(nodes, edges, src)
        min = (None, float("inf"))
        for b in self.cells[ENTER]:
            if b.outDirs.index(1) == 0:
                dir = Direction.N
            elif b.outDirs.index(1) == 1:
                dir = Direction.S
            elif b.outDirs.index(1) == 2:
                dir = Direction.W
            elif b.outDirs.index(1) == 3:
                dir = Direction.E
            node = NodePos(*b.nodeLoc, dir)
            if dist[node] < min[1]:
                min = (node, dist[node])
        return min[0]

    def getTotalProcessed(self):
        return sum(r.processCount for r in self.robots)

    def pushHistory(self, r: Robot):
        if len(self.moveHistory) == len(self.robots) * ERRORTHRESHOLD**3:
            self.moveHistory.pop(0)
        self.moveHistory.append((r, r.currentPos, r.operatingPos))

    def missionFinishHandler(self, robotNum: int, robotPos: NodePos):
        t, c = self.findCell(robotPos)
        r = self.robots[robotNum]

        if t == CHUTE:
            r.processCount += 1
            r.box = 0
            r.dumpPixmap(0)

            if self.logistics == sum([r.processCount for r in self.robots]):
                self.simulationFinishHandler()
                # do nothing
                return

            if r.power < CHARGEREQUIRED:
                charge = [c for c in self.cells[CHARGE] if not c.occupied][0]
                r.setDest(evaluateRouteToCell(robotPos, charge.nodeLoc)[-1], 0)
                charge.occupy()
                return
            else:
                r.setDest(self.getNearestEntrance(robotPos), 0)
                return

        elif t == WORK:
            if self.logisticsLeft == 0:
                r.stopped = True
                return

            destChute = self.cells[CHUTE][
                randint(0, len(self.cells[CHUTE]) - 1)
            ].nodeLoc
            n = evaluateRouteToCell(robotPos, destChute)
            r.setDest(n[-1], 8)
            self.logisticsLeft -= 1
            self.logisticsLabel.setText(f"Left : {self.logisticsLeft}")
            return

        elif t == BUFFER:
            nextPos = deepcopy(robotPos)
            if c.outDirs[0] == 1:
                nextPos.y -= 1
                nextPos.direction = Direction.N
            elif c.outDirs[1] == 1:
                nextPos.y += 1
                nextPos.direction = Direction.S
            elif c.outDirs[2] == 1:
                nextPos.x -= 1
                nextPos.direction = Direction.W
            elif c.outDirs[3] == 1:
                nextPos.x += 1
                nextPos.direction = Direction.E
            else:
                print("data error")
            r.setDest(nextPos, 0)
            return

        elif t == CHARGE:
            if r.power < CHARGEREQUIRED:
                # r.charge()
                r.charging = True
                r.power += 1
                return
            else:
                r.charging = False
                r.setDest(self.getNearestEntrance(robotPos), 0)
                return

        else:
            print("mission finish error")

    def simulationFinishHandler(self):
        self.loopTimer.stop()
        self.finished = True
        elapsed = time() - self.time
        process = [(r.robotType, r.processCount) for r in self.robots]
        self.timeSeries.append((elapsed, self.getTotalProcessed()))
        self.simulationFinished.emit(
            SimulationReport(self.windowTitle(), elapsed, process, self.timeSeries, 0)
        )
        print("alert simulation finished")

    def start(self):
        self.finished = False

        self.time = time()
        self.timeSeries = [(0, 0)]
        self.recorder = QTimer(self)
        self.recorder.timeout.connect(
            lambda: self.timeSeries.append(
                (len(self.timeSeries) * 5, self.getTotalProcessed())
            )
        )
        self.recorder.start(5000)

        self.moveHistory: list[tuple[Robot, NodePos, NodePos]] = []
        self.errorFlag = False
        self.errorHold = None
        # self.booked = [r.currentPos.posTuple() for r in self.robots]

        self.loopTimer = QTimer(self)
        self.loopTimer.setSingleShot(True)
        self.loopTimer.timeout.connect(self.loop)
        self.loop()

    def posList(self, l: list[Robot], r: Robot):
        return [
            o.operatingPos.posTuple()
            for o in l
            if o.operatingPos.posTuple() != r.currentPos.posTuple()
        ]

    def loop(self):
        delayed: list[Robot] = [r for r in self.robots if not r.stopped]
        worked: list[Robot] = [r for r in self.robots if r.stopped]

        temp = []
        for r in delayed:
            r.currentPos = r.operatingPos
            if r.currentPos == r.dest or r.charging:
                temp.append(r)
                worked.append(r)
                self.missionFinishHandler(r.robotNum, r.currentPos)
        delayed = [o for o in delayed if o not in temp]

        while delayed:
            temp = []
            for r in delayed:
                booked = self.posList(self.robots, r)
                route = evaluateRoute(r.currentPos, r.dest, booked)

                if route is not None:
                    r.operatingPos = route[1]
                    temp.append(r)
                    worked.append(r)
                    continue
                else:
                    nextPos = evaluateRoute(r.currentPos, r.dest)[1]
                    if nextPos.posTuple() in self.posList(delayed, r):
                        continue
                    elif nextPos.posTuple() in self.posList(worked, r):
                        temp.append(r)
                        worked.append(r)
                        continue
                    else:
                        r.operatingPos = nextPos
                        temp.append(r)
                        worked.append(r)
                        continue

            # 이 delayed를 사용해서 할수 있을거 같은데?
            if temp:
                delayed = [o for o in delayed if o not in temp]
            else:
                pass

        for r in worked:
            self.pushHistory(r)
            r.doConveyOperation(r.operatingPos)

        if not self.finished:
            self.loopTimer.start(self.speed)
        return

    # def loop(self):
    #     activated = [r for r in self.robots if not r.stopped]
    #     allBooked = []
    #     if self.errorFlag:
    #         for r in self.robots:
    #             allBooked.extend([r.currentPos.posTuple(), r.operatingPos.posTuple()])
    #     else:
    #         for r in self.robots:
    #             r.currentPos = r.operatingPos
    #             allBooked.append(r.currentPos.posTuple())

    #     allBooked = list(set(allBooked))

    #     # error handling #
    #     # self.robots 우선순위 순으로 재정렬?
    #     # if error situation happens:
    #     # grab the robot -> errored=r
    #     # break the loop
    #     # reorder self.robots -> errored robot is 0th
    #     # rewind via movehistory until grabbed robot moves
    #     # if mitigated, restart loop

    #     if self.errorFlag:
    #         print(self.errorHold.robotNum)
    #         last = self.moveHistory.pop()
    #         lastRobot = last[0]

    #         if lastRobot.robotNum == self.errorHold.robotNum:
    #             self.loopTimer.start(self.speed)
    #             return

    #         # self.errorHold = activated[0]
    #         self.errorHold.waitCount = 0
    #         r = self.errorHold

    #         booked = list(filter(lambda x: x != r.currentPos.posTuple(), allBooked))
    #         for op in Robot._registry[r.simulName]:
    #             if op.robotNum == r.robotNum:
    #                 continue
    #             booked.append(op.operatingPos.posTuple())
    #         booked = list(set(booked))

    #         # lastRobot.doConveyOperation(last[1])
    #         lastRobot.setPos(last[1].toViewPos().x, last[1].toViewPos().y)
    #         lastRobot.setRotation(last[1].degree())
    #         # if lastRobot.currentPos.posTuple()==lastRobot.operatingPos.posTuple():
    #         # 아직 이동명령을 안받았음
    #         # last[2] 가 current 임

    #         lastRobot.waitCount = 0
    #         lastRobot.currentPos = last[1]
    #         lastRobot.operatingPos = last[1]
    #         booked.remove(last[2].posTuple())
    #         booked.append(last[1].posTuple())
    #         allBooked.remove(last[2].posTuple())
    #         allBooked.append(last[1].posTuple())
    #         booked = list(set(booked))
    #         allBooked = list(set(allBooked))

    #         route = evaluateRoute(r.currentPos, r.dest, booked)
    #         if route is not None:
    #             self.errorFlag = False
    #         else:
    #             if r.routeCache:
    #                 curr = r.routeCache.index(r.currentPos)
    #                 nextPos = r.routeCache[curr + 1]
    #             else:
    #                 nextPos = evaluateRoute(r.currentPos, r.dest)[1]

    #             if nextPos.posTuple() in booked:
    #                 print(r.robotNum, nextPos.posTuple(), booked)
    #                 self.errorFlag = True
    #             else:
    #                 self.errorFlag = False
    #     ### error handling###

    #     if self.errorFlag:
    #         self.loopTimer.start(self.speed)
    #         return
    #     else:
    #         # print("error escaped")
    #         pass

    #     for r in activated:
    #         ### error detection ###
    #         if r.waitCount > ERRORTHRESHOLD:
    #             self.errorFlag = True
    #             self.errorHold = r
    #             # reset waitcount
    #             for t in self.robots:
    #                 # t.waitCount = 0
    #                 t.routeCache = []
    #             self.robots = [t for t in self.robots if t.robotNum != r.robotNum]
    #             self.robots.insert(0, r)
    #             break

    #         if (self.errorHold is not None) and (r.robotNum == self.errorHold.robotNum):
    #             # self.errorFlag = False
    #             self.errorHold = None
    #         ### error detection ###

    #         ### move operation assignment ###
    #         if r.currentPos == r.dest or r.charging:
    #             self.missionFinishHandler(r.robotNum, r.currentPos)

    #             t, c = self.findCell(r.currentPos)
    #             if t == WORK and r.box > 0:
    #                 print(f"current==dest work {r.currentPos} {r.dest}")
    #             # r.waitOperation()
    #             continue

    #         booked = list(filter(lambda x: x != r.currentPos.posTuple(), allBooked))
    #         for op in Robot._registry[r.simulName]:
    #             if op.robotNum == r.robotNum:
    #                 continue
    #             booked.append(op.operatingPos.posTuple())
    #         booked = list(set(booked))

    #         route = evaluateRoute(r.currentPos, r.dest, booked)
    #         if route is not None:
    #             r.routeCache = route
    #             r.operatingPos = route[1]
    #         else:
    #             if r.routeCache:
    #                 curr = r.routeCache.index(r.currentPos)
    #                 nextPos = r.routeCache[curr + 1]
    #             else:
    #                 nextPos = evaluateRoute(r.currentPos, r.dest)[1]

    #             if nextPos.posTuple() in booked:
    #                 r.waitOperation()
    #                 continue
    #             else:
    #                 r.operatingPos = nextPos

    #         allBooked.remove(r.currentPos.posTuple())
    #         allBooked.append(r.operatingPos.posTuple())
    #         self.pushHistory(r)
    #         r.doConveyOperation(r.operatingPos)
    #         continue

    #     if not self.finished:
    #         self.loopTimer.start(self.speed)
    #     return

    def add_color_info(self, layout, color, text):
        color_layout = QHBoxLayout()
        color_label = QLabel()
        color_label.setStyleSheet(f"background-color: {color.name()};")
        color_label.setFixedSize(50, 50)
        color_layout.addWidget(color_label)
        label = QLabel(text)
        font = QFont()
        font.setPointSize(15)
        label.setFont(font)
        color_layout.addWidget(label)
        color_layout.setStretchFactor(color_label, 1)
        color_layout.setStretchFactor(QLabel(text), 3)
        layout.addLayout(color_layout)
        layout.setSpacing(3)
