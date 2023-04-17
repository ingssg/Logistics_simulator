# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')*/

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os
import sys
import random

import pyqtgraph
from PySide6 import *
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import Qt
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QMainWindow, QDialog, QWidget, QFileDialog, QTableWidget, QVBoxLayout, QGridLayout, \
    QPushButton, QTableWidgetItem, QApplication, QLabel, QLineEdit, QTabWidget
import random
import openpyxl
import pymysql
from pymysql.constants import CLIENT

conn = None
cur = None

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1290', db='lghpdb', charset='utf8',
                       client_flag=CLIENT.MULTI_STATEMENTS, autocommit=True)
cur = conn.cursor()

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 1.homePage.ui
form = resource_path('homePage.ui')  # 여기에 ui파일명 입력
form_class = loadUiType(form)[0]
# 2.simul.ui
form_second = resource_path('simul.ui')
form_secondwindow = loadUiType(form_second)[0]
'''
# 3.view.ui
#form_third = resource_path('view.ui')
#form_thirdwindow = uic.loadUiType(form_third)[0]
'''

# 1.homePage.ui
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        global projectid
        projectid='tmp'
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("시뮬레이터")
        self.setFixedSize(1000, 550)
        self.loadMap.clicked.connect(self.btn_loadMap)  # loadMap button 클릭

    # -loadMap button 함수: simul.ui로 창전환
    def btn_loadMap(self):
        global projectid
        cur.execute("CALL deleteProject(%s)",[projectid])
        self.hide()
        self.second = secondwindow()
        self.second.exec()
        self.show()


# 2.simul.ui
class secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self):
        super(secondwindow, self).__init__()
        # self.initUi()
        self.setupUi(self)
        self.setWindowTitle("시뮬레이터")
        self.setFixedSize(1000, 550)
        self.show()
        # 탭활용해 화면전환 없음

        ###   overview  tab ###
        # overview-1.map 파일 미리보기
        file = QFileDialog.getOpenFileName(self, '', '', 'xlsx파일 (*.xlsx);; All File(*)')  # !!저장파일 타입 정해지면, 확장자에 추가
        global filename  # 선언, 할당 분리
        filename = file[0]
        load_xlsx = openpyxl.load_workbook(file[0], data_only=True)
        load_sheet = load_xlsx['NewSheet1']

        # 파일 이름으로 db에서 해당 정보 연결
        global file_name, simul_name, s_count
        file_name = QFileInfo(file[0]).baseName()
        # 우선 프로젝트명 : p1, 시뮬명 : s1으로 생성, 이후에 값들 입력받으면 변경
        s_count = int(1)
        simul_name = str(file_name) + '_s' + str(s_count)
        s_count = s_count + 1
        sql = "CALL deleteProject('p1'); CALL createProject('p1', NULL, NULL, NULL); CALL createSimul('p1', %s); CALL updateGridtoSimul(%s, %s); CALL updateProjectRunning(1, 'p1');"
        cur.execute(sql, [simul_name, simul_name, str(file_name)])
        # db에서 가져온 GridSize로 row, col 변경
        sql = "SELECT GridSizeX FROM grid " + "WHERE Grid_ID = %s;"
        cur.execute(sql, [str(file_name)])
        file_col = cur.fetchone()
        sql = "SELECT GridSizeY FROM grid " + "WHERE Grid_ID = %s;"
        cur.execute(sql, [str(file_name)])
        file_row = cur.fetchone()
        row = int(file_row[0])
        col = int(file_col[0])

        self.map.setColumnCount(col)
        self.map.setRowCount(row)
        for i in range(row):
            for j in range(col):
                self.map.setItem(i, j, QTableWidgetItem())
        self.map.resizeColumnsToContents()
        self.map.resizeRowsToContents()
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                if load_sheet.cell(i, j).value == "y":
                    self.map.item(i - 1, j - 1).setBackground(Qt.yellow)
                    self.map.item(i - 1, j - 1).setText("y")
                    self.map.item(i - 1, j - 1).setForeground(Qt.yellow)
                if load_sheet.cell(i, j).value == "b":
                    self.map.item(i - 1, j - 1).setBackground(Qt.darkBlue)
                    self.map.item(i - 1, j - 1).setText("b")
                    self.map.item(i - 1, j - 1).setForeground(Qt.darkBlue)
                if load_sheet.cell(i, j).value == "g":
                    self.map.item(i - 1, j - 1).setBackground(Qt.darkGreen)
                    self.map.item(i - 1, j - 1).setText("g")
                    self.map.item(i - 1, j - 1).setForeground(Qt.darkGreen)
                if load_sheet.cell(i, j).value == "r":
                    self.map.item(i - 1, j - 1).setBackground(Qt.red)
                    self.map.item(i - 1, j - 1).setText("r")
                    self.map.item(i - 1, j - 1).setForeground(Qt.red)
                if load_sheet.cell(i, j).value == "d":
                    self.map.item(i - 1, j - 1).setBackground(Qt.darkGray)
                    self.map.item(i - 1, j - 1).setText("d")
                    self.map.item(i - 1, j - 1).setForeground(Qt.darkGray)

        self.ok.clicked.connect(self.btn_ok_overview)  # overview-3.확인 버튼 클릭시, 프로젝트 정보 db저장
        self.ok_run.clicked.connect(self.btn_ok_run)  # run. 확인 버튼클릭시, result탭 이동

        # overview-2.속성별 색상 정보 보여주기
        sql = "SELECT * FROM grid " + "WHERE Grid_ID = %s;"
        cur.execute(sql, [str(file_name)])
        file_grid = cur.fetchone()
        print(file_grid[13])
        print(file_grid[14])
        print(file_grid[15])
        print(file_grid[16])
        print(file_grid[17])

        # 충전셀 색상
        if file_grid[13] == 1:
            self.color_charge.setText("Yellow")
            self.c_charge.setStyleSheet('background:yellow')
        elif file_grid[13] == 2:
            self.color_charge.setText("Red")
            self.c_charge.setStyleSheet('background:red')
        elif file_grid[13] == 3:
            self.color_charge.setText("Green")
            self.c_charge.setStyleSheet('background:green')
        elif file_grid[13] == 4:
            self.color_charge.setText("Blue")
            self.c_charge.setStyleSheet('background:blue')
        elif file_grid[13] == 5:
            self.color_charge.setText("Grey")
            self.c_charge.setStyleSheet('background:darkgrey')

        # 슈트셀 색상
        if file_grid[14] == 1:
            self.color_chute.setText("Yellow")
            self.c_chute.setStyleSheet('background:yellow')
        elif file_grid[14] == 2:
            self.color_chute.setText("Red")
            self.c_chute.setStyleSheet('background:red')
        elif file_grid[14] == 3:
            self.color_chute.setText("Green")
            self.c_chute.setStyleSheet('background:green')
        elif file_grid[14] == 4:
            self.color_chute.setText("Blue")
            self.c_chute.setStyleSheet('background:blue')
        elif file_grid[14] == 5:
            self.color_chute.setText("Grey")
            self.c_chute.setStyleSheet('background:darkgrey')

        # 워크스테이션셀 색상
        if file_grid[15] == 1:
            self.color_ws.setText("Yellow")
            self.c_ws.setStyleSheet('background:yellow')
        elif file_grid[15] == 2:
            self.color_ws.setText("Red")
            self.c_ws.setStyleSheet('background:red')
        elif file_grid[15] == 3:
            self.color_ws.setText("Green")
            self.c_ws.setStyleSheet('background:green')
        elif file_grid[15] == 4:
            self.color_ws.setText("Blue")
            self.c_ws.setStyleSheet('background:blue')
        elif file_grid[15] == 5:
            self.color_ws.setText("Grey")
            self.c_ws.setStyleSheet('background:darkgrey')

        # 버퍼셀 색상
        if file_grid[16] == 1:
            self.color_buffer.setText("Yellow")
            self.c_buffer.setStyleSheet('background:yellow')
        elif file_grid[16] == 2:
            self.color_buffer.setText("Red")
            self.c_buffer.setStyleSheet('background:red')
        elif file_grid[16] == 3:
            self.color_buffer.setText("Green")
            self.c_buffer.setStyleSheet('background:green')
        elif file_grid[16] == 4:
            self.color_buffer.setText("Blue")
            self.c_buffer.setStyleSheet('background:blue')
        elif file_grid[16] == 5:
            self.color_buffer.setText("Grey")
            self.c_buffer.setStyleSheet('background:darkgrey')

        # 블락셀 색상
        if file_grid[17] == 1:
            self.color_block.setText("Yellow")
            self.c_block.setStyleSheet('background:yellow')
        elif file_grid[17] == 2:
            self.color_block.setText("Red")
            self.c_block.setStyleSheet('background:red')
        elif file_grid[17] == 3:
            self.color_block.setText("Green")
            self.c_block.setStyleSheet('background:green')
        elif file_grid[17] == 4:
            self.color_block.setText("Blue")
            self.c_block.setStyleSheet('background:blue')
        elif file_grid[17] == 5:
            self.color_block.setText("Grey")
            self.c_block.setStyleSheet('background:darkgrey')

            ### overview tab end ###

        ### run tab ###
        global count  # 총 시뮬레이션 개수
        count = 1
        self.addsimul.clicked.connect(self.btn_addsimul)  # 시뮬레이션 탭 추가
        self.simultab.tabCloseRequested.connect(self.delete)  # 시뮬레이션 탭 삭제

        # simul1 (시뮬레이션1)탭 기본
        grid = QGridLayout()
        belt = QLabel('벨트 로봇 개수 ')
        self.belt1 = QLineEdit()
        dump = QLabel('덤프 로봇 개수 ')
        self.dump1 = QLineEdit()
        work = QLabel('총 작업량 ')
        self.work1 = QLineEdit()
        speed = QLabel('시뮬레이션 스피드 ')
        self.speed1 = QLineEdit()
        self.view1 = QPushButton('시뮬레이션 보기', self)
        # 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
        # self.btn.move(20, 20)
        grid.addWidget(belt, 0, 0)
        grid.addWidget(self.belt1, 0, 1)
        grid.addWidget(dump, 1, 0)
        grid.addWidget(self.dump1, 1, 1)
        grid.addWidget(work, 2, 0)
        grid.addWidget(self.work1, 2, 1)
        grid.addWidget(speed, 3, 0)
        grid.addWidget(self.speed1, 3, 1)
        grid.addWidget(self.view1, 4, 1)
        self.simul1.setLayout(grid)
        # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
        self.view1.clicked.connect(self.btn_view1)
        ### run end ###

        ### result ###
        # 기능-3) 마침 버튼 추가
        #결과-1) 결과표(tab_4), 시간당 작업량 그래프(tab_5), 로봇타입당 작업량 그래프(tab_6): btn_ok_run 함수
        ### result end ###

    # overview-3.확인 버튼 클릭시, 프로젝트정보 db입력 & run탭으로 이동
    def btn_ok_overview(self):
        global projectid
        projectid = str(self.projectid.text())
        distributor = str(self.distributor.text())
        customer = str(self.customer.text())
        centername = str(self.centername.text())
        cur.execute("SELECT Project_ID FROM project WHERE project.running = 1")
        pid = cur.fetchone()
        sql = "CALL updateProject(%s, %s, %s, %s, %s);"
        cur.execute(sql, [pid[0], projectid, distributor, customer, centername])

        # 탭 이동
        cur_index = self.tabWidget.currentIndex()
        self.tabWidget.setCurrentIndex(cur_index + 1)
        #if cur_index < len(self.tabWidget) - 1:
        #    self.tabWidget.setCurrentIndex(cur_index + 1)

    # run-1.시뮬레이션 추가 버튼 클릭시, 시뮬레이션 탭 추가
    def btn_addsimul(self):
        global count, projectid, simul_name, s_count
        count = count + 1

        # 시뮬레이션 탭 추가 시 DB에도 추가
        simul_name = str(file_name) + '_s' + str(s_count)
        s_count = s_count + 1
        sql = 'CALL createSimul(%s, %s); CALL updateGridtoSimul(%s, %s);'
        cur.execute(sql, [projectid, simul_name, simul_name, file_name])

        # cur_index = self.tabWidget.currentIndex()
        # tabname="simul"+str(count)
        self.tabname = QTabWidget()
        self.simultab.addTab(self.tabname, "시뮬레이션 " + str(count))
        # 기능-1)시뮬레이션 탭(우선 5번 추가 단순 반복으로 구현, 문자열+숫자를 객체 이름으로 사용하는 법 다시 시도)
        if count == 1:  # 시뮬탭1
            grid = QGridLayout()
            belt = QLabel('벨트 로봇 개수 ')
            self.belt1 = QLineEdit()
            dump = QLabel('덤프 로봇 개수 ')
            self.dump1 = QLineEdit()
            work = QLabel('총 작업량 ')
            self.work1 = QLineEdit()
            speed = QLabel('시뮬레이션 스피드 ')
            self.speed1 = QLineEdit()
            self.view1 = QPushButton('시뮬레이션 보기', self)
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지 >> 확인버튼 없애고 무조건 시뮬레이션 보기로 넘어가게 하는 것도 하나의 방법일듯 싶음
            # self.btn.move(20, 20)
            grid.addWidget(belt, 0, 0)
            grid.addWidget(self.belt1, 0, 1)
            grid.addWidget(dump, 1, 0)
            grid.addWidget(self.dump1, 1, 1)
            grid.addWidget(work, 2, 0)
            grid.addWidget(self.work1, 2, 1)
            grid.addWidget(speed, 3, 0)
            grid.addWidget(self.speed1, 3, 1)
            grid.addWidget(self.view1, 4, 1)
            self.tabname.setLayout(grid)
            # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
            self.view1.clicked.connect(self.btn_view1)
        if count == 2:  # 시뮬탭1
            grid = QGridLayout()
            belt = QLabel('벨트 로봇 개수 ')
            self.belt2 = QLineEdit()
            dump = QLabel('덤프 로봇 개수 ')
            self.dump2 = QLineEdit()
            work = QLabel('총 작업량 ')
            self.work2 = QLineEdit()
            speed = QLabel('시뮬레이션 스피드 ')
            self.speed2 = QLineEdit()
            self.view2 = QPushButton('시뮬레이션 보기', self)
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
            # self.btn.move(20, 20)
            grid.addWidget(belt, 0, 0)
            grid.addWidget(self.belt2, 0, 1)
            grid.addWidget(dump, 1, 0)
            grid.addWidget(self.dump2, 1, 1)
            grid.addWidget(work, 2, 0)
            grid.addWidget(self.work2, 2, 1)
            grid.addWidget(speed, 3, 0)
            grid.addWidget(self.speed2, 3, 1)
            grid.addWidget(self.view2, 4, 1)
            self.tabname.setLayout(grid)
            # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
            self.view2.clicked.connect(self.btn_view2)
        if count == 3:
            grid = QGridLayout()
            belt = QLabel('벨트 로봇 개수 ')
            self.belt3 = QLineEdit()
            dump = QLabel('덤프 로봇 개수 ')
            self.dump3 = QLineEdit()
            work = QLabel('총 작업량 ')
            self.work3 = QLineEdit()
            speed = QLabel('시뮬레이션 스피드 ')
            self.speed3 = QLineEdit()
            self.view3 = QPushButton('시뮬레이션 보기', self)
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
            # self.btn.move(20, 20)
            grid.addWidget(belt, 0, 0)
            grid.addWidget(self.belt3, 0, 1)
            grid.addWidget(dump, 1, 0)
            grid.addWidget(self.dump3, 1, 1)
            grid.addWidget(work, 2, 0)
            grid.addWidget(self.work3, 2, 1)
            grid.addWidget(speed, 3, 0)
            grid.addWidget(self.speed3, 3, 1)
            grid.addWidget(self.view3, 4, 1)
            self.tabname.setLayout(grid)
            # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
            self.view3.clicked.connect(self.btn_view3)
        if count == 4:
            grid = QGridLayout()
            belt = QLabel('벨트 로봇 개수 ')
            self.belt4 = QLineEdit()
            dump = QLabel('덤프 로봇 개수 ')
            self.dump4 = QLineEdit()
            work = QLabel('총 작업량 ')
            self.work4 = QLineEdit()
            speed = QLabel('시뮬레이션 스피드 ')
            self.speed4 = QLineEdit()
            self.view4 = QPushButton('시뮬레이션 보기', self)
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
            # self.btn.move(20, 20)
            grid.addWidget(belt, 0, 0)
            grid.addWidget(self.belt4, 0, 1)
            grid.addWidget(dump, 1, 0)
            grid.addWidget(self.dump4, 1, 1)
            grid.addWidget(work, 2, 0)
            grid.addWidget(self.work4, 2, 1)
            grid.addWidget(speed, 3, 0)
            grid.addWidget(self.speed4, 3, 1)
            grid.addWidget(self.view4, 4, 1)
            self.tabname.setLayout(grid)
            # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
            self.view4.clicked.connect(self.btn_view4)
        if count == 5:
            grid = QGridLayout()
            belt = QLabel('벨트 로봇 개수 ')
            self.belt5 = QLineEdit()
            dump = QLabel('덤프 로봇 개수 ')
            self.dump5 = QLineEdit()
            work = QLabel('총 작업량 ')
            self.work5 = QLineEdit()
            speed = QLabel('시뮬레이션 스피드 ')
            self.speed5 = QLineEdit()
            self.view5 = QPushButton('시뮬레이션 보기', self)
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
            # self.btn.move(20, 20)
            grid.addWidget(belt, 0, 0)
            grid.addWidget(self.belt5, 0, 1)
            grid.addWidget(dump, 1, 0)
            grid.addWidget(self.dump5, 1, 1)
            grid.addWidget(work, 2, 0)
            grid.addWidget(self.work5, 2, 1)
            grid.addWidget(speed, 3, 0)
            grid.addWidget(self.speed5, 3, 1)
            grid.addWidget(self.view5, 4, 1)
            self.tabname.setLayout(grid)
            # view="btn_view"+str(1)->객체 만들어지지X view함수 여러개..(다시해보기)
            self.view5.clicked.connect(self.btn_view5)

    # run-2.시뮬레이션 탭 삭제버튼 클릭시, 탭 클로즈 & 시뮬레이션 DB 삭제
    def delete(self, index):
        global count, projectid, simul_name, s_count, file_name
        count = count - 1
        s_count = s_count - 1
        # DB에서 해당 simulname(simul3같은)테이터 삭제
        cur_index = self.simultab.currentIndex()
        simulname = "simul" + str(cur_index + 1)
        simul_name = file_name + '_s' + str(cur_index + 1)
        print(simulname)
        # 시뮬레이션 3을 삭제할 때 시뮬레이션 3을 클릭하고 있어야만 simulname 값이 3이 나옴.
        sql = "CALL deleteSimulation(%s);"
        cur.execute(sql, [simul_name])

        # 삭제 시뮬레이션 뒷쪽 시뮬레이션의 simulid 하나씩 당기기 ->중간 시뮬레이션 삭제하는 경우와 delete를 위해서
        d = count - cur_index
        k = d
        move = count + 1
        while d > 0:
            simulid = "simul" + str(move)
            # print(simulid)
            # DB-5) simul id가 'simulid'["simul"+str(move)]인 데이터의 simul id를 simulid-1["simul"+str(move-1)]로 변경
            # (예:simul2 데이터의 simul id를 simul1로 변경) 반복
            d = d - 1
            move = move - 1
            self.simultab.setTabText(move, "시뮬레이션 " + str(move))
        move = move + 1
        while k > 0:
            simulid = file_name + '_s' + str(move)
            move = move - 1
            newsimulid = file_name + '_s' + str(move)
            move = move + 2
            sql = "CALL updateSimulName(%s, %s);"
            cur.execute(sql, [simulid, newsimulid])
            k = k - 1

        # 탭 없애기
        self.simultab.removeTab(index)

    # run-3.확인 버튼 클릭시, result 탭이동
    def btn_ok_run(self):
        print(count)
        ##결과표 만들기
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(count)
        headers = []
        for i in range(count):
            headers.append("시뮬레이션 " + str(i + 1))
        print(headers)
        self.table.setHorizontalHeaderLabels(headers)
        # table.setHorizontalHeaderLabels(["simulation"])
        self.table.setVerticalHeaderLabels(
            ["총 소요시간(s)", "시간당 작업량", "벨트로봇당 평균 작업량", "덤프로봇당 평균 작업량", "벨트로봇 개수", "덤프로봇 개수", "물류량"])
        self.table.setItem(0, 0, QTableWidgetItem(str(int(int(self.work1.text()) / 60))))
        """for i in range(count):
            w="work"+str(i+1)
            b="belt"+str(i+1)
            d="dump"+str(i+1)
            table.setItem(0,i,QTableWidgetItem(60))#총소요시간:임의로 60초, 나중에 가져오기
            table.setItem(1, i, QTableWidgetItem((self.w)/60))  # 시간당 작업량=물류량/작업시간
            table.setItem(2, i, QTableWidgetItem((self.w)*(self.b)/(self.d)))  # 벨트로봇 당 작업량=총작업량*로봇타입비율 ?
            table.setItem(3, i, QTableWidgetItem(60))  # 덤프로봇 당 작업량
            table.setItem(4, i, QTableWidgetItem(self.b))  # 벨트로봇 개수
            table.setItem(5, i, QTableWidgetItem(self.d))  # 덤프로봇 개수
            table.setItem(6, i, QTableWidgetItem(self.w))  # 물류량"""
        #위 객체 이름 해결시, 밑 코드 위 코드로 바꾸기
        for i in range(count):
            if i==0:
                self.table.setItem(0, i, QTableWidgetItem('60'))  # 총소요시간:임의로 60초, 나중에 값받기*
                self.table.setItem(1, i, QTableWidgetItem(str((int(int(self.work1.text()) / 60)))))  # 시간당 작업량=물류량/작업시간, 시간 값받기*
                self.table.setItem(2, i, QTableWidgetItem('10'))  # 벨트로봇 당 작업량 값받기*[=총작업량*로봇타입비율 ?int((self.work1) * (self.belt1) / (self.dump1))]
                self.table.setItem(3, i, QTableWidgetItem('10'))  # 덤프로봇 당 작업량 값받기*
                self.table.setItem(4, i, QTableWidgetItem(self.belt1.text()))  # 벨트로봇 개수
                self.table.setItem(5, i, QTableWidgetItem(self.dump1.text()))  # 덤프로봇 개수
                self.table.setItem(6, i, QTableWidgetItem(self.work1.text()))  # 물류량
            elif i==1:
                self.table.setItem(0, i, QTableWidgetItem('60'))  # 총소요시간:임의로 60초, 나중에 값받기*
                self.table.setItem(1, i, QTableWidgetItem(
                    str((int(int(self.work2.text()) / 60)))))  # 시간당 작업량=물류량/작업시간, 시간 값받기*
                self.table.setItem(2, i, QTableWidgetItem(
                    '10'))  # 벨트로봇 당 작업량 값받기*[=총작업량*로봇타입비율 ?int((self.work1) * (self.belt1) / (self.dump1))]
                self.table.setItem(3, i, QTableWidgetItem('10'))  # 덤프로봇 당 작업량 값받기*
                self.table.setItem(4, i, QTableWidgetItem(self.belt2.text()))  # 벨트로봇 개수
                self.table.setItem(5, i, QTableWidgetItem(self.dump2.text()))  # 덤프로봇 개수
                self.table.setItem(6, i, QTableWidgetItem(self.work2.text()))  # 물류량
            elif i==2:
                self.table.setItem(0, i, QTableWidgetItem('60'))  # 총소요시간:임의로 60초, 나중에 값받기*
                self.table.setItem(1, i, QTableWidgetItem(
                    str((int(int(self.work3.text()) / 60)))))  # 시간당 작업량=물류량/작업시간, 시간 값받기*
                self.table.setItem(2, i, QTableWidgetItem(
                    '10'))  # 벨트로봇 당 작업량 값받기*[=총작업량*로봇타입비율 ?int((self.work1) * (self.belt1) / (self.dump1))]
                self.table.setItem(3, i, QTableWidgetItem('10'))  # 덤프로봇 당 작업량 값받기*
                self.table.setItem(4, i, QTableWidgetItem(self.belt3.text()))  # 벨트로봇 개수
                self.table.setItem(5, i, QTableWidgetItem(self.dump3.text()))  # 덤프로봇 개수
                self.table.setItem(6, i, QTableWidgetItem(self.work3.text()))  # 물류량
            elif i==3:
                self.table.setItem(0, i, QTableWidgetItem('60'))  # 총소요시간:임의로 60초, 나중에 값받기*
                self.table.setItem(1, i, QTableWidgetItem(
                    str((int(int(self.work4.text()) / 60)))))  # 시간당 작업량=물류량/작업시간, 시간 값받기*
                self.table.setItem(2, i, QTableWidgetItem(
                    '10'))  # 벨트로봇 당 작업량 값받기*[=총작업량*로봇타입비율 ?int((self.work1) * (self.belt1) / (self.dump1))]
                self.table.setItem(3, i, QTableWidgetItem('10'))  # 덤프로봇 당 작업량 값받기*
                self.table.setItem(4, i, QTableWidgetItem(self.belt4.text()))  # 벨트로봇 개수
                self.table.setItem(5, i, QTableWidgetItem(self.dump4.text()))  # 덤프로봇 개수
                self.table.setItem(6, i, QTableWidgetItem(self.work4.text()))  # 물류량
            elif i==4: #현재 시뮬 5개 까지, 늘릴때 여기도 늘리기
                self.table.setItem(0, i, QTableWidgetItem('60'))  # 총소요시간:임의로 60초, 나중에 값받기*
                self.table.setItem(1, i, QTableWidgetItem(
                    str((int(int(self.work5.text()) / 60)))))  # 시간당 작업량=물류량/작업시간, 시간 값받기*
                self.table.setItem(2, i, QTableWidgetItem(
                    '10'))  # 벨트로봇 당 작업량 값받기*[=총작업량*로봇타입비율 ?int((self.work1) * (self.belt1) / (self.dump1))]
                self.table.setItem(3, i, QTableWidgetItem('10'))  # 덤프로봇 당 작업량 값받기*
                self.table.setItem(4, i, QTableWidgetItem(self.belt5.text()))  # 벨트로봇 개수
                self.table.setItem(5, i, QTableWidgetItem(self.dump5.text()))  # 덤프로봇 개수
                self.table.setItem(6, i, QTableWidgetItem(self.work5.text()))  # 물류량


        self.table.setGeometry(300, 300, 600, 600)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.tab_4.setLayout(layout)
        ##로봇타입당 작업량 그래프##
        name = []
        num=[]
        workbelt = []
        workdump = []
        for i in range(count):
            name.append("시뮬레이션 " + str(i + 1))
            num.append(i+1)
            workbelt.append(10 * (i + 1))  # 임의, 값받아오기*
            workdump.append(15 * (i + 1))  # 임의, 값받아오기*
        #x축 문자열
        x_dict=dict(enumerate(name))
        ticks=[list(zip(x_dict.keys(),x_dict.values()))]
        self.graph1.setBackground("White")
        self.graph1.setLabel("left", "로봇 타입당 작업량")
        self.graph1.addLegend()
        pen = pyqtgraph.mkPen(color="Red")
        self.graph1.plot(list(range(len(name))), workbelt, name="Belt Type", pen=pen, symbol='o', symbolSize=5, symbolBrush=("Red"))
        pen = pyqtgraph.mkPen(color="Blue")
        self.graph1.plot(list(range(len(name))), workdump, name="Dump Type", pen=pen, symbol='o', symbolSize=5, symbolBrush=("Blue"))
        xax=self.graph1.getAxis('bottom')
        xax.setTicks(ticks)
        self.graph1.showGrid(x=True,y=True)
        ##로봇타입당 작업량 그래프 end##
        ##시간당 작업량 그래프##
        self.bargraph.setBackground("White")
        self.bargraph.setLabel("left", "시간당 작업량")
        y=[]
        for i in range(count):
            y.append((int(int(self.work1.text()) / 1))) #임의의 값 1, 소요시간 받아오기* (모든 시뮬 작업량이 같은 경우)
        bar=pyqtgraph.BarGraphItem(x=list(range(len(name))),height=y,width=0.3,brush='dark blue')
        self.bargraph.addItem(bar)
        xax = self.bargraph.getAxis('bottom')
        xax.setTicks(ticks)
        ##시간당 작업량 그래프 end##
        # 탭 이동
        cur_index = self.tabWidget.currentIndex()
        self.tabWidget.setCurrentIndex(cur_index + 1)

    # run-4. 시뮬레이션 보기 클릭시, 입력 정보 DB에 저장 & 시뮬레이션 화면 띄우기
    def btn_view1(self):
        global file_name
        '''다시시도
        # cur_index = self.simultab.currentIndex()
        # print(cur_index+1)
        # beltname="belt"+str(cur_index+1)
        # print(self.beltname.text())
        '''
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        belt1 = self.belt1.text()
        dump1 = self.dump1.text()
        work1 = self.work1.text()
        speed1 = self.speed1.text()
        # DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = file_name + "_s" + str(cur_index + 1)
        sql = "CALL createRun(%s, %s, %s, %s, %s);"
        cur.execute(sql, [simulid, belt1, dump1, work1, speed1])

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

    def btn_view2(self):
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        belt2 = self.belt2.text()
        dump2 = self.dump2.text()
        work2 = self.work2.text()
        speed2 = self.speed2.text()
        # DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = file_name + "_s" + str(cur_index + 1)
        sql = "CALL createRun(%s, %s, %s, %s, %s);"
        cur.execute(sql, [simulid, belt2, dump2, work2, speed2])

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

    def btn_view3(self):
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        belt3 = self.belt3.text()
        dump3 = self.dump3.text()
        work3 = self.work3.text()
        speed3 = self.speed3.text()
        # DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = file_name + "_s" + str(cur_index + 1)
        sql = "CALL createRun(%s, %s, %s, %s, %s);"
        cur.execute(sql, [simulid, belt3, dump3, work3, speed3])

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

    def btn_view4(self):
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        belt4 = self.belt4.text()
        dump4 = self.dump4.text()
        work4 = self.work4.text()
        speed4 = self.speed4.text()
        # DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = file_name + "_s" + str(cur_index + 1)
        sql = "CALL createRun(%s, %s, %s, %s, %s);"
        cur.execute(sql, [simulid, belt4, dump4, work4, speed4])

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

    def btn_view5(self):
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        # 시뮬레이션보기 클릭시, 정보 db에 저장
        belt5 = self.belt5.text()
        dump5 = self.dump5.text()
        work5 = self.work5.text()
        speed5 = self.speed5.text()
        # DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = file_name + "_s" + str(cur_index + 1)
        sql = "CALL createRun(%s, %s, %s, %s, %s);"
        cur.execute(sql, [simulid, belt5, dump5, work5, speed5])

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''


# 3.view.ui 시뮬레이션 보기 버튼 클릭시, 시뮬레이션 보여주는 화면
# 시뮬레이션-2) 시뮬레이션 화면 클래스 추가
'''
class thirdwindow(QDialog, QWidget, form_thirdwindow):
    def __init__(self):
        super(thirdwindow, self).__init__()
        # self.initUi()
        self.setupUi(self)
        self.setWindowTitle("시뮬레이션")
        self.setFixedSize(1600, 900)
        self.show()
        self.check.clicked.connect(self.btn_check)
    def btn_check(self):
        self.close()
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()
cur.execute("CALL deleteProject(%s)", [projectid])
conn.close()
