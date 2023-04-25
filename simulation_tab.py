from PySide6.QtWidgets import QLabel, QPushButton, QTabBar, QTabWidget
from graph import ThroughputBarChart
from simulation_info import SimulationInfo


class SimulationTab(QTabWidget):
    def __init__(self, graph: ThroughputBarChart, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.addTab(SimulationInfo(graph), 'run0')
        self.addTab(QLabel('addtabtab'), '+')
        self.tabBar().tabBarClicked.connect(self.addTabHandler)

    def addTabHandler(self, index):
        if index == self.count()-1:
            self.insertTab(
                self.count()-1, SimulationInfo(self.graph), f'run{self.count()-1}')
