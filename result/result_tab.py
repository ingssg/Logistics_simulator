from PySide6.QtCore import Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QTabBar, QTabWidget
from result.result_table import ResultTable
from result.throughput_robot import ThroughputRobot
from result.throughput_time import ThroughputTime
from simulation.simulation_form import SimulationForm
from simulation.simulation_observer import SimulationObserver, SimulationReport


class ResultTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        observer = SimulationObserver.getInstance()
        observer.simulationReported.connect(self.addResult)
        observer.simulationRemoved.connect(self.removeCharts)

        self.setFont(QFont('나눔고딕 ExtraBold', 10))

    @Slot(SimulationReport)
    def addResult(self, report: SimulationReport):
        self.addTab(ResultTable(report), f"{report.name} - Result")
        self.addTab(ThroughputRobot(report), f"{report.name} - Robot")
        self.addTab(ThroughputTime(report), f"{report.name} - TimeSeries")

    @Slot(int)
    def removeCharts(self, index):
        self.removeTab(index * 2)
        self.removeTab(index * 2)
