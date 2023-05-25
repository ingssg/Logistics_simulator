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

    def deployRobot(self, pos: NodePos, type: int):
        r = Robot(CELLSIZE, len(self.robots), type, pos, self.speed, self.windowTitle())
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
        if len(self.moveHistory) == len(self.robots) * 3:
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
                # self.close()
                return

            if r.power < CHARGEREQUIRED:
                charge = [c for c in self.cells[CHARGE] if not c.occupied][0]
                r.am(evaluateRouteToCell(robotPos, charge.nodeLoc)[-1], 0)
                charge.occupy()
                return
            else:
                r.am(self.getNearestEntrance(robotPos), 0)
                return
        elif t == WORK:
            if self.logisticsLeft == 0:
                return

            destChute = self.cells[CHUTE][
                randint(0, len(self.cells[CHUTE]) - 1)
            ].nodeLoc
            r.am(evaluateRouteToCell(robotPos, destChute)[-1], 8)
            self.logisticsLeft -= 1
            self.logisticsLabel.setText(f"Left : {self.logisticsLeft}")
            return
        elif t == CHARGE:
            if r.power < CHARGEREQUIRED:
                # r.charge()
                r.charging = True
                r.power += 1
                return
            else:
                r.am(self.getNearestEntrance(robotPos), 0)
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

            r.am(nextPos, 0)
            return
        else:
            print("mission finish error")

    def simulationFinishHandler(self):
        self.finished = True
        elapsed = time() - self.time
        process = [(r.robotType, r.processCount) for r in self.robots]
        self.timeSeries.append((elapsed, self.getTotalProcessed()))
        self.simulationFinished.emit(
            SimulationReport(self.windowTitle(), elapsed, process, self.timeSeries, 0)
        )

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

        self.loopTimer = QTimer(self)
        self.loopTimer.setSingleShot(True)
        self.loopTimer.timeout.connect(self.loop)

        self.loopTimer.start(self.speed)

    def loop(self):
        allBooked = []

        for r in self.robots:
            r.currentPos = r.operatingPos
            allBooked.append(r.currentPos.posTuple())

        # self.robots 우선순위 순으로 재정렬?

        for r in self.robots:
            if r.currentPos == r.dest:
                self.missionFinishHandler(r.robotNum, r.currentPos)

                if r.charging:
                    r.waitOperation()
                    continue

            booked = list(filter(lambda x: x != r.currentPos.posTuple(), allBooked))
            for opRobot in Robot._registry[r.simulName]:
                if opRobot.robotNum == r.robotNum:
                    continue
                booked.append(
                    opRobot.operatingPos.posTuple(),
                )
            booked = list(set(booked))

            route = evaluateRoute(r.currentPos, r.dest, booked)
            if route is not None:
                r.routeCache = route
                r.operatingPos = route[1]
                allBooked.append(r.operatingPos.posTuple())
                r.doConveyOperation(r.operatingPos)
                self.pushHistory(r)
                continue
            else:
                if r.routeCache:
                    curr = r.routeCache.index(r.currentPos)
                    nextPos = r.routeCache[curr + 1]
                else:
                    nextPos = evaluateRoute(r.currentPos, r.dest)[1]
                    if nextPos.posTuple() in booked:
                        r.waitOperation()
                        continue
                    else:
                        r.operatingPos = nextPos
                        allBooked.append(r.operatingPos.posTuple())
                        r.doConveyOperation(r.operatingPos)
                        self.pushHistory(r)
                        continue

        if not self.finished:
            self.loopTimer.start(self.speed)

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

    # @Slot(int, NodePos)
    # def missionFinishHandler(self, num: int, position: NodePos):
    #     for cell in self.cells:
    #         if cell.nodeLoc == position.point().toTuple():
    #             rbt = self.robots[num]

    #             if cell.cellType == "chute":
    #                 if self.logistics == sum([r.processCount for r in self.robots]):
    #                     self.simulationFinishHandler()
    #                     self.close()
    #                     return
    #                 if self.robots[num].power < 10:
    #                     charges = list(
    #                         filter(
    #                             lambda x: x.cellType == "chargingstation"
    #                             and not x.occupied,
    #                             self.cells,
    #                         )
    #                     )
    #                     nodes, edges = gen()
    #                     dist, prevs = dijkstra(nodes, edges, position)
    #                     min = (None, float("inf"))
    #                     for c in charges:
    #                         node = NodePos(*c.nodeLoc, Direction.N)
    #                         if dist[node] < min[1]:
    #                             min = (node, dist[node])
    #                     selected = [
    #                         c for c in charges if c.nodeLoc == min[0].posTuple()
    #                     ]
    #                     selected[0].occupy()
    #                     route = evaluateRoute(position, min[0])
    #                     rbt.assignMission(route, 0)
    #                     return
    #                 nextcell = self.findNearestEntrance(position, self.buffer)
    #                 route = evaluateRoute(position, nextcell)
    #                 rbt.assignMission(route, 0)
    #             elif cell.cellType == "workstation":
    #                 if self.logisticsLeft == 0:
    #                     return
    #                 randomindex = randint(0, len(self.chute) - 1)
    #                 nextcell = self.chute[randomindex].pos
    #                 route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
    #                 rbt.assignMission(route, 8)
    #                 self.logisticsLeft -= 1
    #                 self.logisticsLabel.setText(f"Left : {self.logisticsLeft}")
    #             elif cell.cellType == "buffer":
    #                 nextcell = self.workstation[0].pos
    #                 route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
    #                 rbt.assignMission(route, 0)
    #             elif cell.cellType == "chargingstation":
    #                 if rbt.power < 20:
    #                     # rbt.chargeOperation(cell)
    #                     rbt.setRoute(rbt.route[-1:])
    #                     rbt.charge()
    #                     return
    #                 nextcell = self.findNearestEntrance(position, self.buffer)
    #                 route = evaluateRoute(position, nextcell)
    #                 rbt.assignMission(route, 0)
    #                 cell.deOccupy()
    #             else:
    #                 print("runtime fatal robotnum", num, "cell not found on", position)
