# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homePage.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_homepage(object):
    def setupUi(self, homepage):
        if not homepage.objectName():
            homepage.setObjectName(u"homepage")
        homepage.resize(1000, 550)
        homepage.setStyleSheet(u"background-color: rgb(1,35,38);")
        self.centralwidget = QWidget(homepage)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(200, 310, 151, 61))
        font = QFont()
        font.setFamilies([u"\ud734\uba3c\ubaa8\uc74cT"])
        font.setPointSize(25)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(82,242,226);")
        self.logolabel = QLabel(self.centralwidget)
        self.logolabel.setObjectName(u"logolabel")
        self.logolabel.setGeometry(QRect(220, 200, 121, 111))
        self.loadMap = QPushButton(self.centralwidget)
        self.loadMap.setObjectName(u"loadMap")
        self.loadMap.setGeometry(QRect(520, 250, 300, 75))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadMap.sizePolicy().hasHeightForWidth())
        self.loadMap.setSizePolicy(sizePolicy)
        self.loadMap.setMinimumSize(QSize(300, 75))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uace0\ub515 ExtraBold"])
        font1.setPointSize(15)
        self.loadMap.setFont(font1)
        self.loadMap.setStyleSheet(u"color: rgb(0,0,0);\n"
"background-color: rgb(86,140,140);\n"
"border-radius: 35px;\n"
"border: 9px double rgb(82,242,226);")
        homepage.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(homepage)
        self.statusbar.setObjectName(u"statusbar")
        homepage.setStatusBar(self.statusbar)

        self.retranslateUi(homepage)

        QMetaObject.connectSlotsByName(homepage)
    # setupUi

    def retranslateUi(self, homepage):
        homepage.setWindowTitle(QCoreApplication.translate("homepage", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("homepage", u"Simulator", None))
        self.logolabel.setText(QCoreApplication.translate("homepage", u"<html><head/><body><p><br/></p></body></html>", None))
        self.loadMap.setText(QCoreApplication.translate("homepage", u"\ub9f5 \ud30c\uc77c \ubd88\ub7ec\uc624\uae30", None))
    # retranslateUi

