from PySide6.QtCore import Qt
from PySide6 import QtCharts
from PySide6.QtCharts import QBarSeries, QBarSet, QChart, QChartView
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from simulation.simulation_observer import SimulationReport


class ThroughputRobot(QChartView):
    def __init__(self, report: SimulationReport, parent=None):
        super().__init__(parent)
        self.series = QBarSeries()
        set1 = QBarSet("Throughput")
        set1.append([r[1] for r in report.robots])

        self.series.append(set1)

        self.dataChart = QChart()
        self.dataChart.setTitle("Simulation Result - Throughput")
        self.dataChart.addSeries(self.series)
        self.dataChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        self.axisX = QtCharts.QBarCategoryAxis()
        self.axisX.append(
            [
                f"{'dump' if report.robots[i][0]==1 else 'belt'} {i}"
                for i in range(len(report.robots))
            ]
        )
        self.dataChart.addAxis(self.axisX, Qt.AlignBottom)
        self.series.attachAxis(self.axisX)

        self.axisY = QtCharts.QValueAxis()
        self.dataChart.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.dataChart.legend().setVisible(True)
        self.dataChart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.dataChart)
        self.setRenderHint(QPainter.Antialiasing)
