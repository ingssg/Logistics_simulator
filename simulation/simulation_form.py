from __future__ import annotations
from dataclasses import dataclass
import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from simulator.simulator import Simulator

if TYPE_CHECKING:
    from simulation.simulation_tab import SimulationTab

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)


@dataclass
class SimulationParameter:
    name: str
    belt: int
    dump: int
    logistics: int
    speed: str


class SimulationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maxRobot = 3
        form_layout = QFormLayout(self)

        self.name_field = QLineEdit(self)
        form_layout.addRow("Name", self.name_field)
        self.belt_field = QLineEdit(self)
        form_layout.addRow("Belt", self.belt_field)
        self.dump_field = QLineEdit(self)
        form_layout.addRow("Dump", self.dump_field)
        self.logistic_field = QLineEdit(self)
        form_layout.addRow("Logistics", self.logistic_field)
        # self.interval_field = QLineEdit(self)
        # form_layout.addRow('Record Interval', self.interval_field)
        self.speed = QComboBox()
        self.speed.addItems(["0.5", "1", "2"])
        self.speed.setCurrentIndex(1)
        form_layout.addRow("speed", self.speed)
        start_button = QPushButton("Start Simulation", self)
        form_layout.addRow(start_button)
        remove_button = QPushButton("Remove Simulation", self)
        form_layout.addRow(remove_button)

        start_button.clicked.connect(self.startSimulation)
        # start_button.setDisabled(True)
        remove_button.clicked.connect(self.removeTabHandler)

        form_layout.setVerticalSpacing(25)
        form_layout.setHorizontalSpacing(50)
        form_layout.setContentsMargins(50, 50, 50, 0)

    def startSimulation(self):
        if not self.isFormValid():
            return

        p = SimulationParameter(
            self.name_field.text(),
            int(self.belt_field.text()),
            int(self.dump_field.text()),
            int(self.logistic_field.text()),
            self.speed.currentText(),
        )
        self.simulator = Simulator(p)
        self.simulator.simulationFinished.connect(self.terminate)
        self.simulator.show()

    def isFormValid(self) -> bool:
        alert = QMessageBox()
        alert.setWindowTitle("Parameter Checker")
        if not self.name_field.text():
            alert.setText("Invalid input name")
            alert.exec()
            return False

        if (
            not self.belt_field.text().isnumeric()
            or not self.dump_field.text().isnumeric()
            or not self.logistic_field.text().isnumeric()
        ):
            alert.setText("Invalid input numeric")
            alert.exec()
            return False

        if int(self.belt_field.text()) + int(self.dump_field.text()) > self.maxRobot:
            alert.setText(f"Robots exceeded")
            alert.exec()
            return False
        else:
            return True

    def terminate(self, r):
        self.simulator.deleteLater()

    def removeTabHandler(self):
        index = self.parent().indexOf(self)
        self.parent().parent().tabCloseRequested.emit(index)
