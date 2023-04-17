from random import randint
from time import time
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt, Signal, Slot

from cell import Cell, ChuteCell, StationCell, StationQueueCell
from db import queryMap
from pathfinding import Direction, NodePos, registerMap
from robot import Robot, Robot2

CELLSIZE = 100

cells2 = {'chute': [((2, 0), (0, 0)), ((2, 1), (0, 0)), ((2, 2), (0, 2))], 'workstation': [
    ((0, 1), [(2, 0), (2, 1), (2, 2)])], 'stationqueue': [((0, 0), (0, 1)), ((0, 2), (0, 1))]}
grid2 = (6, 6)
robots2 = [(NodePos(0, 0, Direction.W), 0), (NodePos(
    0, 1, Direction.W), 1), (NodePos(0, 2, Direction.N), 0)]


class SimulationWindow(QWidget):
    simulationFinished = Signal(float, int, int)

    def __init__(self, label) -> None:
        super().__init__(None)
        self.setWindowTitle('new simulation')
        '''
        todo: input
        robots:list[Robot]
        map
        
        del self -> use signal -> then parent class delete 
        '''

        self.time = time()

        self.simulationFinished.connect(self.foo)
        self.label = label

        self.setLayout(QHBoxLayout())
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.layout().addWidget(self.view)

        self.cells: list[Cell] = []
        self.robots: list[Robot] = []

        c, g = queryMap('test1')
        self.generateMap(c, g)
        # self.generateMap(cells2, grid2)
        # self.deployRobots(robots2)
        for r in robots2:
            self.deployRobot(r[0], r[1])
        # self.start()

        self.newbutton = QLabel(self)
        self.newbutton.setText('start')
        self.layout().addWidget(self.newbutton)

        self.efficiency = [0, 0]

        self.a = Robot2()
        self.scene.addItem(self.a)
        self.a.animation2()

    # example slot
    @Slot(float, int, int)
    def foo(self, fv, eff0, eff1):
        print("foo", fv)
        print("type0", eff0, "type1", eff1)

    def finishHandler(self):
        elapsed_time = time()-self.time

        self.simulationFinished.emit(
            elapsed_time, self.efficiency[0], self.efficiency[1])

    def closeEvent(self, event: QCloseEvent) -> None:
        self.label.setText(str(time()-self.time))
        self.finishHandler()

    @Slot(int, NodePos)
    def missionFinishHandler(self, num: int, type: int, position: NodePos):
        self.efficiency[type] += 1

        for cell in self.cells:
            if cell.pos().toPoint().toTuple() == position.point().toTuple():
                cell.assign(self.robots[num])
                return

        print("runtime fatal robotnum", num,
              "cell not found on", position)

    def start(self):
        self.time = time()

        for r in self.robots:
            r.signalObj.missionFinished.emit(
                r.robotNum, r.route[len(r.route)-1])

    def randomPackages(self, count: int, chutes: list[tuple[int, int]]):
        l = []
        for _ in range(count):
            l.append(chutes[randint(len(chutes))])
        return l

    # def deployRobots(self, posList: list[NodePos]):
    #     for p in posList:
    #         r = Robot(CELLSIZE, len(self.robots), p)
    #         r.signalObj.missionFinished.connect(self.missionFinishHandler)
    #         self.robots.append(r)
    #         self.scene.addItem(r)

    def deployRobot(self, pos, type):
        r = Robot(CELLSIZE, len(self.robots), pos, type)
        r.signalObj.missionFinished.connect(self.missionFinishHandler)
        self.robots.append(r)
        self.scene.addItem(r)

    def addCell(self, cell: Cell):
        self.scene.addItem(cell)
        self.cells.append(cell)

    def generateMap(self, cells: dict[str, list], grid: tuple[int, int]):
        registerMap(cells, grid)

        for i in range(grid[0]+1):
            self.scene.addLine(i*CELLSIZE, 0, i*CELLSIZE, grid[1]*CELLSIZE)
        for i in range(grid[1]+1):
            self.scene.addLine(0, i*CELLSIZE, grid[0]*CELLSIZE, i*CELLSIZE)

        # todo find nearest cell
        # or robot find nearest dest?
        # chute->workstation, charge->work ...
        for a, b in cells.items():
            if a == "chute":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.red))
                    print(self.cells[0].scene())
            elif a == "chargingstation":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.yellow))
            elif a == "workstation":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.green))
            elif a == "buffer":
                for c in b:
                    self.addCell(
                        Cell(c[0]*CELLSIZE, c[1]*CELLSIZE, CELLSIZE, CELLSIZE, Qt.blue))
            elif a == "block":
                for c in b:
                    print("add block", c)
