# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewLogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class NewLogin_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550,900)
        Form.setStyleSheet("background-color:qlineargradient(x1:0, y1:1, x0:0, y0:1,stop:0 rgb(170, 150, 50),stop:0.2 rgb(83, 50, 41) ,stop:1 rgb(94, 80, 69));\n"
"border-radius:30px;\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("background:transparent;\n"
"background-image: url(:/resources/common/p0.jpg);\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setStyleSheet("background:rgba(255, 255, 255,150)")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        self.frame_7.setStyleSheet("background:transparent")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background:rgba(255,255,255,200);\n"
"border-radius:12px")
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.frame_8 = QtWidgets.QFrame(self.frame_7)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.Name = QtWidgets.QLineEdit(self.frame_8)
        self.Name.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.Name.setObjectName("Name")
        self.horizontalLayout_5.addWidget(self.Name)
        self.verticalLayout_3.addWidget(self.frame_8)
        self.frame_12 = QtWidgets.QFrame(self.frame_7)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.User = QtWidgets.QLineEdit(self.frame_12)
        self.User.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.User.setObjectName("User")
        self.horizontalLayout_9.addWidget(self.User)
        self.verticalLayout_3.addWidget(self.frame_12)
        self.frame_10 = QtWidgets.QFrame(self.frame_7)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.frame_10)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.Protocal = QtWidgets.QLineEdit(self.frame_10)
        self.Protocal.setEnabled(True)
        self.Protocal.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.Protocal.setReadOnly(True)
        self.Protocal.setObjectName("Protocal")
        self.horizontalLayout_7.addWidget(self.Protocal)
        self.verticalLayout_3.addWidget(self.frame_10)
        self.frame_11 = QtWidgets.QFrame(self.frame_7)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.Port = QtWidgets.QLineEdit(self.frame_11)
        self.Port.setValidator(QtGui.QIntValidator())
        self.Port.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.Port.setObjectName("Port")
        self.horizontalLayout_8.addWidget(self.Port)
        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 30)
        self.verticalLayout_3.addWidget(self.frame_11)
        self.frame_13 = QtWidgets.QFrame(self.frame_7)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_8 = QtWidgets.QLabel(self.frame_13)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_11.addWidget(self.label_8)
        self.Host_2 = QtWidgets.QLineEdit(self.frame_13)
        self.Host_2.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.Host_2.setObjectName("Host_2")
        self.horizontalLayout_11.addWidget(self.Host_2)
        self.verticalLayout_3.addWidget(self.frame_13)
        self.frame_9 = QtWidgets.QFrame(self.frame_7)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.Host = QtWidgets.QLineEdit(self.frame_9)
        self.Host.setStyleSheet("background:rgba(255,255,255,200);\n"
"padding:6px;\n"
"border-radius:10px")
        self.Host.setObjectName("Host")
        self.horizontalLayout_6.addWidget(self.Host)
        self.verticalLayout_3.addWidget(self.frame_9)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout_3.setStretch(2, 2)
        self.verticalLayout_3.setStretch(3, 2)
        self.verticalLayout_3.setStretch(4, 2)
        self.verticalLayout_3.setStretch(6, 2)
        self.horizontalLayout_4.addWidget(self.frame_7)
        self.horizontalLayout_3.addWidget(self.frame_6)
        self.horizontalLayout_3.setStretch(0, 3)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(50, 50))
        self.frame_3.setStyleSheet("border-radius:0;\n"
"background:transparent;\n"
"")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(15, 6, 15, 6)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Confirm = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Confirm.sizePolicy().hasHeightForWidth())
        self.Confirm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.Confirm.setFont(font)
        self.Confirm.setStyleSheet("border-radius:18px;\n"
"background:rgba(255, 255, 255);\n"
"")
        self.Confirm.setFlat(False)
        self.Confirm.setObjectName("Confirm")
        self.horizontalLayout_2.addWidget(self.Confirm)
        self.Cancel = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Cancel.sizePolicy().hasHeightForWidth())
        self.Cancel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.Cancel.setFont(font)
        self.Cancel.setStyleSheet("background:rgb(255, 255, 255);\n"
"border-radius:18px")
        self.Cancel.setFlat(True)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout_2.addWidget(self.Cancel)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "新建会话"))
        self.label_2.setText(_translate("Form", " 名称 "))
        self.label_6.setText(_translate("Form", "用户名"))
        self.label_4.setText(_translate("Form", " 协议 "))
        self.Protocal.setText(_translate("Form", "FTP"))
        self.label_5.setText(_translate("Form", " 端口 "))
        self.label_8.setText(_translate("Form", " 主机 "))
        self.label_3.setText(_translate("Form", " 口令 "))
        self.Confirm.setText(_translate("Form", "确定"))
        self.Cancel.setText(_translate("Form", "取消"))
