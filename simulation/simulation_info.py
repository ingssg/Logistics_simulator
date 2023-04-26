from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from simulator.simulator import Simulator
if TYPE_CHECKING:
    from simulation.simulation_tab import SimulationTab

from PySide6.QtWidgets import QFormLayout, QLineEdit, QPushButton, QWidget


class SimulationInfo(QWidget):
    def __init__(self, parent: SimulationTab = None):
        super().__init__(parent)
        form_layout = QFormLayout(self)

        name_field = QLineEdit(self)
        form_layout.addRow('Name', name_field)
        belt_field = QLineEdit(self)
        form_layout.addRow('Belt', belt_field)
        dump_field = QLineEdit(self)
        form_layout.addRow('Dump', dump_field)
        logistic_field = QLineEdit(self)
        form_layout.addRow('Logistics', logistic_field)
        interval_field = QLineEdit(self)
        form_layout.addRow('Record Interval', interval_field)
        start_button = QPushButton('Start Simulation', self)
        form_layout.addRow(start_button)
        remove_button = QPushButton('Remove Simulation', self)
        form_layout.addRow(remove_button)

        start_button.clicked.connect(
            lambda: self.startSimulation(name_field.text()))
        # start_button.setDisabled(True)
        remove_button.clicked.connect(self.pr)

        form_layout.setVerticalSpacing(25)
        form_layout.setHorizontalSpacing(50)
        form_layout.setContentsMargins(50, 50, 50, 0)

    def startSimulation(self, name):
        self.simulation = Simulator(name)
        self.simulation.simulationFinished.connect(self.terminateView)
        self.simulation.show()

    def terminateView(self):
        self.simulation = None

    def pr(self):
        print(self.parent().indexOf(self))
