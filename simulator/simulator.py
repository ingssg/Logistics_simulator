from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING
from random import randint
from time import sleep, time
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QWidget
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
CHARGE = "chargingstation"
BLOCK = "block"
CELL = "cell"

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

        self.robotInfoLabel = QLabel()
        self.robotInfoLabel.setText(f"=====ROBOT INFO=====")
        sideInfo_layout.addWidget(self.robotInfoLabel)

        self.robotNumLabel = QLabel()
        self.robotNumLabel.setText(f"Robot Num : None")
        sideInfo_layout.addWidget(self.robotNumLabel)

        self.robotDestLabel = QLabel()
        self.robotDestLabel.setText(f"Destination : None")
        sideInfo_layout.addWidget(self.robotDestLabel)

        self.robotPowLabel = QLabel()
        self.robotPowLabel.setText(f"Battery : None")
        sideInfo_layout.addWidget(self.robotPowLabel)

        self.robotChargingLabel = QLabel()
        self.robotChargingLabel.setText(f"isCharging  : None")
        sideInfo_layout.addWidget(self.robotChargingLabel)

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
        # changed = False
        changed = True
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
            self.getNearestWork(pos),
        )
        r.setParent(self)
        r.missionFinished.connect(self.missionFinishHandler)
        r.robotClicked.connect(self.displayRobotPanel)
        self.robots.append(r)
        self.scene.addItem(r)

    def displayRobotPanel(self, rn):
        r = self.robots[rn]
        self.robotNumLabel.setText(f"Robot Num : {r.robotNum}")
        self.robotDestLabel.setText(f"Destination : {r.dest}")
        self.robotPowLabel.setText(f"Battery : {r.power}")
        self.robotChargingLabel.setText(f"isCharging  : {r.charging}")

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

    def getNearestWork(self, src: NodePos):
        nodes, edges = gen()
        dist, prevs = dijkstra(nodes, edges, src)
        min = (None, float("inf"))
        for b in self.cells[WORK]:
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
        self.moveHistory.append((r, r.operatingPos))
        # self.moveHistory.append((r, r.currentPos, r.operatingPos))

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
            elif self.finished:
                r.setDest(self.getNearestEntrance(robotPos), 0)
                return
            else:
                r.setDest(self.getNearestWork(robotPos), 0)
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
            elif self.finished:
                r.setDest(self.getNearestEntrance(robotPos), 0)
                return
            else:
                r.charging = False
                r.setDest(self.getNearestWork(robotPos), 0)
                return

        else:
            print("mission finish error")

    def simulationFinishHandler(self):
        if self.finished:
            return

        self.loopTimer.stop()
        self.finished = True
        elapsed = time() - self.time
        process = [(r.robotType, r.processCount) for r in self.robots]
        self.timeSeries.append((elapsed, self.getTotalProcessed()))
        self.simulationFinished.emit(
            SimulationReport(self.windowTitle(), elapsed, process, self.timeSeries, 0)
        )

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Simulation")
        confirmation.setText(f"Simulation {self.windowTitle()} finished.")
        confirmation.setStandardButtons(QMessageBox.Ok)
        confirmation.setDefaultButton(QMessageBox.Ok)
        confirmation.exec()

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

        self.moveHistory: list[tuple[Robot, NodePos]] = []
        # self.moveHistory: list[tuple[Robot, NodePos, NodePos]] = []
        self.errorFlag = False
        self.errorHold = None
        # self.booked = [r.currentPos.posTuple() for r in self.robots]
        self.errors = 0

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

        tempCount = 0

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
                        # not tested
                        # tempnext=evaluateRoute(r.currentPos,r.dest,[nextPos.posTuple()])
                        # if tempnext is None:
                        #     continue
                        # else:
                        #     r.operatingPos=tempnext[1]
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

            if temp:
                delayed = [o for o in delayed if o not in temp]
            else:
                tempCount += 1

            if tempCount > 2:
                self.errorFlag = True
                self.errors += 1

                for o in worked:
                    o.operatingPos = o.currentPos
                delayed.extend(worked)
                worked = []
                self.errorHold = delayed[0]
                break

        if not self.errorFlag:
            for r in worked:
                self.pushHistory(r)
                r.doConveyOperation(r.operatingPos)

            if not self.finished:
                self.loopTimer.start(self.speed)
            return
        else:
            self.loopTimer.timeout.disconnect(self.loop)
            self.loopTimer.timeout.connect(self.errorLoop)
            self.loopTimer.start(self.speed)
            return

    def errorLoop(self):
        solved = False

        lastr, lastp = self.moveHistory.pop()
        print(f"error loop pop {lastr} {lastp}")
        if lastr != self.errorHold:
            self.rewind(lastr, lastp)

        booked = self.posList(self.robots, self.errorHold)
        route = evaluateRoute(self.errorHold.currentPos, self.errorHold.dest, booked)
        if route is not None:
            self.errorHold.operatingPos = route[1]
            solved = True
        else:
            nextPos = evaluateRoute(self.errorHold.currentPos, self.errorHold.dest)[1]
            if nextPos.posTuple() in self.posList(self.robots, self.errorHold):
                solved = False
            else:
                self.errorHold.operatingPos = nextPos
                solved = True

        if solved:
            self.errorFlag = False
            self.errorHold.doConveyOperation(self.errorHold.operatingPos)
            self.loopTimer.timeout.disconnect(self.errorLoop)
            self.loopTimer.timeout.connect(self.loop)
            self.loopTimer.start(self.speed)
        else:
            self.loopTimer.start(self.speed)

    def rewind(self, r: Robot, p: NodePos):
        r.setPos(p.toViewPos().point())
        r.setRotation(p.degree())
        r.currentPos = p
        r.operatingPos = p

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
