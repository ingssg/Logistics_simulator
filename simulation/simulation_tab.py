from PySide6.QtWidgets import QLabel, QPushButton, QTabBar, QTabWidget
from simulation.simulation_form import SimulationForm
from simulation.simulation_observer import SimulationObserver


class SimulationTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addTab(SimulationForm(), 'run0')
        self.addTab(QLabel('addtabtab'), '+')
        self.tabBar().tabBarClicked.connect(self.addTabHandler)
        self.tabCloseRequested.connect(self.removeTabHandler)

    def addTabHandler(self, index):
        if index == self.count()-1:
            self.insertTab(
                self.count()-1, SimulationForm(), f'run{self.count()-1}')

    def removeTabHandler(self, index):
        self.removeTab(index)
        SimulationObserver.getInstance().forwardRemoved(index)
