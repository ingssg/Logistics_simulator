from dataclasses import dataclass
import pymysql
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    password="root",
    db="lghpdb",
    charset="utf8",
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


def colorText(color):
    if warehouse_name == "":
        print("map not opened")
        return

    with conn.cursor() as cur:
        cur.execute("select * from grid where grid_id = %s", [warehouse_name])
        cellColor = cur.fetchone()
        for i in range(12, 17):
            if cellColor[i] == color:
                break
        if i - 12 == 0:
            return "충전"
        elif i - 12 == 1:
            return "슈트"
        elif i - 12 == 2:
            return "워크스테이션"
        elif i - 12 == 3:
            return "버퍼"
        elif i - 12 == 4:
            return "블락"


def cellColor(cellnum):
    if warehouse_name == "":
        print("map not opened!!!!!!!!!!")
        return

    with conn.cursor() as cur:
        cur.execute("select * from grid where grid_id = %s", [warehouse_name])
        cell_Color = cur.fetchone()
        Cell_num = cellnum + 11
        if cell_Color[Cell_num] == 1:
            return "yellow"
        elif cell_Color[Cell_num] == 2:
            return "red"
        elif cell_Color[Cell_num] == 3:
            return "green"
        elif cell_Color[Cell_num] == 4:
            return "blue"
        elif cell_Color[Cell_num] == 5:
            return "lightgrey"


def colorDict():
    cell_colors = {
        "cell": QColor(0, 0, 0, 0),
        "chute": QColor(cellColor(2)),
        "buffer": QColor(cellColor(4)),
        "workstation": QColor(cellColor(3)),
        "block": QColor(cellColor(5)),
        "chargingstation": QColor(cellColor(1)),
    }
    return cell_colors
