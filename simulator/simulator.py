from __future__ import annotations
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

        self.cells: list[Cell] = []
        self.robots: list[Robot] = []

        self.map = queryMap()
        self.generateMap(self.map)

        if params.speed == "1":
            self.speed = SPEED
        elif params.speed == "2":
            self.speed = SPEED // 2
        else:  # 0.5
            self.speed = SPEED * 2

        self.workstation = list(
            filter(lambda c: c.cellType == "workstation", self.map.cells)
        )
        self.chute = list(filter(lambda c: c.cellType == "chute", self.map.cells))
        self.buffer = list(filter(lambda c: c.cellType == "buffer", self.map.cells))
        self.chargingstation = list(
            filter(lambda c: c.cellType == "chargingstation", self.map.cells)
        )

        Robot._registry[self.windowTitle()] = []
        for i in range(params.belt + params.dump):
            if i == params.belt:
                self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 1)
            else:
                self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 0)

        # self.deployRobot(NodePos(0, 1, 1), 1)

        self.logistics = params.logistics
        self.logisticsLeft = params.logistics

        self.lastbuffers = [self.findLastBuffer(w) for w in self.workstation]

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

    def simulationFinishHandler(self):
        elapsed = time() - self.time
        process = [(r.robotType, r.processCount) for r in self.robots]
        self.simulationFinished.emit(
            SimulationReport(self.windowTitle(), elapsed, process, self.timeSeries, 0)
        )

    def closeEvent(self, event: QCloseEvent):
        self.simulationFinishHandler()

    @Slot(int, NodePos)
    def missionFinishHandler(self, num: int, position: NodePos):
        for cell in self.cells:
            if cell.nodeLoc == position.point().toTuple():
                rbt = self.robots[num]

                if cell.cellType == "chute":
                    if self.logistics == sum([r.processCount for r in self.robots]):
                        self.simulationFinishHandler()
                        self.close()
                        return
                    if self.robots[num].power < 10:
                        charges = list(
                            filter(
                                lambda x: x.cellType == "chargingstation"
                                and not x.occupied,
                                self.cells,
                            )
                        )
                        nodes, edges = gen()
                        dist, prevs = dijkstra(nodes, edges, position)
                        min = (None, float("inf"))
                        for c in charges:
                            node = NodePos(*c.nodeLoc, Direction.N)
                            if dist[node] < min[1]:
                                min = (node, dist[node])
                        selected = [
                            c for c in charges if c.nodeLoc == min[0].posTuple()
                        ]
                        selected[0].occupy()
                        route = evaluateRoute(position, min[0])
                        rbt.assignMission(route, 0)
                        return
                    nextcell = self.findNearestEntrance(position, self.buffer)
                    route = evaluateRoute(position, nextcell)
                    rbt.assignMission(route, 0)
                elif cell.cellType == "workstation":
                    if self.logisticsLeft == 0:
                        return
                    randomindex = randint(0, len(self.chute) - 1)
                    nextcell = self.chute[randomindex].pos
                    route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
                    rbt.assignMission(route, 8)
                    self.logisticsLeft -= 1
                    self.logisticsLabel.setText(f"Left : {self.logisticsLeft}")
                elif cell.cellType == "buffer":
                    nextcell = self.workstation[0].pos
                    route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
                    rbt.assignMission(route, 0)
                elif cell.cellType == "chargingstation":
                    if rbt.power < 20:
                        # rbt.chargeOperation(cell)
                        rbt.setRoute(rbt.route[-1:])
                        rbt.charge()
                        return
                    nextcell = self.findNearestEntrance(position, self.buffer)
                    route = evaluateRoute(position, nextcell)
                    rbt.assignMission(route, 0)
                    cell.deOccupy()
                else:
                    print("runtime fatal robotnum", num, "cell not found on", position)

    def start(self):
        self.time = time()
        self.timeSeries = [(0, 0)]
        self.recorder = QTimer(self)
        self.recorder.timeout.connect(
            lambda: self.timeSeries.append(
                (len(self.timeSeries) * 5, sum(r.processCount for r in self.robots))
            )
        )

        for r in self.robots:
            r.missionFinished.emit(r.robotNum, r.route[len(r.route) - 1])

        self.recorder.start(5000)

    def deployRobot(self, pos: NodePos, type: int):
        r = Robot(CELLSIZE, len(self.robots), type, pos, self.speed, self.windowTitle())
        r.setParent(self)
        r.missionFinished.connect(self.missionFinishHandler)
        self.robots.append(r)
        self.scene.addItem(r)

    def generateMap(self, map: Warehouse):
        for i in range(map.grid[0] + 1):
            self.scene.addLine(i * CELLSIZE, 0, i * CELLSIZE, map.grid[1] * CELLSIZE)
        for i in range(map.grid[1] + 1):
            self.scene.addLine(0, i * CELLSIZE, map.grid[0] * CELLSIZE, i * CELLSIZE)

        for c in map.cells:
            cell = Cell(c.pos, c.outDir, c.cellType)
            cell.setParent(self)
            self.cells.append(cell)
            self.scene.addItem(cell)

    def findLastBuffer(self, w: CellData):
        hold = w
        p = w.pos
        changed = False

        while changed:
            changed = False
            for b in self.buffer:
                # n s w e
                # outdir n -> buffer should be s of workstation
                if (
                    (b.pos == (p[0], p[1] + 1) and b.outDir == (1, 0, 0, 0))
                    or (b.pos == (p[0], p[1] - 1) and b.outDir == (0, 1, 0, 0))
                    or (b.pos == (p[0] + 1, p[1]) and b.outDir == (0, 0, 1, 0))
                    or (b.pos == (p[0] - 1, p[1]) and b.outDir == (0, 0, 0, 1))
                ):
                    hold = b
                    p = b.pos
                    changed = True

        return hold

    # 이거 if문 왜있나 했더니
    """
    처음에 버퍼 찾으려고 했던거라 있음
    차지스테이션 찾을때는 다른함수 써야됨
    이거 아예 Cell객체 쓰는 함수로 바꾸자
    Cell에 outdir넣어줘야함
    """

    def findNearestEntrance(self, src: NodePos, cellDatas: list[CellData]):
        nodes, edges = gen()
        dist, prevs = dijkstra(nodes, edges, src)
        min = (None, float("inf"))
        for b in cellDatas:
            if b.outDir.index(1) == 0:
                dir = Direction.N
            elif b.outDir.index(1) == 1:
                dir = Direction.S
            elif b.outDir.index(1) == 2:
                dir = Direction.W
            elif b.outDir.index(1) == 3:
                dir = Direction.E
            node = NodePos(*b.pos, dir)
            if dist[node] < min[1]:
                min = (node, dist[node])
        return min[0]

    # def findNearestEntrance(self, src: NodePos,cellDatas:list[CellData]):
    #     nodes, edges = gen()
    #     dist, prevs = dijkstra(nodes, edges, src)
    #     min = (None, float("inf"))
    #     for b in self.lastbuffers:
    #         if b.outDir.index(1) == 0:
    #             dir = Direction.N
    #         elif b.outDir.index(1) == 1:
    #             dir = Direction.S
    #         elif b.outDir.index(1) == 2:
    #             dir = Direction.W
    #         elif b.outDir.index(1) == 3:
    #             dir = Direction.E
    #         node = NodePos(*b.pos, dir)
    #         if dist[node] < min[1]:
    #             min = (node, dist[node])
    #     return min[0]

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
