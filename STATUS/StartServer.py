import os
import threading
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from server import Ui_ServerWindow
from adduser import Ui_addUserForm
from src.ClientServer import WHUFTPServer

class EmitStr(QObject):
    textWrite = pyqtSignal(str)

    def write(self, text):
        self.textWrite.emit(str(text))


class AddUserWin(QWidget, Ui_addUserForm):
    def __init__(self):
        super().__init__()

        self.setupUi(self)


class ServerUI(QMainWindow, Ui_ServerWindow):
    def __init__(self, parent=None):
        super(ServerUI, self).__init__(parent)

        # sys.stdout = EmitStr(textWrite=self.outputWriteInfo)  # redirect stdout
        # sys.stderr = EmitStr(textWrite=self.outputWriteError)  # redirect stderr

        self.setupUi(self)

        # debug use
        self.nameEdit.setText('whuftp')
        self.addressEdit.setText('172.16.20.195')
        self.portEdit.setText('21')
        self.rootEdit.setText('../user_dir')
        self.dbEdit.setText('../src/user_info.db')
        self.maxconEdit.setText('150')
        self.maxconipEdit.setText('15')
        self.readlimEdit.setText('300')
        self.writelimEdit.setText('300')

        self.rootBtn.clicked.connect(self.chosseRoot)
        self.dbBtn.clicked.connect(self.chooseDatabase)

    def chosseRoot(self):
        dir_path = QFileDialog.getExistingDirectory(self,
                                                    '选择服务器根目录',
                                                    '/home')
        if dir_path:
            self.rootEdit.setText(dir_path)

    def chooseDatabase(self):
        db_path = QFileDialog.getOpenFileName(self,
                                              '选择服务器数据库',
                                              '/home')
        if db_path[0]:
            self.dbEdit.setText(db_path[0])




    def closeEvent(self, e):
        reply = QMessageBox.question(self,
                                     '询问',
                                     "确定要退出服务器吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            e.accept()
            sys.exit(0)
        else:
            e.ignore()

    # 输出日志至text browser
    def outputWriteInfo(self, text):
        self.logBrowser.append(text)

    def outputWriteError(self, text):
        # 错误信息用红色输出
        self.logBrowser.append(f'<font color=\'#FF0000\'>{text}</font>')


class Server:
    def __init__(self):
        self.server = None  # ftp server
        self.thread_server = threading.Thread() # 服务器运行线程，防止GUI卡死
        self.mainWin = ServerUI()
        self.addUserWin = AddUserWin()



        self.model = QFileSystemModel()
        self.mainWin.treeView.setModel(self.model)
        self.mainWin.treeView.doubleClicked.connect(self.file_name)  # 打开文件

        self.initSignalSlots()

    def initSignalSlots(self):
        self.mainWin.applyBtn.clicked.connect(self.apply_server)
        self.mainWin.startBtn.clicked.connect(self.start_server)
        self.mainWin.closeBtn.clicked.connect(self.close_server)
        self.mainWin.resetBtn.clicked.connect(self.reset_server)

        self.mainWin.addUserBtn.clicked.connect(self.add_user)
        self.mainWin.updateBtn.clicked.connect(self.update_user_list)
        self.mainWin.delUserBtn.clicked.connect(self.delete_user)
        self.addUserWin.addUserBtn.clicked.connect(self.confirm_add_user)

    # 应用服务器
    def apply_server(self):
        thread_apply = threading.Thread(target=self._apply_server)
        thread_apply.setDaemon(True)
        thread_apply.start()

    def _apply_server(self):
        self.mainWin.stateLbl.setText('状态：应用中……')
        # time.sleep(10) # debug use
        try:
            name = self.mainWin.nameEdit.text() # seems to be dummy...
            address = self.mainWin.addressEdit.text()
            port = self.mainWin.portEdit.text()
            root_dir = self.mainWin.rootEdit.text()
            log_path = os.path.join(root_dir, 'LOG.log')  # 根目录下生成日志
            db_path = self.mainWin.dbEdit.text()
            max_cons = self.mainWin.maxconEdit.text()
            max_cons_per_ip = self.mainWin.maxconipEdit.text()
            read_limit = self.mainWin.readlimEdit.text()
            write_limit = self.mainWin.writelimEdit.text()

            # NOTE: 避免invalid literal for int() with base 10而卡死
            try:
                port = int(port)
                max_cons = int(max_cons)
                max_cons_per_ip = int(max_cons_per_ip)
                read_limit = int(read_limit) * 1024  # GUI上填写的时KB/s
                write_limit = int(write_limit) * 1024

                self.server = WHUFTPServer(
                    address, port,
                    read_limit, write_limit,
                    max_cons, max_cons_per_ip,
                    root_dir, log_path, db_path,
                )

                self.server.apply_server()
                self.mainWin.applyBtn.setDisabled(True)
                self.mainWin.startBtn.setDisabled(False)
                self.mainWin.stateLbl.setStyleSheet(
                    "color: rgb(255, 255, 255); background-color: rgba(0, 170, 0, 200);")
                self.mainWin.stateLbl.setText('状态：应用服务器成功！')

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
            self.server.close_server()
            self.server = None
            self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 0, 0, 200);")
            self.mainWin.stateLbl.setText('状态：应用服务器失败！')

    # 开启服务器
    def start_server(self):
        if self.server is None:
            QMessageBox.warning(self.mainWin, '警告', '请先应用服务器！')
        else:
            self.mainWin.stateLbl.setText('状态：启动服务器中……')
            try:
                self.thread_server = threading.Thread(target=self.server.start_server)
                self.thread_server.setDaemon(True)  # 守护线程
                self.thread_server.start()

                self.mainWin.startBtn.setDisabled(True)
                self.mainWin.applyBtn.setDisabled(True)
                self.mainWin.closeBtn.setDisabled(False)
                self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 170, 255, 200);")
                self.mainWin.stateLbl.setText('状态：已开启')


                # 显示文件目录
                self.model.setRootPath(self.server.root_dir)
                self.mainWin.treeView.setRootIndex(self.model.index(self.server.root_dir))
            except Exception as e:
                self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 0, 0, 200);")
                self.mainWin.stateLbl.setText('状态：启动服务器失败！')

    def close_server(self):
        if self.server:
            self.server.close_server()
            self.server = None
            self.mainWin.startBtn.setDisabled(True)
            self.mainWin.applyBtn.setDisabled(False)
            self.mainWin.closeBtn.setDisabled(True)
            self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(128, 128, 128, 200);")
            self.mainWin.stateLbl.setText('状态：未开启')

    # 重置服务器
    def reset_server(self):
        if self.server:
            self.server.close_server()
            self.server = None
        self.mainWin.nameEdit.setText('')
        self.mainWin.addressEdit.setText('')
        self.mainWin.portEdit.setText('')
        self.mainWin.rootEdit.setText('')
        self.mainWin.dbEdit.setText('')
        self.mainWin.maxconEdit.setText('')
        self.mainWin.maxconipEdit.setText('')
        self.mainWin.readlimEdit.setText('')
        self.mainWin.writelimEdit.setText('')
        self.mainWin.startBtn.setDisabled(True)
        self.mainWin.applyBtn.setDisabled(False)
        self.mainWin.closeBtn.setDisabled(True)
        self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(128, 128, 128, 200);")
        self.mainWin.stateLbl.setText('状态：未创建')


    def update_user_list(self):
        if self.server:
            try:
                self.mainWin.userTbl.setRowCount(0)
                self.mainWin.userTbl.clearContents()
                user_info = self.server.authorizer.user_table
                for row, item in enumerate(user_info.items()):
                    username = item[0]
                    password = item[1]['pwd']
                    permission = item[1]['perm']
                    self.mainWin.userTbl.insertRow(row)
                    self.mainWin.userTbl.setItem(row, 0, QTableWidgetItem(username))
                    self.mainWin.userTbl.setItem(row, 1, QTableWidgetItem(password))
                    self.mainWin.userTbl.setItem(row, 2, QTableWidgetItem(permission))
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self.mainWin,
                                '警告',
                                '请先打开服务器！')


    # 添加用户
    def add_user(self):
        # modification is needed
        if self.server:
            self.addUserWin.show()
        else:
            QMessageBox.warning(self.mainWin,
                                '警告',
                                '请先打开服务器！')

    # 确认添加用户
    def confirm_add_user(self):
        # TODO: 赋予不同权限
        username = self.addUserWin.nameEdit.text()
        password = self.addUserWin.passwordEdit.text()
        if self.server and username and password:
            try:
                self.server.register(username, password)
            except Exception as e:
                print(e)
            else:
                print(f'Successfully add user {username}!')
                self.addUserWin.close()


    def get_selected_user(self):
        row = self.mainWin.userTbl.currentIndex().row()
        username = self.mainWin.userTbl.item(row, 0).text()
        print(username)
        # password = self.mainWin.userTbl.item(row, 2).text()
        # permission = self.mainWin.userTbl.item(row, 3).text()

        return  username

    # 删除用户
    def delete_user(self):
        if self.server:
            try:
                username = self.get_selected_user()
            except Exception as e:
                print(e)
            else:
                reply = QMessageBox.question(self.mainWin,
                                             '询问',
                                             f'确定要删除用户{username}吗？',
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No
                                             )
                if reply == QMessageBox.Yes:
                    try:
                        self.server.authorizer.remove_user(username)
                        user_dir =  os.path.join(self.server.root_dir, username)
                        # NOTE: 删除用户文件（optional）
                        # 直接这么删除有问题，会报错[WinError 5] 拒绝访问。暂时为解决
                        # if os.path.exists(user_dir):
                        #     os.remove(user_dir)
                        print(f'Successfully removed user {username}!')
                        self.update_user_list()
                    except Exception as e:
                        print(e)
                else:
                    pass
        else:
            QMessageBox.warning(self.mainWin,
                                '警告',
                                '请先打开服务器！')


    def file_name(self, Qmodelidx):
        print(self.model.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.model.fileName(Qmodelidx))  # 输出文件名



if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.mainWin.show()
    sys.exit(app.exec_())
