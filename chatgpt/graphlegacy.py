from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from simulation.simulation_observer import SimulationReport


class ThroughputBarChart(QChartView):
    def __init__(self, report: SimulationReport, parent=None):
        super().__init__(parent)
        self.simulations_names = []
        self.set1 = QtCharts.QBarSet('Belt')
        self.set2 = QtCharts.QBarSet('Dump')
        self.set3 = QtCharts.QBarSet('Total')

        self.series = QtCharts.QBarSeries()
        self.series.append(self.set1)
        self.series.append(self.set2)
        self.series.append(self.set3)

        self.dataChart = QChart()
        self.dataChart.setTitle('Simulation Result - Throughput')
        self.dataChart.addSeries(self.series)
        self.dataChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        self.axisX = QtCharts.QBarCategoryAxis()
        self.axisX.append(self.simulations_names)
        self.dataChart.addAxis(self.axisX, Qt.AlignBottom)
        self.series.attachAxis(self.axisX)

        self.axisY = QtCharts.QValueAxis()
        self.dataChart.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.dataChart.legend().setVisible(True)
        self.dataChart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.dataChart)

        self.maxRange = 0

    @Slot(str, float, int, int)
    def addDataSlot(self, name: str, elapsed, r1: int, r2: int):
        self.simulations_names.append(name)
        self.set1.append(r1)
        self.set2.append(r2)
        self.set3.append(r1+r2)
        self.axisX.append(self.simulations_names)

        self.maxRange = r1+r2 if r1+r2 > self.maxRange else self.maxRange
        self.axisY.setRange(0, self.maxRange*1.1)
        self.axisY.setLabelFormat("%d")


class ThroughputTime(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.simulations_names = []

        self.series1 = QLineSeries()
        self.series1.setName('Throughput')

        self.lineChart = QChart()
        self.lineChart.addSeries(self.series1)
        self.lineChart.addSeries(self.series2)
        self.lineChart.setTitle('robot type')
        self.lineChart.setAnimationOptions(QChart.SeriesAnimations)

        self.axisX = QValueAxis()
        self.axisX.setRange(0, 4)
        self.axisX.setTickCount(5)
        self.axisX.setLabelFormat("%d")
        self.lineChart.addAxis(self.axisX, Qt.AlignBottom)
        self.series1.attachAxis(self.axisX)
        self.series2.attachAxis(self.axisX)

        self.axisY = QValueAxis()
        self.axisY.setRange(0, 6)
        self.axisY.setTickCount(7)
        self.axisY.setLabelFormat("%.1f")
        self.lineChart.addAxis(self.axisY, Qt.AlignLeft)
        self.series1.attachAxis(self.axisY)
        self.series2.attachAxis(self.axisY)

        self.lineChart.legend().setVisible(True)
        self.lineChart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.lineChart)
        self.setRenderHint(QPainter.Antialiasing)

    @Slot(str, float, int, int)
    def addDataSlot(self, name: str, elapsed: float, r1: int, r2: int):
        self.series1.append(r1/elapsed)
        self.series2.append(r2/elapsed)
        self.series1.attachAxis(self.axisX)
        self.series2.attachAxis(self.axisX)
        self.series1.attachAxis(self.axisY)
        self.series2.attachAxis(self.axisY)
