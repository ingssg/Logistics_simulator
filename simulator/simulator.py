from __future__ import annotations
from typing import TYPE_CHECKING
from random import randint
from time import time
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QCloseEvent, QIcon, QColor, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QTimer, Qt, Signal, Slot
from db.db import Warehouse, queryMap, colorText
from simulator.cell import Cell

if TYPE_CHECKING:
    from simulation.simulation_form import SimulationParameter
from simulation.simulation_observer import SimulationObserver, SimulationReport
from simulator.pathfinding import Direction, NodePos, evaluateRouteToCell, gen
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
        # for i in range(params.belt):
        #     self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 0)
        # for i in range(params.dump):
        #     self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 1)
        for i in range(params.belt + params.dump):
            if i == params.belt:
                self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 1)
            else:
                self.deployRobot(NodePos(*self.buffer[i].pos, Direction.E), 0)

        self.logistics = params.logistics

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

    @Slot(int, int, NodePos)
    def missionFinishHandler(self, num: int, type, position: NodePos):
        for cell in self.cells:
            if cell.nodeLoc == position.point().toTuple():
                rbt = self.robots[num]
                if cell.cellType == "chute":
                    nextcell = self.workstation[0].pos
                    route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
                    rbt.assignMission(route, 0)
                elif cell.cellType == "workstation":
                    self.logistics -= 1
                    randomindex = randint(0, len(self.chute) - 1)
                    nextcell = self.chute[randomindex].pos
                    route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
                    rbt.assignMission(route, 8)
                elif cell.cellType == "buffer":
                    nextcell = self.workstation[0].pos
                    route = evaluateRouteToCell(rbt.route[len(rbt.route) - 1], nextcell)
                    rbt.assignMission(route, 0)
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
            r.missionFinished.emit(r.robotNum, r.robotType, r.route[len(r.route) - 1])

        self.recorder.start(5000)

    def deployRobot(self, pos: NodePos, type: int):
        r = Robot(CELLSIZE, len(self.robots), type, pos, self.speed)
        r.setParent(self)
        r.missionFinished.connect(self.missionFinishHandler)
        self.robots.append(r)
        self.scene.addItem(r)

    def addCell(self, cell: Cell):
        self.cells.append(cell)
        self.scene.addItem(cell)

    def generateMap(self, map: Warehouse):
        for i in range(map.grid[0] + 1):
            self.scene.addLine(i * CELLSIZE, 0, i * CELLSIZE, map.grid[1] * CELLSIZE)
        for i in range(map.grid[1] + 1):
            self.scene.addLine(0, i * CELLSIZE, map.grid[0] * CELLSIZE, i * CELLSIZE)

        for c in map.cells:
            self.addCell(Cell(c.pos, c.outDir, c.cellType))
            
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
