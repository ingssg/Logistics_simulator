from PySide6.QtWidgets import QLabel, QPushButton, QTabBar, QTabWidget
from simulation.simulation_info import SimulationInfo


class SimulationTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addTab(SimulationInfo(), 'run0')
        self.addTab(QLabel('addtabtab'), '+')
        self.tabBar().tabBarClicked.connect(self.addTabHandler)

    def addTabHandler(self, index):
        if index == self.count()-1:
            self.insertTab(
                self.count()-1, SimulationInfo(), f'run{self.count()-1}')
