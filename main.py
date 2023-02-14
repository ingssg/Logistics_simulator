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

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QFileInfo
import random

# import xlsxwriter

import openpyxl
from PyQt5.uic.properties import QtGui


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 1.homePage.ui
form = resource_path('homePage.ui')  # 여기에 ui파일명 입력
form_class = uic.loadUiType(form)[0]
# 2.simul.ui
form_second = resource_path('simul.ui')
form_secondwindow = uic.loadUiType(form_second)[0]
'''
# 3.view.ui
#form_third = resource_path('view.ui')
#form_thirdwindow = uic.loadUiType(form_third)[0]
'''

# 1.homePage.ui
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("시뮬레이터")
        self.setFixedSize(1500, 900)
        self.loadMap.clicked.connect(self.btn_loadMap)  # loadMap button 클릭

    # -loadMap button 함수: simul.ui로 창전환
    def btn_loadMap(self):
        self.hide()
        self.second = secondwindow()
        self.second.exec_()
        self.show()

# 2.simul.ui
class secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self):
        super(secondwindow, self).__init__()
        # self.initUi()
        self.setupUi(self)
        self.setWindowTitle("시뮬레이터")
        self.setFixedSize(1600, 900)
        self.show()
        # 탭활용해 화면전환 없음

        ###   overview  tab ###
        # overview-1.map 파일 미리보기
        file = QFileDialog.getOpenFileName(self, '', '', 'xlsx파일 (*.xlsx);; All File(*)')  # !!저장파일 타입 정해지면, 확장자에 추가
        global filename  # 선언, 할당 분리
        filename = file[0]
        load_xlsx = openpyxl.load_workbook(file[0], data_only=True)
        load_sheet = load_xlsx['NewSheet1']
        # DB-1) self.map에 db에서 맵파일 불러오기 (지금은 엑셀로 가져옴. db에서 가져오는 걸로 변경하기)
        row = load_sheet.max_row
        col = load_sheet.max_column
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

        self.ok.clicked.connect(self.btn_ok_overview) # overview-3.확인 버튼 클릭시, 프로젝트 정보 db저장
        self.ok_run.clicked.connect(self.btn_ok_run)#run. 확인 버튼클릭시, result탭 이동

        # overview-2.속성별 색상 정보 보여주기
        # DB-2)속성별 색상 정보 db에서 가져와서 보여주기 (현재 임의로 지정)
        self.color_charge.setText("Yellow")
        self.color_chute.setText("Red")
        self.color_ws.setText("Green")
        self.color_buffer.setText("Blue")
        self.color_block.setText("Grey")

        self.c_charge.setStyleSheet('background:yellow')
        self.c_chute.setStyleSheet('background:red')
        self.c_ws.setStyleSheet('background:green')
        self.c_buffer.setStyleSheet('background:blue')
        self.c_block.setStyleSheet('background:darkgrey')
        ### overview tab end ###

        ### run tab ###
        global count #총 시뮬레이션 개수
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
        #시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
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
        #기능-3) 마침 버튼 추가
        ### result end ###

    # overview-3.확인 버튼 클릭시, 프로젝트정보 db입력 & run탭으로 이동
    def btn_ok_overview(self):
        # DB-3) 입력된 프로젝트정보 db에 저장
        print(self.projectid.text())
        print(self.distributor.text())
        print(self.customer.text())
        print(self.centername.text())

        # 탭 이동
        cur_index = self.tabWidget.currentIndex()
        if cur_index < len(self.tabWidget) - 1:
            self.tabWidget.setCurrentIndex(cur_index + 1)

    # run-1.시뮬레이션 추가 버튼 클릭시, 시뮬레이션 탭 추가
    def btn_addsimul(self):
        global count
        count = count + 1
        print(count)
        # cur_index = self.tabWidget.currentIndex()
        # tabname="simul"+str(count)
        self.tabname = QTabWidget()
        self.simultab.addTab(self.tabname, "시뮬레이션 " + str(count))
        # 기능-1)시뮬레이션 탭(우선 5번 추가 단순 반복으로 구현, 문자열+숫자를 객체이름으로 사용하는 법 다시 시도)
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
            # 지금은 시뮬레이션보기 버튼 클릭시 입력정보 저장, 따로 저장 버튼 추가할지 말지
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
        global count
        count = count - 1
        #기능-2) (시뮬레이션보기 버튼 클릭 없이 삭제하기 위해->시뮬레이션 만들때 임의값 넣어줘야하?나중에)
        # DB에서 해당 simulname(simul3같은)테이터 삭제
        cur_index = self.simultab.currentIndex()
        simulname = "simul" + str(cur_index + 1)
        print(simulname)
        #DB-4) simul id가 simulname인 데이터 DB에서 삭제

        #삭제 시뮬레이션 뒷쪽 시뮬레이션의 simulid 하나씩 당기기 ->중간 시뮬레이션 삭제하는 경우와 delete를 위해서
        d = count - cur_index
        move = count + 1
        while d > 0:
            simulid = "simul" + str(move)
            print(simulid)
            # DB-5) simul id가 'simulid'["simul"+str(move)]인 데이터의 simul id를 simulid-1["simul"+str(move-1)]로 변경
            # (예:simul2 데이터의 simul id를 simul1로 변경) 반복
            d = d - 1
            move = move - 1
            self.simultab.setTabText(move, "시뮬레이션 " + str(move))
            
        # 탭 없애기
        self.simultab.removeTab(index)

    # run-3.확인 버튼 클릭시, result 탭이동
    def btn_ok_run(self):
        # 탭 이동
        cur_index = self.tabWidget.currentIndex()
        if cur_index < len(self.tabWidget) - 1:
            self.tabWidget.setCurrentIndex(cur_index + 1)

    #run-4. 시뮬레이션 보기 클릭시, 입력 정보 DB에 저장 & 시뮬레이션 화면 띄우기
    def btn_view1(self):
        '''다시시도
        # cur_index = self.simultab.currentIndex()
        # print(cur_index+1)
        # beltname="belt"+str(cur_index+1)
        # print(self.beltname.text())
        '''
        #시뮬레이션보기 클릭시, 정보 db에 저장
        print(self.belt1.text())
        print(self.dump1.text())
        print(self.work1.text())
        print(self.speed1.text())
        #DB-6)위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = "simul" + str(cur_index + 1)
        print(simulid)
        
        #시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

    def btn_view2(self):
        #시뮬레이션보기 클릭시, 정보 db에 저장
        print(self.belt2.text())
        print(self.dump2.text())
        print(self.work2.text())
        print(self.speed2.text())
        # DB-6) 위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = "simul" + str(cur_index + 1)
        print(simulid)

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''
    def btn_view3(self):
        #시뮬레이션보기 클릭시, 정보 db에 저장
        print(self.belt3.text())
        print(self.dump3.text())
        print(self.work3.text())
        print(self.speed3.text())
        #DB-6) 위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = "simul" + str(cur_index + 1)
        print(simulid)

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''
    def btn_view4(self):
        #시뮬레이션보기 클릭시, 정보 db에 저장
        print(self.belt4.text())
        print(self.dump4.text())
        print(self.work4.text())
        print(self.speed4.text())
        #DB-6) 위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = "simul" + str(cur_index + 1)
        print(simulid)

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''
    def btn_view5(self):
        #시뮬레이션보기 클릭시, 정보 db에 저장
        print(self.belt5.text())
        print(self.dump5.text())
        print(self.work5.text())
        print(self.speed5.text())
        #DB-6) 위정보를 다음 simulid인 db에 저장하기
        cur_index = self.simultab.currentIndex()
        simulid = "simul" + str(cur_index + 1)
        print(simulid)

        # 시뮬레이션-1) 시뮬레이션 화면 띄우기
        '''
        # 시뮬레이션 화면이동 코드
        #self.hide()
        #self.third = thirdwindow()
        #self.third.exec_()
        #self.show()
        '''

# 3.view.ui 시뮬레이션 보기 버튼 클릭시, 시뮬레이션 보여주는 화면
#시뮬레이션-2) 시뮬레이션 화면 클래스 추가
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
    app.exec_()