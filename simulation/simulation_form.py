from __future__ import annotations
from dataclasses import dataclass
import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QFont
from db.db import queryMap
from result.result_table import registerRunInfo
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
    QLabel,
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
        form_layout = QFormLayout(self)

        self.name_label = QLabel(self)
        self.name_label.setText("Name")
        self.belt_label = QLabel(self)
        self.belt_label.setText("Belt Type")
        self.dump_label = QLabel(self)
        self.dump_label.setText("Dump Type")
        self.logistic_label = QLabel(self)
        self.logistic_label.setText("Logistics")
        self.speed_label = QLabel(self)
        self.speed_label.setText("Speed")

        self.name_field = QLineEdit(self)
        form_layout.addRow(self.name_label, self.name_field)
        self.belt_field = QLineEdit(self)
        form_layout.addRow(self.belt_label, self.belt_field)
        self.dump_field = QLineEdit(self)
        form_layout.addRow(self.dump_label, self.dump_field)
        self.logistic_field = QLineEdit(self)
        form_layout.addRow(self.logistic_label, self.logistic_field)
        # self.interval_field = QLineEdit(self)
        # form_layout.addRow('Record Interval', self.interval_field)
        self.speed = QComboBox()
        self.speed.addItems(["0.5", "1", "2"])
        self.speed.setCurrentIndex(1)
        form_layout.addRow(self.speed_label, self.speed)
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

        start_button.setStyleSheet(
            "color: rgb(82,242,226);border: 7px double rgb(82,242,226);border-radius: 25px;"
        )
        start_button.setFont(QFont("나눔고딕 ExtraBold", 12))
        start_button.setFixedSize(210, 50)
        remove_button.setStyleSheet(
            "color: rgb(82,242,226);border: 7px double rgb(82,242,226);border-radius: 25px;"
        )
        remove_button.setFont(QFont("나눔고딕 ExtraBold", 12))
        remove_button.setFixedSize(210, 50)
        self.name_label.setFont(QFont("나눔고딕 ExtraBold", 14))
        self.name_label.setStyleSheet("color: rgb(82,242,226)")
        self.belt_label.setFont(QFont("나눔고딕 ExtraBold", 14))
        self.belt_label.setStyleSheet("color: rgb(82,242,226)")
        self.dump_label.setFont(QFont("나눔고딕 ExtraBold", 14))
        self.dump_label.setStyleSheet("color: rgb(82,242,226)")
        self.logistic_label.setFont(QFont("나눔고딕 ExtraBold", 14))
        self.logistic_label.setStyleSheet("color: rgb(82,242,226)")
        self.speed_label.setFont(QFont("나눔고딕 ExtraBold", 14))
        self.speed_label.setStyleSheet("color: rgb(82,242,226)")
        self.name_field.setStyleSheet(
            "color: rgb(82,242,226);border: 2px solid rgb(82,242,226);"
        )
        self.name_field.setFixedSize(120, 35)
        self.belt_field.setStyleSheet(
            "color: rgb(82,242,226);border: 2px solid rgb(82,242,226);"
        )
        self.belt_field.setFixedSize(120, 35)
        self.dump_field.setStyleSheet(
            "color: rgb(82,242,226);border: 2px solid rgb(82,242,226);"
        )
        self.dump_field.setFixedSize(120, 35)
        self.logistic_field.setStyleSheet(
            "color: rgb(82,242,226);border: 2px solid rgb(82,242,226);"
        )
        self.logistic_field.setFixedSize(120, 35)
        self.speed.setStyleSheet(
            "color: rgb(82,242,226);border: 2px solid rgb(82,242,226);"
        )
        self.speed.setFixedSize(120, 35)
        self.speed.setFont(QFont("나눔고딕 ExtraBold", 13))

        self.bufferCount = len(
            list(filter(lambda x: x.cellType == "buffer", queryMap().cells))
        )

    def startSimulation(self):
        runinfo = {
            "belt": self.belt_field.text(),
            "dump": self.dump_field.text(),
            "logis": self.logistic_field.text()
        }
        registerRunInfo(runinfo)
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

        if int(self.belt_field.text()) + int(self.dump_field.text()) > self.bufferCount:
            alert.setText("Robots exceeded")
            alert.exec()
            return False
        else:
            return True

    def terminate(self, r):
        self.simulator.deleteLater()

    def removeTabHandler(self):
        index = self.parent().indexOf(self)
        self.parent().parent().tabCloseRequested.emit(index)
