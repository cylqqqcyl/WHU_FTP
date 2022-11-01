# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(800, 604)
        self.centralwidget = QtWidgets.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.infoTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.infoTab.setFont(font)
        self.infoTab.setStyleSheet("")
        self.infoTab.setObjectName("infoTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.infoTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stateLbl = QtWidgets.QLabel(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.stateLbl.setFont(font)
        self.stateLbl.setStyleSheet("background-color: rgba(128, 128, 128, 200);\n"
"color: rgb(255, 255, 255);")
        self.stateLbl.setObjectName("stateLbl")
        self.verticalLayout.addWidget(self.stateLbl)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_6.setSpacing(20)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.nameLbl = QtWidgets.QLabel(self.infoTab)
        self.nameLbl.setMinimumSize(QtCore.QSize(100, 0))
        self.nameLbl.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
        self.gridLayout_6.addWidget(self.nameLbl, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout_6.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.addressLbl = QtWidgets.QLabel(self.infoTab)
        self.addressLbl.setMinimumSize(QtCore.QSize(100, 0))
        self.addressLbl.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.addressLbl.setFont(font)
        self.addressLbl.setObjectName("addressLbl")
        self.gridLayout_6.addWidget(self.addressLbl, 1, 0, 1, 1)
        self.addressEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.addressEdit.setFont(font)
        self.addressEdit.setObjectName("addressEdit")
        self.gridLayout_6.addWidget(self.addressEdit, 1, 1, 1, 1)
        self.portLbl = QtWidgets.QLabel(self.infoTab)
        self.portLbl.setMinimumSize(QtCore.QSize(100, 0))
        self.portLbl.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.portLbl.setFont(font)
        self.portLbl.setObjectName("portLbl")
        self.gridLayout_6.addWidget(self.portLbl, 2, 0, 1, 1)
        self.portEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.portEdit.setFont(font)
        self.portEdit.setObjectName("portEdit")
        self.gridLayout_6.addWidget(self.portEdit, 2, 1, 1, 1)
        self.rootBtn = QtWidgets.QPushButton(self.infoTab)
        self.rootBtn.setMinimumSize(QtCore.QSize(100, 0))
        self.rootBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.rootBtn.setObjectName("rootBtn")
        self.gridLayout_6.addWidget(self.rootBtn, 3, 0, 1, 1)
        self.rootEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.rootEdit.setFont(font)
        self.rootEdit.setObjectName("rootEdit")
        self.gridLayout_6.addWidget(self.rootEdit, 3, 1, 1, 1)
        self.dbBtn = QtWidgets.QPushButton(self.infoTab)
        self.dbBtn.setMinimumSize(QtCore.QSize(100, 0))
        self.dbBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dbBtn.setObjectName("dbBtn")
        self.gridLayout_6.addWidget(self.dbBtn, 4, 0, 1, 1)
        self.dbEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.dbEdit.setFont(font)
        self.dbEdit.setObjectName("dbEdit")
        self.gridLayout_6.addWidget(self.dbEdit, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.maxconLbl = QtWidgets.QLabel(self.infoTab)
        self.maxconLbl.setMinimumSize(QtCore.QSize(200, 0))
        self.maxconLbl.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.maxconLbl.setFont(font)
        self.maxconLbl.setObjectName("maxconLbl")
        self.gridLayout_2.addWidget(self.maxconLbl, 0, 0, 1, 1)
        self.maxconEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.maxconEdit.setFont(font)
        self.maxconEdit.setObjectName("maxconEdit")
        self.gridLayout_2.addWidget(self.maxconEdit, 0, 1, 1, 1)
        self.readlimLbl = QtWidgets.QLabel(self.infoTab)
        self.readlimLbl.setMinimumSize(QtCore.QSize(200, 0))
        self.readlimLbl.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.readlimLbl.setFont(font)
        self.readlimLbl.setObjectName("readlimLbl")
        self.gridLayout_2.addWidget(self.readlimLbl, 0, 2, 1, 1)
        self.readlimEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.readlimEdit.setFont(font)
        self.readlimEdit.setObjectName("readlimEdit")
        self.gridLayout_2.addWidget(self.readlimEdit, 0, 3, 1, 1)
        self.maxconipLbl = QtWidgets.QLabel(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.maxconipLbl.setFont(font)
        self.maxconipLbl.setObjectName("maxconipLbl")
        self.gridLayout_2.addWidget(self.maxconipLbl, 1, 0, 1, 1)
        self.maxconipEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.maxconipEdit.setFont(font)
        self.maxconipEdit.setObjectName("maxconipEdit")
        self.gridLayout_2.addWidget(self.maxconipEdit, 1, 1, 1, 1)
        self.writelimLbl = QtWidgets.QLabel(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.writelimLbl.setFont(font)
        self.writelimLbl.setObjectName("writelimLbl")
        self.gridLayout_2.addWidget(self.writelimLbl, 1, 2, 1, 1)
        self.writelimEdit = QtWidgets.QLineEdit(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.writelimEdit.setFont(font)
        self.writelimEdit.setObjectName("writelimEdit")
        self.gridLayout_2.addWidget(self.writelimEdit, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.applyBtn = QtWidgets.QPushButton(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.applyBtn.setFont(font)
        self.applyBtn.setObjectName("applyBtn")
        self.horizontalLayout.addWidget(self.applyBtn)
        self.startBtn = QtWidgets.QPushButton(self.infoTab)
        self.startBtn.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.startBtn.setFont(font)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout.addWidget(self.startBtn)
        self.closeBtn = QtWidgets.QPushButton(self.infoTab)
        self.closeBtn.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.closeBtn.setFont(font)
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout.addWidget(self.closeBtn)
        self.resetBtn = QtWidgets.QPushButton(self.infoTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.resetBtn.setFont(font)
        self.resetBtn.setObjectName("resetBtn")
        self.horizontalLayout.addWidget(self.resetBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget.addTab(self.infoTab, "")
        self.logTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.logTab.setFont(font)
        self.logTab.setObjectName("logTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.logTab)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.logBrowser = QtWidgets.QTextBrowser(self.logTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.logBrowser.setFont(font)
        self.logBrowser.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.logBrowser.setObjectName("logBrowser")
        self.gridLayout_3.addWidget(self.logBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.logTab, "")
        self.userTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.userTab.setFont(font)
        self.userTab.setObjectName("userTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.userTab)
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.addUserBtn = QtWidgets.QPushButton(self.userTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.addUserBtn.setFont(font)
        self.addUserBtn.setObjectName("addUserBtn")
        self.gridLayout_4.addWidget(self.addUserBtn, 1, 0, 1, 1)
        self.userTbl = QtWidgets.QTableWidget(self.userTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.userTbl.setFont(font)
        self.userTbl.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.userTbl.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.userTbl.setColumnCount(4)
        self.userTbl.setObjectName("userTbl")
        self.userTbl.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.userTbl.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTbl.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTbl.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTbl.setHorizontalHeaderItem(3, item)
        self.userTbl.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_4.addWidget(self.userTbl, 0, 0, 1, 3)
        self.delUserBtn = QtWidgets.QPushButton(self.userTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.delUserBtn.setFont(font)
        self.delUserBtn.setObjectName("delUserBtn")
        self.gridLayout_4.addWidget(self.delUserBtn, 1, 2, 1, 1)
        self.updateBtn = QtWidgets.QPushButton(self.userTab)
        self.updateBtn.setObjectName("updateBtn")
        self.gridLayout_4.addWidget(self.updateBtn, 1, 1, 1, 1)
        self.tabWidget.addTab(self.userTab, "")
        self.fileTab = QtWidgets.QWidget()
        self.fileTab.setObjectName("fileTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.fileTab)
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.treeView = QtWidgets.QTreeView(self.fileTab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.treeView.setFont(font)
        self.treeView.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.treeView.setObjectName("treeView")
        self.gridLayout_5.addWidget(self.treeView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.fileTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        ServerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ServerWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "FTP Server"))
        self.stateLbl.setText(_translate("ServerWindow", "状态：未创建"))
        self.nameLbl.setText(_translate("ServerWindow", "名称："))
        self.addressLbl.setText(_translate("ServerWindow", "地址："))
        self.portLbl.setText(_translate("ServerWindow", "端口："))
        self.rootBtn.setText(_translate("ServerWindow", "根目录"))
        self.dbBtn.setText(_translate("ServerWindow", "数据库"))
        self.maxconLbl.setText(_translate("ServerWindow", "服务器最大连接数："))
        self.readlimLbl.setText(_translate("ServerWindow", "读文件限速（KB/s）："))
        self.maxconipLbl.setText(_translate("ServerWindow", "IP最大连接数："))
        self.writelimLbl.setText(_translate("ServerWindow", "写文件限速（KB/s）："))
        self.applyBtn.setText(_translate("ServerWindow", "应用"))
        self.startBtn.setText(_translate("ServerWindow", "开启"))
        self.closeBtn.setText(_translate("ServerWindow", "关闭"))
        self.resetBtn.setText(_translate("ServerWindow", "重置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.infoTab), _translate("ServerWindow", "信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), _translate("ServerWindow", "日志"))
        self.addUserBtn.setText(_translate("ServerWindow", "添加"))
        item = self.userTbl.horizontalHeaderItem(0)
        item.setText(_translate("ServerWindow", "用户"))
        item = self.userTbl.horizontalHeaderItem(1)
        item.setText(_translate("ServerWindow", "口令"))
        item = self.userTbl.horizontalHeaderItem(2)
        item.setText(_translate("ServerWindow", "权限"))
        item = self.userTbl.horizontalHeaderItem(3)
        item.setText(_translate("ServerWindow", "信息"))
        self.delUserBtn.setText(_translate("ServerWindow", "删除"))
        self.updateBtn.setText(_translate("ServerWindow", "刷新"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.userTab), _translate("ServerWindow", "用户"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileTab), _translate("ServerWindow", "文件"))
