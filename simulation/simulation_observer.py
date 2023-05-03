from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal, Slot


@dataclass
class SimulationReport:
    name: str
    elapsed: float
    robots: list[int]
    timeSeries: list[tuple[float, int]]


class SimulationObserver(QObject):
    _instance = None
    simulationReported = Signal(SimulationReport)
    simulationRemoved = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(SimulationReport)
    def forwardReport(self, report: SimulationReport):
        self.simulationReported.emit(report)

    @Slot(int)
    def forwardRemoved(self, index: int):
        self.simulationRemoved.emit(index)

    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance
