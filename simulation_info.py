from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation_tab import SimulationTab

from PySide6.QtWidgets import QFormLayout, QLineEdit, QPushButton, QWidget
from graph import ThroughputBarChart

from simulation_window import SimulationWindow


class SimulationInfo(QWidget):
    def __init__(self, graph: ThroughputBarChart, parent: SimulationTab = None):
        super().__init__(parent)
        self.graph = graph
        form_layout = QFormLayout(self)
        name_field = QLineEdit(self)
        belt_field = QLineEdit(self)
        dump_field = QLineEdit(self)
        logistic_field = QLineEdit(self)

        start_button = QPushButton('Start Simulation', self)
        start_button.clicked.connect(
            lambda: self.startSimulation(name_field.text()))
        # start_button.setDisabled(True)

        form_layout.addRow('Name', name_field)
        form_layout.addRow('Belt', belt_field)
        form_layout.addRow('Dump', dump_field)
        form_layout.addRow('Logistics', logistic_field)
        form_layout.addRow(start_button)

        form_layout.setVerticalSpacing(50)
        form_layout.setHorizontalSpacing(50)
        form_layout.setContentsMargins(50, 50, 50, 0)

    def startSimulation(self, name):
        self.simulation = SimulationWindow(name)
        self.simulation.simulationFinished.connect(self.graph.addDataSlot)
        self.simulation.simulationFinished.connect(self.terminateView)
        self.simulation.show()

    def terminateView(self):
        self.simulation = None
