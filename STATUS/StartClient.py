import threading

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import *
# from PySide2.QtUiTools import QUiLoader
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QFile
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import PyQt5
import os
import sys
from src import user
from client import Ui_MainWindow
from login import Ui_loginForm

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class LoginWin(QDialog, Ui_loginForm):
    def __init__(self, parent=None):
        super(LoginWin, self).__init__(parent)

        self.setupUi(self)

        self.closeBtn.clicked.connect(self.close)

        # an example
        self.sessionTbl.insertRow(0)
        for col, text in enumerate(['whuftp', 'user1', 'FTP', '21', '172.16.20.1', '123456']):
            self.sessionTbl.setItem(0, col, QTableWidgetItem(text))

        self.sessionTbl.setColumnHidden(5, True)  # 隐藏密码

    def get_selected_row(self):
        row = self.sessionTbl.currentIndex().row()
        user = self.sessionTbl.item(row, 1).text()
        port = self.sessionTbl.item(row, 3).text()
        host = self.sessionTbl.item(row, 4).text()
        password = self.sessionTbl.item(row, 5).text()

        return user, port, host, password


class ClientUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ClientUI, self).__init__(parent)

        self.setupUi(self)

        self.loginWin = LoginWin()

    def closeEvent(self, e):
        reply = QMessageBox.question(self,
                                     '询问',
                                     "确定要退出客户端吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            e.accept()
            sys.exit(0)
        else:
            e.ignore()


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ftpserver = None  # 所连接到的服务器实例
        qfile_stats = QFile("client.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.loginWin = LoginWin()
        self.ui = ClientUI()
        # self.ui.button.clicked.connect(self.handleCalc)

        # signal slots
        self.ui.eButton.clicked.connect(self.exit)  # 退出按键操作
        self.ui.ulButton.clicked.connect(self.upload)  # 上传按键操作
        self.ui.upButton.setEnabled(False)  # 返回上层按键操作
        self.ui.dButton.setEnabled(False)  # 下载按键操作
        self.ui.qButton.clicked.connect(self.connect_server)  # 查询按键操作

        self.loginWin.connectBtn.clicked.connect(self.connect_shortcut)

        self.client_root = 'home'
        self.modelt = QFileSystemModel()
        self.modelt.setRootPath(self.client_root)

        # 为控件添加模式。
        self.ui.treeView.setModel(self.modelt)
        self.ui.treeView.setRootIndex(self.modelt.index(self.client_root))  # 只显示设置的那个文件路径。
        self.ui.treeView.doubleClicked.connect(self.file_name)  # 双击文件打开

        # Qt的文件模型似乎只能显示本机的文件系统
        self.server_root = ''  # 服务器端的文件目录。客户端初始化时为空，用户登录后显示
        self.modelt2 = QFileSystemModel()
        ####################################################
        # 成功连接后再显示远程目录，而非初始化客户端时
        # self.modelt2.setRootPath(self.server_root)  ##<-这里后续修改Path值#
        ####################################################
        self.ui.treeView_2.setModel(self.modelt2)
        # self.ui.treeView_2.setRootIndex(self.modelt2.index(self.server_root))  # 只显示设置的那个文件路径。
        self.ui.treeView_2.doubleClicked.connect(self.file_name)  # 双击文件打开

    def upload(self):
        QMessageBox.about(
            self.ui, '登入信息',
            f'''域名：\n{self.ui.domainEdit.text()}\n端口：\n{self.ui.portEdit.text()}\n用户名：\n{self.ui.nameEdit.text()}\n口令：\n{self.ui.pwEdit.text()}'''
        )

    def file_name(self, Qmodelidx):
        print(self.modelt.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.modelt.fileName(Qmodelidx))  # 输出文件名

    def exit(self):
        reply = QMessageBox.question(self.ui,
                                     '询问',
                                     "确定要退出客户端吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(app.exec())  # 更正退出
        else:
            pass

    def connect_shortcut(self):
        user, port, host, password = self.loginWin.get_selected_row()
        self.ui.nameEdit.setText(user)
        self.ui.portEdit.setText(port)
        self.ui.domainEdit.setText(host)
        self.ui.pwEdit.setText(password)
        self.loginWin.close()

    def connect_server(self):
        # 注册线程来连接服务器，防止服务器未开启等情况时客户端卡死
        thread = threading.Thread(target=self._connect_server)
        thread.setDaemon(True)
        thread.start()

    def _connect_server(self):
        self.ui.serverLbl.setText('远程目录列表（连接中……）：')
        try:
            self.ftpserver = user.ftpconnect(
                host=self.ui.domainEdit.text(),
                username=self.ui.nameEdit.text(),
                password=self.ui.pwEdit.text(),
                port=int(self.ui.portEdit.text()))

            self.server_root = '../user_dir'  # 感觉不是很合理……
            self.modelt2.setRootPath(self.server_root)
            self.ui.treeView_2.setRootIndex(self.modelt2.index(self.server_root))
            self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 170, 255, 200);")
            self.ui.serverLbl.setText('远程目录列表：')

        except:
            self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 0, 0, 200);")
            self.ui.serverLbl.setText('远程目录列表（连接失败！）：')
            # QMessageBox.warning(self.ui, '警告', f'''{e}''')    # 弹窗会卡死


app = QApplication([])
stats = Stats()
stats.loginWin.exec()
stats.ui.show()
sys.exit(app.exec())  # 安全结束
