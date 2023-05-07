from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from simulation.simulation_observer import SimulationReport


class ResultTable(QTableWidget):
    def __init__(self, report: SimulationReport, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["type", "value"])
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem("name"))
        self.setItem(0, 1, QTableWidgetItem(report.name))
        self.setItem(1, 0, QTableWidgetItem("throughput"))
        self.setItem(1, 1, QTableWidgetItem(str(sum(r[1] for r in report.robots))))
        self.setItem(2, 0, QTableWidgetItem("elapsed"))
        self.setItem(2, 1, QTableWidgetItem(str(report.elapsed)))
