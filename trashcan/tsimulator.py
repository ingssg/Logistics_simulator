# @Slot()
# def doNextOperation(self):
#     if self.sequence + 1 == len(self.route):
#         self.finishMission()
#         return

#     if self.deadlockedCounter >= DEAD_THRESHOLD:
#         # this idea is not testable
#         # find all robots
#         bots: list[Robot] = []
#         selfPos = self.route[self.sequence].point().toTuple()
#         for r in self._registry:
#             neighborPos = r.route[r.sequence].point().toTuple()
#             if r.stopped:
#                 if (
#                     neighborPos == (selfPos[0], selfPos[1] - 1)
#                     or neighborPos == (selfPos[0], selfPos[1] + 1)
#                     or neighborPos == (selfPos[0] - 1, selfPos[1])
#                     or neighborPos == (selfPos[0] + 1, selfPos[1])
#                 ):
#                     bots.append(r)

#         for r in bots:
#             # i think tempblocked should be nodepos
#             # each cell can assign "align" mission to robot
#             # to dump or get box
#             route = evaluateRoute(
#                 r.route[r.sequence],
#                 r.route[len(r.route) - 1],
#                 tempBlocked=[r.route[r.sequence + 1].point().toTuple()],
#             )
#             r.assignMission()

#     # robot is reached this cell just right now!
#     degreeDiff = (
#         self.route[self.sequence + 1].degree() - self.route[self.sequence].degree()
#     )

#     if degreeDiff != 0:
#         self.stopped = False
#         self.sequence += 1
#         self.rotateOperation(degreeDiff, self.speed)
#     else:
#         self.evadeCollision()

# def evadeCollision(self):
#     self_op_dest = self.route[self.sequence + 1]

#     for r in self._registry:
#         if r.robotNum == self.robotNum:
#             continue

#         opCurrPos = r.currRobotPosWait()
#         opOperPos = r.getOperatingPos()

#         # maybe do not use of these...

#         """
#         1 0 2
#         1 wait
#         2 proceed

#         / 0 1
#         0
#         2
#         """
#         # self is finished operation just right now!
#         # self.seq is not accumulated!

#         if not r.stopped and self_op_dest.point() == opOperPos.point():
#             print("op")
#             self.waitOperation(self.speed + 30)
#             return

#         elif self_op_dest.point() == opCurrPos.point():
#             if facingEach(self_op_dest, opCurrPos):
#                 print("facing")

#                 # if tempblocked is one of deadlocked robots destination??
#                 if self.route[len(self.route) - 1].point() == opCurrPos.point():
#                     self.priority += 1

#                 if self.priority < r.priority:
#                     # call maybe..upper conflict resolver?
#                     print("evaluate")
#                     # if tempblocked is one of deadlocked robots destination??
#                     # tempblocked should be nodepos?
#                     route = evaluateRoute(
#                         self.route[self.sequence],
#                         self.route[len(self.route) - 1],
#                         tempBlocked=[opCurrPos.point().toTuple()],
#                     )
#                     self.assignMission(route, self.box)
#                     return
#                 else:
#                     print(self.robotNum, "evaluate else", self.priority, r.priority)
#                     self.waitOperation(self.speed + 30)
#                     return

#             else:
#                 print("not facing")
#                 self.waitOperation(self.speed + 30)
#                 return

#     self.stopped = False
#     self.sequence += 1
#     self.moveOperation(self.route[self.sequence].toViewPos().point(), self.speed)
#     return

# def chargeOperation(self, cell: Cell):
#     # cell.occupy()
#     self.setRoute(self.route[-1:])
#     self.stopped = True

#     while self.power < 20:
#         self.debug(f"power {self.power} route {self.route}")
#         sleep(1)
#         self.power += 1
#     cell.deOccupy()
#     self.finishMission()
