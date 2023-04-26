from random import randint
from time import time
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QTimer, Qt, Signal, Slot
from db.db import queryMap
from simulation.simulation_observer import SimulationObserver, SimulationReport
from simulator.pathfinding import Direction, NodePos, evaluateRouteToCell, registerMap
from simulator.robot import Robot
from simulator.cell import Cell

CELLSIZE = 100

cells2 = {'chute': [((2, 0), (0, 0)), ((2, 1), (0, 0)), ((2, 2), (0, 2))], 'workstation': [
    ((0, 1), [(2, 0), (2, 1), (2, 2)])], 'stationqueue': [((0, 0), (0, 1)), ((0, 2), (0, 1))]}
grid2 = (6, 6)
robots2 = [(NodePos(0, 0, Direction.W), 0), (NodePos(
    0, 1, Direction.W), 1), (NodePos(0, 2, Direction.N), 0)]

'''
i think...
just stop the simulation window and not delete (garbage collect)

the window will be deleted...
if tab of the main window is closed
'''


class Simulator(QWidget):
    simulationFinished = Signal(SimulationReport)

    def __init__(self, simulationName, mapName='test2') -> None:
        super().__init__(None)
        self.setWindowTitle(simulationName)
        self.setLayout(QHBoxLayout())

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.layout().addWidget(self.view)

        self.simulationFinished.connect(
            SimulationObserver.getInstance().forwardReport)

        self.infoLabel = QLabel(self)
        self.infoLabel.setText('some information here')
        self.layout().addWidget(self.infoLabel)

        self.cells: list[Cell] = []
        self.robots: list[Robot] = []
        # self.throughput = [0, 0]
        self.time = time()

        # self.generateMap(cells2, grid2)
        # self.deployRobots(robots2)

        self.cellsDBRaw, g = queryMap(mapName)
        self.generateMap(self.cellsDBRaw, g)
        # for r in robots2:
        #     self.deployRobot(r[0], r[1])

        c = self.cellsDBRaw['buffer']
        self.deployRobot(NodePos(c[0][0], c[0][1], Direction.E), 0)
        # self.deployRobot(NodePos(c[1][0], c[1][1], Direction.E), 1)

        self.start()

    def simulationFinishHandler(self):
        elapsed = time()-self.time

        process = [r.processCount for r in self.robots]

        report = SimulationReport(
            self.windowTitle(), elapsed, process, self.timeSeries)
        self.simulationFinished.emit(report)

    def closeEvent(self, event: QCloseEvent):
        self.simulationFinishHandler()

    # @Slot(int,int)
    # def conveyedHandler(self, robotType,robotNum):
    #     self.throughput[robotType] += 1
    #     if robotType==0:

    @Slot(int, int, NodePos)
    def missionFinishHandler(self, num: int, type: int, position: NodePos):
        for cell in self.cells:
            if cell.coordinate == position.point().toTuple():
                rbt = self.robots[num]
                if cell.cellType == "chute":
                    print('chute', position)
                    nextcell = self.cellsDBRaw['workstation'][0]
                    route = evaluateRouteToCell(
                        rbt.route[len(rbt.route)-1], nextcell)
                    rbt.assignMission(route, 0)
                elif cell.cellType == 'workstation':
                    print('work', position)
                    randomindex = randint(0, len(self.cellsDBRaw['chute'])-1)
                    nextcell = self.cellsDBRaw['chute'][randomindex]
                    route = evaluateRouteToCell(
                        rbt.route[len(rbt.route)-1], nextcell)
                    rbt.assignMission(route, 8)
                elif cell.cellType == 'buffer':
                    print('buffer', position)
                    nextcell = self.cellsDBRaw['workstation'][0]
                    route = evaluateRouteToCell(
                        rbt.route[len(rbt.route)-1], nextcell)
                    rbt.assignMission(route, 0)
                else:
                    print("runtime fatal robotnum", num,
                          "cell not found on", position)

    def start(self):
        self.time = time()

        self.timeSeries = [(0, 0)]
        self.recorder = QTimer(self)
        self.recorder.timeout.connect(lambda: self.timeSeries.append(
            (len(self.timeSeries)*5, randint(0, 5))))
        self.recorder.start(5000)

        for r in self.robots:
            r.missionFinished.emit(
                r.robotNum, r.robotType, r.route[len(r.route)-1])

    def randomPackages(self, count: int, chutes: list[tuple[int, int]]):
        l = []
        for _ in range(count):
            l.append(chutes[randint(len(chutes))])
        return l

    def deployRobot(self, pos: NodePos, type: int):
        r = Robot(CELLSIZE, len(self.robots), type, pos)
        r.missionFinished.connect(self.missionFinishHandler)
        self.robots.append(r)
        self.scene.addItem(r)

    def addCell(self, cell: Cell):
        self.cells.append(cell)
        self.scene.addItem(cell)

    def generateMap(self, cells: dict[str, list], grid: tuple[int, int]):
        registerMap(cells, grid)

        for i in range(grid[0]+1):
            self.scene.addLine(i*CELLSIZE, 0, i*CELLSIZE, grid[1]*CELLSIZE)
        for i in range(grid[1]+1):
            self.scene.addLine(0, i*CELLSIZE, grid[0]*CELLSIZE, i*CELLSIZE)

        for a, b in cells.items():
            if a == "chute":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.red, 'chute'))
            elif a == "chargingstation":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.yellow, "chargingstation"))
            elif a == "workstation":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.green, 'workstation'))
            elif a == "buffer":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.blue, "buffer"))
            elif a == "block":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.gray, 'blocked'))
