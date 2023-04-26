from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Qt, Slot
from PySide6.QtGui import QPainter

from simulation.simulation_observer import SimulationReport


class ThroughputTime(QChartView):
    def __init__(self, report=SimulationReport, parent=None):
        super().__init__(parent)
        self.series1 = QLineSeries()
        self.series1.setName('Throughput')
        s = list(map(lambda x: QPointF(x[0], x[1]), report.timeSeries))
        print(s)
        self.series1.append(
            s)

        self.lineChart = QChart()
        self.lineChart.addSeries(self.series1)
        self.lineChart.setTitle('Simulation Result - Throughput')
        self.lineChart.setAnimationOptions(QChart.SeriesAnimations)

        self.axisX = QValueAxis()
        # self.axisX.setRange(0, 4)
        # self.axisX.setTickCount(5)
        # self.axisX.setLabelFormat("%d")
        self.lineChart.addAxis(self.axisX, Qt.AlignBottom)
        self.series1.attachAxis(self.axisX)

        self.axisY = QValueAxis()
        # self.axisY.setRange(0, 6)
        # self.axisY.setTickCount(7)
        # self.axisY.setLabelFormat("%.1f")
        self.lineChart.addAxis(self.axisY, Qt.AlignLeft)
        self.series1.attachAxis(self.axisY)

        self.lineChart.legend().setVisible(True)
        self.lineChart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.lineChart)
        self.setRenderHint(QPainter.Antialiasing)
        # chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @Slot(str, float, int, int)
    def addDataSlot(self, name: str, elapsed: float, r1: int, r2: int):
        self.series1.append(r1/elapsed)
        self.series2.append(r2/elapsed)
        self.series1.attachAxis(self.axisX)
        self.series2.attachAxis(self.axisX)
        self.series1.attachAxis(self.axisY)
        self.series2.attachAxis(self.axisY)
