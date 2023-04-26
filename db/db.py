import pymysql
from PySide6.QtCore import Qt

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='root', db='lghpdb', charset='utf8')

dblist = ['buffer', 'chargingstation', 'chute', 'workstation']
colors = [Qt.blue, Qt.yellow, Qt.red, Qt.white]


def queryMap(mapName: str):
    with conn.cursor() as cur:
        cur.execute(
            'select gridsizex, gridsizey from grid where grid_id = %s', [mapName])
        grid = cur.fetchone()

        # X and Y converted!!
        cells: dict[str, tuple] = {}
        for l in dblist:
            cur.execute(
                'select locationy, locationx from {} where grid_id=%s'.format(l), [mapName])
            cells[l] = cur.fetchall()

        return cells, grid


if __name__ == "__main__":
    print(queryMap('test1'))
