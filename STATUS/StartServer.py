from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from server import Ui_ServerWindow
from adduser import Ui_addUserForm


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

        self.setupUi(self)

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


class Server:
    def __init__(self):
        self.server = None  # ftp server
        self.mainWin = ServerUI()
        self.addUserWin = AddUserWin()

        sys.stdout = EmitStr(textWrite=self.outputWriteInfo)  # redirect stdout
        sys.stderr = EmitStr(textWrite=self.outputWriteError)  # redirect stderr

        self.name = 'whuftp'  # server name
        self.address = ''  # ipv4 address of the host
        self.port = 21  # default is 21
        self.read_limit = 300 * 1024  # 300 kb/s
        self.write_limit = 300 * 1024  # 300 kb/s
        self.max_cons = 150
        self.max_cons_per_ip = 15
        self.file_root = '../user_dir'  # 文件根目录

        self.model = QFileSystemModel()
        self.mainWin.treeView.setModel(self.model)
        # self.mainWin.treeView.doubleClicked.connect(self.file_name) # 打开文件

        self.initInfo()
        self.initSignalSlots()

    def initInfo(self):
        self.mainWin.nameEdit.setText(self.name)
        self.mainWin.addressEdit.setText(self.address)
        self.mainWin.portEdit.setText(str(self.port))
        self.mainWin.maxconEdit.setText(str(self.max_cons))
        self.mainWin.maxconipEdit.setText(str(self.max_cons_per_ip))
        self.mainWin.readlimEdit.setText(str(self.read_limit))
        self.mainWin.writelimEdit.setText(str(self.write_limit))

    def initSignalSlots(self):
        self.mainWin.applyBtn.clicked.connect(self.apply_server)
        self.mainWin.resetBtn.clicked.connect(self.reset_server)
        self.mainWin.addUserBtn.clicked.connect(self.add_user)
        self.mainWin.delUserBtn.clicked.connect(self.delete_user)

        self.addUserWin.addUserBtn.clicked.connect(self.confirm_add_user)

    # 应用服务器
    def apply_server(self):
        # placeholder
        self.mainWin.stateLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 170, 255, 200);")
        self.mainWin.stateLbl.setText('状态：已开启')
        print('Successfully started the server!')

    # 重置服务器
    def reset_server(self):
        pass

    # 添加用户
    def add_user(self):
        # modification is needed
        self.addUserWin.show()
        
    # 确认添加用户
    def confirm_add_user(self):
        pass

    # 删除用户
    def delete_user(self):
        pass

    # 输出日志至text browser
    def outputWriteInfo(self, text):
        self.mainWin.logBrowser.append(text)

    def outputWriteError(self, text):
        # 错误信息用红色输出
        self.mainWin.logBrowser.append(f'<font color=\'#FF0000\'>{text}</font>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.mainWin.show()
    sys.exit(app.exec_())