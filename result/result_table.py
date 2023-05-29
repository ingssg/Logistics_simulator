import csv
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QFileDialog

from simulation.simulation_observer import SimulationReport

projectinfo = {}
runinfo = {}


def registerProjectInfo(info):
    global projectinfo
    projectinfo = info


def registerRunInfo(info):
    global runinfo
    runinfo = info


class ResultTable(QTableWidget):
    def __init__(self, report: SimulationReport, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["type", "value"])
        self.setRowCount(4)
        self.setItem(0, 0, QTableWidgetItem("Simul ID"))
        self.setItem(0, 1, QTableWidgetItem(report.name))
        self.setItem(1, 0, QTableWidgetItem("throughput"))
        self.setItem(1, 1, QTableWidgetItem(str(sum(r[1] for r in report.robots))))
        self.setItem(2, 0, QTableWidgetItem("elapsed"))
        self.setItem(2, 1, QTableWidgetItem(str(report.elapsed)))
        self.setItem(3, 0, QTableWidgetItem("errors"))
        self.setItem(3, 1, QTableWidgetItem(str(report.errors)))
        self.save_button = QPushButton("저장", self)
        self.save_button.move(205, 200)
        self.save_button.clicked.connect(lambda: self.save_data(report))
        self.save_button.setStyleSheet(
            "color: rgb(82, 242, 226); background-color: rgb(86, 140, 140);border: 2px solid rgb(82, 242, 226); border-radius: 20px;"
        )
        self.setStyleSheet("background-color: rgb(255,255,255);")
        self.save_button.setFixedSize(120, 40)

    def save_data(self, report: SimulationReport):
        pinfo = projectinfo
        rinfo = runinfo
        table1_header = ["ProjectID", "Distributor", "Customer", "CenterName"]
        table2_header = ["GridID", "SimulID", "Dump", "Belt", "Logistics"]
        table3_header = ["Throughput", "Time", "Errors"]

        table1_data = [
            pinfo["PID"],
            pinfo["Distributor"],
            pinfo["Customer"],
            pinfo["CenterName"],
        ]
        table2_data = [
            pinfo["gridID"],
            str(report.name),
            rinfo["dump"],
            rinfo["belt"],
            rinfo["logis"],
        ]
        table3_data = [
            str(sum(r[1] for r in report.robots)),
            str(round(report.elapsed, 2)),
            str(report.errors),
        ]

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv)"
        )
        if filename:
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["PROJECT INFO"])
                writer.writerow(table1_header)
                writer.writerow(table1_data)
                writer.writerow([])
                writer.writerow(["SETTING"])
                writer.writerow(table2_header)
                writer.writerow(table2_data)
                writer.writerow([])
                writer.writerow(["RESULT"])
                writer.writerow(table3_header)
                writer.writerow(table3_data)
