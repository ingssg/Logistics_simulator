from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel, QPushButton, QTabBar, QTabWidget
from result.throughput_robot import ThroughputRobot
from result.throughput_time import ThroughputTime
from simulation.simulation_info import SimulationInfo
from simulation.simulation_observer import SimulationObserver, SimulationReport


class ResultTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        SimulationObserver.getInstance().simulationReported.connect(self.addResult)

    @Slot(SimulationReport)
    def addResult(self, report: SimulationReport):
        self.addTab(ThroughputRobot(report), f'{report.name} - Robot')
        self.addTab(ThroughputTime(report), f'{report.name} - TimeSeries')
