# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitlednogNBw.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(649, 567)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 120, 101, 381))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pbGrabSingle = QPushButton(self.frame)
        self.pbGrabSingle.setObjectName(u"pbGrabSingle")
        self.pbGrabSingle.setGeometry(QRect(10, 230, 75, 24))
        self.pbCloseCam = QPushButton(self.frame)
        self.pbCloseCam.setObjectName(u"pbCloseCam")
        self.pbCloseCam.setGeometry(QRect(10, 140, 75, 24))
        self.pbStopGrab = QPushButton(self.frame)
        self.pbStopGrab.setObjectName(u"pbStopGrab")
        self.pbStopGrab.setGeometry(QRect(10, 200, 75, 24))
        self.pbStartGrab = QPushButton(self.frame)
        self.pbStartGrab.setObjectName(u"pbStartGrab")
        self.pbStartGrab.setGeometry(QRect(10, 170, 75, 24))
        self.pbConnectCam = QPushButton(self.frame)
        self.pbConnectCam.setObjectName(u"pbConnectCam")
        self.pbConnectCam.setGeometry(QRect(10, 110, 75, 24))
        self.pbOCR = QPushButton(self.frame)
        self.pbOCR.setObjectName(u"pbOCR")
        self.pbOCR.setGeometry(QRect(10, 350, 75, 24))
        self.pbTrain = QPushButton(self.frame)
        self.pbTrain.setObjectName(u"pbTrain")
        self.pbTrain.setGeometry(QRect(10, 260, 75, 24))
        self.pbMatch = QPushButton(self.frame)
        self.pbMatch.setObjectName(u"pbMatch")
        self.pbMatch.setGeometry(QRect(10, 290, 75, 24))
        self.pbSelectROI = QPushButton(self.frame)
        self.pbSelectROI.setObjectName(u"pbSelectROI")
        self.pbSelectROI.setGeometry(QRect(10, 320, 75, 24))
        self.pbEnumDev = QPushButton(self.frame)
        self.pbEnumDev.setObjectName(u"pbEnumDev")
        self.pbEnumDev.setGeometry(QRect(10, 60, 75, 24))
        self.lbResult = QLabel(Form)
        self.lbResult.setObjectName(u"lbResult")
        self.lbResult.setGeometry(QRect(450, 530, 161, 16))
        self.lbCam = QLabel(Form)
        self.lbCam.setObjectName(u"lbCam")
        self.lbCam.setGeometry(QRect(100, 540, 161, 16))
        self.lbPic = QLabel(Form)
        self.lbPic.setObjectName(u"lbPic")
        self.lbPic.setGeometry(QRect(140, 30, 450, 300))
        self.lbPic.setStyleSheet(u"\n"
"background-color: rgb(191, 191, 191);")
        self.lbTrain = QLabel(Form)
        self.lbTrain.setObjectName(u"lbTrain")
        self.lbTrain.setGeometry(QRect(140, 360, 225, 150))
        self.lbTrain.setStyleSheet(u"\n"
"background-color: rgb(191, 191, 191);")
        self.lbRes = QLabel(Form)
        self.lbRes.setObjectName(u"lbRes")
        self.lbRes.setGeometry(QRect(380, 360, 225, 150))
        self.lbRes.setStyleSheet(u"\n"
"background-color: rgb(191, 191, 191);")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pbGrabSingle.setText(QCoreApplication.translate("Form", u"\u91c7\u96c6\u5355\u5f20", None))
        self.pbCloseCam.setText(QCoreApplication.translate("Form", u"\u65ad\u5f00\u76f8\u673a", None))
        self.pbStopGrab.setText(QCoreApplication.translate("Form", u"\u505c\u6b62\u91c7\u96c6", None))
        self.pbStartGrab.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u91c7\u96c6", None))
        self.pbConnectCam.setText(QCoreApplication.translate("Form", u"\u8fde\u63a5\u76f8\u673a", None))
        self.pbOCR.setText(QCoreApplication.translate("Form", u"OCR", None))
        self.pbTrain.setText(QCoreApplication.translate("Form", u"\u8bad\u7ec3", None))
        self.pbMatch.setText(QCoreApplication.translate("Form", u"\u5339\u914d", None))
        self.pbSelectROI.setText(QCoreApplication.translate("Form", u"\u9009\u62e9ROI", None))
        self.pbEnumDev.setText(QCoreApplication.translate("Form", u"\u679a\u4e3e\u8bbe\u5907", None))
        self.lbResult.setText(QCoreApplication.translate("Form", u"Res:", None))
        self.lbCam.setText(QCoreApplication.translate("Form", u"cam:", None))
        self.lbPic.setText("")
        self.lbTrain.setText("")
        self.lbRes.setText("")
    # retranslateUi

