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
class Warehouse:
    grid: tuple[int, int]
    cellDirs: list[tuple]
    functionCells: dict[str, tuple]


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
        ncells = cur.fetchall()
        ncells = list(map(lambda x: x[4:10], ncells))

        # X and Y converted!!
        cells: dict[str, tuple] = {}
        for l in dblist:
            cur.execute(
                "select locationy, locationx from {} where grid_id=%s".format(l),
                [warehouse_name],
            )
            cells[l] = cur.fetchall()

        return Warehouse(grid, ncells, cells)
