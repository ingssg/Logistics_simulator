from dataclasses import dataclass
import pymysql
from PySide6.QtCore import Qt

conn = pymysql.connect(
    host="127.0.0.1", user="root", password="root", db="lghpdb", charset="utf8"
)

dblist = ["buffer", "chargingstation", "chute", "workstation"]
colors = [Qt.blue, Qt.yellow, Qt.red, Qt.white]

warehouse_name = ""


def registerWarehouse(name):
    global warehouse_name
    warehouse_name = name


@dataclass
class _Cell:
    cellType: str
    pos: tuple[int, int]
    outDir: tuple[int, int, int, int]


@dataclass
class Warehouse:
    grid: tuple[int, int]
    cells: list[_Cell]

    def __post_init__(self):
        self.cells = [_Cell(getCellType(c[0]), c[1], c[2]) for c in self.cells]


def getCellType(n: int) -> str:
    if n == 1:
        return "chargingstation"
    elif n == 2:
        return "chute"
    elif n == 3:
        return "workstation"
    elif n == 4:
        return "buffer"
    elif n == 5:
        return "block"
    elif n == 7:
        return "cell"
    else:
        return "cell"


def queryMap():
    if warehouse_name == "":
        print("map not opened")
        return

    with conn.cursor() as cur:
        cur.execute(
            "select gridsizex, gridsizey from grid where grid_id = %s", [warehouse_name]
        )
        grid = cur.fetchone()

        cur.execute("select * from cell where grid_id=%s", [warehouse_name])
        rawcells = cur.fetchall()
        cells = {(x[2], (x[5], x[4]), x[6:10]) for x in rawcells}

        return Warehouse(grid, cells)
