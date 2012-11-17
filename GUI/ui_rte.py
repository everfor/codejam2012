# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RTEDlg.ui'
#
# Created: Sat Nov 17 08:38:22 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RTEDlg(object):
    def setupUi(self, RTEDlg):
        RTEDlg.setObjectName(_fromUtf8("RTEDlg"))
        RTEDlg.resize(1222, 572)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RTEDlg.sizePolicy().hasHeightForWidth())
        RTEDlg.setSizePolicy(sizePolicy)
        RTEDlg.setMinimumSize(QtCore.QSize(1222, 572))
        RTEDlg.setMaximumSize(QtCore.QSize(1222, 572))
        RTEDlg.setWhatsThis(_fromUtf8(""))
        self.line = QtGui.QFrame(RTEDlg)
        self.line.setGeometry(QtCore.QRect(260, 10, 20, 551))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.smaMpl = MatplotlibWidget(RTEDlg)
        self.smaMpl.setGeometry(QtCore.QRect(280, 10, 461, 271))
        self.smaMpl.setObjectName(_fromUtf8("smaMpl"))
        self.emaMpl = MatplotlibWidget(RTEDlg)
        self.emaMpl.setGeometry(QtCore.QRect(280, 290, 461, 271))
        self.emaMpl.setObjectName(_fromUtf8("emaMpl"))
        self.lwmaMpl = MatplotlibWidget(RTEDlg)
        self.lwmaMpl.setGeometry(QtCore.QRect(750, 10, 461, 271))
        self.lwmaMpl.setObjectName(_fromUtf8("lwmaMpl"))
        self.tmaMpl = MatplotlibWidget(RTEDlg)
        self.tmaMpl.setGeometry(QtCore.QRect(750, 290, 461, 271))
        self.tmaMpl.setObjectName(_fromUtf8("tmaMpl"))
        self.groupBox = QtGui.QGroupBox(RTEDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 251, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.connectButton = QtGui.QPushButton(self.groupBox)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.gridLayout_3.addWidget(self.connectButton, 0, 0, 1, 1)
        self.disconnectButton = QtGui.QPushButton(self.groupBox)
        self.disconnectButton.setObjectName(_fromUtf8("disconnectButton"))
        self.gridLayout_3.addWidget(self.disconnectButton, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.ipEdit = QtGui.QLineEdit(self.groupBox)
        self.ipEdit.setObjectName(_fromUtf8("ipEdit"))
        self.gridLayout.addWidget(self.ipEdit, 0, 1, 1, 1)
        self.pfLabel = QtGui.QLabel(self.groupBox)
        self.pfLabel.setWordWrap(True)
        self.pfLabel.setObjectName(_fromUtf8("pfLabel"))
        self.gridLayout.addWidget(self.pfLabel, 1, 0, 1, 1)
        self.pfEdit = QtGui.QLineEdit(self.groupBox)
        self.pfEdit.setObjectName(_fromUtf8("pfEdit"))
        self.gridLayout.addWidget(self.pfEdit, 1, 1, 1, 1)
        self.tbLabel = QtGui.QLabel(self.groupBox)
        self.tbLabel.setWordWrap(True)
        self.tbLabel.setObjectName(_fromUtf8("tbLabel"))
        self.gridLayout.addWidget(self.tbLabel, 2, 0, 1, 1)
        self.tbEdit = QtGui.QLineEdit(self.groupBox)
        self.tbEdit.setObjectName(_fromUtf8("tbEdit"))
        self.gridLayout.addWidget(self.tbEdit, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(RTEDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 160, 251, 61))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.startButton = QtGui.QPushButton(self.groupBox_2)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.verticalLayout_2.addWidget(self.startButton)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(RTEDlg)
        QtCore.QMetaObject.connectSlotsByName(RTEDlg)

    def retranslateUi(self, RTEDlg):
        RTEDlg.setWindowTitle(QtGui.QApplication.translate("RTEDlg", "Algorithmic Trading Application", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("RTEDlg", "Connection Details", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("RTEDlg", "&Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectButton.setText(QtGui.QApplication.translate("RTEDlg", "&Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RTEDlg", "IP Address", None, QtGui.QApplication.UnicodeUTF8))
        self.pfLabel.setText(QtGui.QApplication.translate("RTEDlg", "Price Feed Port", None, QtGui.QApplication.UnicodeUTF8))
        self.pfEdit.setText(QtGui.QApplication.translate("RTEDlg", "8211", None, QtGui.QApplication.UnicodeUTF8))
        self.tbLabel.setText(QtGui.QApplication.translate("RTEDlg", "Trade Booking Port", None, QtGui.QApplication.UnicodeUTF8))
        self.tbEdit.setText(QtGui.QApplication.translate("RTEDlg", "8212", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("RTEDlg", "GUI Commands", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("RTEDlg", "Start", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget
