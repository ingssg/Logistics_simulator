from __future__ import annotations

import heapq
from enum import IntEnum

from PySide6.QtCore import QPoint

from db.db import Warehouse, queryMap


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Pos:
    def __init__(self, x, y, direction) -> None:
        self.x: int = int(x)
        self.y: int = int(y)
        self.direction: int = int(direction)

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.direction == __o.direction

    def __hash__(self) -> int:
        return hash("x%dy%dd%d" % (self.x, self.y, self.direction))

    def __repr__(self) -> str:
        return "x:%d y:%d dir:%d" % (self.x, self.y, self.direction)

    def point(self):
        return QPoint(self.x, self.y)

    def degree(self):
        return self.direction * 90

    def posTuple(self):
        return (self.x, self.y)


class ViewPos(Pos):
    def __init__(self, x, y, direction) -> None:
        super().__init__(x, y, direction)

    def toNodePos(self) -> NodePos:
        return NodePos(self.x // 100, self.y // 100, self.direction)

    def __eq__(self, __o: object) -> bool:
        return type(__o) is ViewPos and super().__eq__(__o)

    def __hash__(self) -> int:
        return super().__hash__()


class NodePos(Pos):
    def __init__(self, x, y, direction) -> None:
        super().__init__(x, y, direction)

    def toViewPos(self) -> ViewPos:
        return ViewPos(self.x * 100, self.y * 100, self.direction)

    def __eq__(self, __o: object) -> bool:
        return type(__o) is NodePos and super().__eq__(__o)

    def __hash__(self) -> int:
        return super().__hash__()

    def __lt__(self, __o: object) -> bool:
        return True


def facingEach(a: NodePos, b: NodePos):
    return (a.direction != b.direction) and ((a.direction + b.direction) % 2 == 0)


warehouse: Warehouse


def registerMap():
    global warehouse
    warehouse = queryMap()


def gen(tempBlocked: list[tuple[int, int]] = []):
    raw_cells = warehouse.cells
    edges: dict[NodePos, list[tuple[NodePos, int]]] = {}

    nodes = list(
        filter(lambda x: x.pos not in tempBlocked and x.cellType != "block", raw_cells)
    )
    orientedNodes: list[NodePos] = []

    # create 4 nodes per point
    # create all rotation edge
    for n in nodes:
        for i in range(4):
            add = NodePos(*n.pos, i)
            orientedNodes.append(add)

            if add.direction == Direction.N:
                clockwise, counterwise = Direction.E, Direction.W
            elif add.direction == Direction.W:
                clockwise, counterwise = Direction.N, Direction.S
            else:
                clockwise, counterwise = add.direction + 1, add.direction - 1

            edges[add] = [
                (NodePos(add.x, add.y, clockwise), 10),
                (NodePos(add.x, add.y, counterwise), 10),
            ]

    for n in nodes:
        if n.outDir[0] == 1:
            if (dest := NodePos(n.pos[0], n.pos[1] - 1, Direction.N)) in orientedNodes:
                edges[NodePos(*n.pos, Direction.N)].append((dest, 10))
        if n.outDir[1] == 1:
            if (dest := NodePos(n.pos[0], n.pos[1] + 1, Direction.S)) in orientedNodes:
                edges[NodePos(*n.pos, Direction.S)].append((dest, 10))
        if n.outDir[2] == 1:
            if (dest := NodePos(n.pos[0] - 1, n.pos[1], Direction.W)) in orientedNodes:
                edges[NodePos(*n.pos, Direction.W)].append((dest, 10))
        if n.outDir[3] == 1:
            if (dest := NodePos(n.pos[0] + 1, n.pos[1], Direction.E)) in orientedNodes:
                edges[NodePos(*n.pos, Direction.E)].append((dest, 10))

    return orientedNodes, edges


def dijkstra(
    nodes: list[NodePos], edges: dict[NodePos, list[tuple[NodePos, int]]], src: NodePos
):
    distances = {node: float("inf") for node in nodes}
    prevs: dict[NodePos, NodePos] = {node: None for node in nodes}
    queue: list[tuple[float, NodePos]] = []

    distances[src] = 0
    heapq.heappush(queue, (distances[src], src))

    while queue:
        currDist, currNode = heapq.heappop(queue)

        if distances[currNode] < currDist:
            # dont need to visit current_distance to current route
            # cuz current route is longer
            continue

        for neighbor, weight in edges[currNode]:
            alt = currDist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                heapq.heappush(queue, (alt, neighbor))

                prevs[neighbor] = currNode

    return distances, prevs


def backTrack(prevs: dict[NodePos, NodePos], source: NodePos, destination: NodePos):
    route: list[NodePos] = [destination]

    currentTrace = destination
    while currentTrace != source:
        currentTrace = prevs[currentTrace]
        route.insert(0, currentTrace)
    return route


def evaluateRoute(src: NodePos, dest: NodePos, tempBlocked: list[tuple[int, int]] = []):
    nodes, edges = gen(tempBlocked=tempBlocked)
    _, prevs = dijkstra(nodes, edges, src)

    try:
        r = backTrack(prevs, src, dest)
        return r
    except:
        print(f"route none {src} to {dest}")


def evaluateRouteToCell(src: NodePos, dest: tuple[int, int]):
    nodes, edges = gen()
    distances, prevs = dijkstra(nodes, edges, src)
    min = (None, float("inf"))
    for i in range(4):
        temp = NodePos(dest[0], dest[1], i)

        tempdist = distances[temp]
        if tempdist < min[1]:
            min = (temp, tempdist)

    try:
        r = backTrack(prevs, src, min[0])
        return r
    except:
        print(f"route none {src} to {dest}")
