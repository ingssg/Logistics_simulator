# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simul.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1000, 550)
        Dialog.setStyleSheet(u"background-color: rgb(1,35,38);")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(5, 5, 1000, 550))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uace0\ub515 ExtraBold"])
        self.tabWidget.setFont(font)
        self.tabWidget.setToolTipDuration(-3)
        self.tabWidget.setStyleSheet(u"background-color: rgb(1,35,38);\n"
"gridline-color: rgb(1,35,38);\n"
"color: rgb(1,35,38);\n"
"border-color: rgb(25, 25, 25);\n"
"gridline-color: rgb(30, 30, 30);")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(200, 17))
        self.tabWidget.setElideMode(Qt.ElideMiddle)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.map = QTableWidget(self.tab)
        self.map.setObjectName(u"map")
        self.map.setGeometry(QRect(280, 70, 431, 381))
        self.map.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 110, 121, 21))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uace0\ub515 ExtraBold"])
        font1.setPointSize(15)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(82,242,226);")
        self.listView = QListView(self.tab)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(30, 70, 221, 311))
        self.listView.setStyleSheet(u"color: rgb(255,255,255);\n"
"background-color: rgb(1,35,40);\n"
"border: 7px double rgb(82,242,226);\n"
"border-radius: 10px;")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(800, 110, 101, 21))
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(82,242,226);")
        self.listView_2 = QListView(self.tab)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setGeometry(QRect(740, 70, 221, 311))
        self.listView_2.setStyleSheet(u"color: rgb(255,255,255);\n"
"background-color: rgb(1,35,40);\n"
"border: 7px double rgb(82,242,226);\n"
"border-radius: 10px;")
        self.color_charge = QLabel(self.tab)
        self.color_charge.setObjectName(u"color_charge")
        self.color_charge.setGeometry(QRect(1400, 90, 54, 12))
        self.color_ws = QLabel(self.tab)
        self.color_ws.setObjectName(u"color_ws")
        self.color_ws.setGeometry(QRect(1400, 150, 61, 16))
        self.color_chute = QLabel(self.tab)
        self.color_chute.setObjectName(u"color_chute")
        self.color_chute.setGeometry(QRect(1400, 120, 51, 20))
        self.color_buffer = QLabel(self.tab)
        self.color_buffer.setObjectName(u"color_buffer")
        self.color_buffer.setGeometry(QRect(1400, 180, 61, 16))
        self.color_block = QLabel(self.tab)
        self.color_block.setObjectName(u"color_block")
        self.color_block.setGeometry(QRect(1400, 210, 61, 16))
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(50, 150, 180, 161))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.distributor = QLineEdit(self.gridLayoutWidget)
        self.distributor.setObjectName(u"distributor")
        self.distributor.setMinimumSize(QSize(0, 25))
        font2 = QFont()
        font2.setPointSize(12)
        self.distributor.setFont(font2)
        self.distributor.setStyleSheet(u"background-color: rgb(1,35,40);\n"
"color: rgb(107,242,242);\n"
"border: 1px solid rgb(107,242,242);")

        self.gridLayout.addWidget(self.distributor, 1, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uace0\ub515 ExtraBold"])
        font3.setPointSize(11)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"color: rgb(82,242,226);")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"color: rgb(82,242,226);")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.customer = QLineEdit(self.gridLayoutWidget)
        self.customer.setObjectName(u"customer")
        self.customer.setMinimumSize(QSize(0, 25))
        self.customer.setFont(font2)
        self.customer.setStyleSheet(u"background-color: rgb(1,35,40);\n"
"color: rgb(107,242,242);\n"
"border: 1px solid rgb(107,242,242);")

        self.gridLayout.addWidget(self.customer, 2, 1, 1, 1)

        self.projectid = QLineEdit(self.gridLayoutWidget)
        self.projectid.setObjectName(u"projectid")
        self.projectid.setMinimumSize(QSize(0, 25))
        self.projectid.setFont(font2)
        self.projectid.setStyleSheet(u"background-color: rgb(1,35,40);\n"
"color: rgb(107,242,242);\n"
"border: 1px solid rgb(107,242,242);\n"
"")

        self.gridLayout.addWidget(self.projectid, 0, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color: rgb(82,242,226);")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)
        self.label_6.setStyleSheet(u"color: rgb(82,242,226);")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.centername = QLineEdit(self.gridLayoutWidget)
        self.centername.setObjectName(u"centername")
        self.centername.setMinimumSize(QSize(80, 25))
        self.centername.setFont(font2)
        self.centername.setStyleSheet(u"background-color: rgb(1,35,40);\n"
"color: rgb(107,242,242);\n"
"border: 1px solid rgb(107,242,242);")

        self.gridLayout.addWidget(self.centername, 3, 1, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.tab)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(780, 140, 160, 176))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.c_charge = QPushButton(self.tab)
        self.c_charge.setObjectName(u"c_charge")
        self.c_charge.setGeometry(QRect(892, 141, 37, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_charge.sizePolicy().hasHeightForWidth())
        self.c_charge.setSizePolicy(sizePolicy)
        self.c_charge.setMinimumSize(QSize(30, 30))
        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(771, 285, 115, 30))
        font4 = QFont()
        font4.setFamilies([u"\ub098\ub214\uace0\ub515 ExtraBold"])
        font4.setPointSize(13)
        self.label_11.setFont(font4)
        self.label_11.setStyleSheet(u"color: rgb(82,242,226);")
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(771, 213, 115, 30))
        self.label_9.setFont(font4)
        self.label_9.setStyleSheet(u"color: rgb(82,242,226);")
        self.c_ws = QPushButton(self.tab)
        self.c_ws.setObjectName(u"c_ws")
        self.c_ws.setGeometry(QRect(892, 213, 37, 30))
        sizePolicy.setHeightForWidth(self.c_ws.sizePolicy().hasHeightForWidth())
        self.c_ws.setSizePolicy(sizePolicy)
        self.c_ws.setMinimumSize(QSize(30, 30))
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(771, 249, 115, 30))
        self.label_10.setFont(font4)
        self.label_10.setStyleSheet(u"color: rgb(82,242,226);")
        self.c_block = QPushButton(self.tab)
        self.c_block.setObjectName(u"c_block")
        self.c_block.setGeometry(QRect(892, 285, 37, 30))
        sizePolicy.setHeightForWidth(self.c_block.sizePolicy().hasHeightForWidth())
        self.c_block.setSizePolicy(sizePolicy)
        self.c_block.setMinimumSize(QSize(30, 30))
        self.c_chute = QPushButton(self.tab)
        self.c_chute.setObjectName(u"c_chute")
        self.c_chute.setGeometry(QRect(892, 177, 37, 30))
        sizePolicy.setHeightForWidth(self.c_chute.sizePolicy().hasHeightForWidth())
        self.c_chute.setSizePolicy(sizePolicy)
        self.c_chute.setMinimumSize(QSize(30, 30))
        self.c_buffer = QPushButton(self.tab)
        self.c_buffer.setObjectName(u"c_buffer")
        self.c_buffer.setGeometry(QRect(892, 249, 37, 30))
        sizePolicy.setHeightForWidth(self.c_buffer.sizePolicy().hasHeightForWidth())
        self.c_buffer.setSizePolicy(sizePolicy)
        self.c_buffer.setMinimumSize(QSize(30, 30))
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(771, 141, 115, 30))
        self.label_7.setFont(font4)
        self.label_7.setStyleSheet(u"color: rgb(82,242,226);")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(771, 177, 115, 30))
        self.label_8.setFont(font4)
        self.label_8.setStyleSheet(u"color: rgb(82,242,226);")
        self.save = QPushButton(self.tab)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(100, 330, 75, 24))
        self.save.setFont(font3)
        self.save.setStyleSheet(u"QPushButton {\n"
"            color: rgb(82,242,226);\n"
"            background-color: rgb(86,140,140);\n"
"            border: 2px solid rgb(82,242,226);\n"
"            border-radius: 10px;\n"
"        }\n"
"        QPushButton:hover {\n"
"            color: rgb(255,255,255);\n"
"            background-color: rgb(100,149,237);\n"
"            border-color: rgb(100,149,237);\n"
"        }")
        self.tabWidget.addTab(self.tab, "")
        self.listView_2.raise_()
        self.listView.raise_()
        self.map.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.color_charge.raise_()
        self.color_ws.raise_()
        self.color_chute.raise_()
        self.color_buffer.raise_()
        self.color_block.raise_()
        self.gridLayoutWidget.raise_()
        self.gridLayoutWidget_2.raise_()
        self.c_charge.raise_()
        self.label_11.raise_()
        self.label_9.raise_()
        self.c_ws.raise_()
        self.label_10.raise_()
        self.c_block.raise_()
        self.c_chute.raise_()
        self.c_buffer.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.save.raise_()

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\ud504\ub85c\uc81d\ud2b8 \uc815\ubcf4", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\uc18d\uc131\ubcc4 \uc0c9\uc0c1", None))
        self.color_charge.setText("")
        self.color_ws.setText("")
        self.color_chute.setText("")
        self.color_buffer.setText("")
        self.color_block.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Distributor", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Project ID", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Customer", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Center Name", None))
        self.c_charge.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\ube14\ub77d", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\uc6cc\ud06c \uc2a4\ud14c\uc774\uc158", None))
        self.c_ws.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\ubc84\ud37c", None))
        self.c_block.setText("")
        self.c_chute.setText("")
        self.c_buffer.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\ucda9\uc804", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\uc288\ud2b8", None))
        self.save.setText(QCoreApplication.translate("Dialog", u"save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Overview", None))
    # retranslateUi

