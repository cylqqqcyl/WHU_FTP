import threading
import json
import ProcessBar as PB
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5
import os
from src.ClientServer import WHUFTPClient
from client import Ui_MainWindow
from login import Ui_loginForm
from Transmission import Ui_Form
import traceback
import time
from ftplib import FTP
import sys, getpass, os.path
import src.user as user
import threading

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


# NOTE: 无法在子线程中弹窗。故弹窗动作要放在主线程，子线程只负责告诉主线程是否弹窗。
class MsgThread(QThread):
    msgSigal = pyqtSignal()  # 弹窗信号

    def __init__(self):
        super(MsgThread, self).__init__()

    def run(self):
        self.msgSigal.emit()  # 发送信号至主线程


class TransWin(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(TransWin, self).__init__(parent)

        self.setupUi(self)

        self.CloseBtn.clicked.connect(self.close)

        # 设置一个值表示进度条的当前进度
        self.pv = 0
        # 声明一个时钟控件
        #self.timer1 = QBasicTimer()

        '''设置下载页面进度条参数'''
        self.DownloadBar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);"
            "  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); "
            "border-radius: 10px; margin: 0.1px;  width: 1px;}")
        self.DownloadBar.setMinimum(0)      # 设置进度条的范围
        self.DownloadBar.setMaximum(100)
        self.DownloadBar.setValue(self.pv)  #设置当前值
        self.DownloadBar.setFormat('Loaded  %p%'.format(self.DownloadBar.value() - self.DownloadBar.minimum()))   # 设置进度条文字格式

        '''设置上传页面进度条参数'''
        self.UploadBar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);"
            "  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); "
            "border-radius: 10px; margin: 0.1px;  width: 1px;}")
        self.UploadBar.setMinimum(0)
        self.UploadBar.setMaximum(100)
        self.UploadBar.setValue(self.pv)
        self.UploadBar.setFormat('Loaded  %p%'.format(self.UploadBar.value() - self.UploadBar.minimum()))



class LoginWin(QDialog, Ui_loginForm):
    def __init__(self, parent=None):
        super(LoginWin, self).__init__(parent)

        self.setupUi(self)

        #self.closeBtn.clicked.connect(self.close)

        # 获取上次的config
        with open('cache/config_client.json', "r") as f:
            data = f.read()
        config = json.loads(data)
        self.config = config

        self.sessionTbl.insertRow(0)
        for col, text in enumerate(config.values()):
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

    def saveConfig(self):
        name = 'whuftp'
        username = self.nameEdit.text()
        protocol = 'FTP'
        port = self.portEdit.text()
        domain = self.domainEdit.text()
        password = self.pwEdit.text()

        config = self.loginWin.config
        values = [name, username, protocol, port, domain, password]
        keys = config.keys()
        for (key, value) in zip(keys, values):
            if value:
                config[key] = value

            data = json.dumps(config)
            with open('cache/config_client.json', 'w') as f:
                f.write(data)

    def closeEvent(self, e):
        reply = QMessageBox.question(self,
                                     '询问',
                                     "确定要退出客户端吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.saveConfig()
            e.accept()
            sys.exit(0)
        else:
            e.ignore()


class Client:
    def __init__(self):
        # 从文件中加载UI定义
        self.I = 0

        self.ftpuser = None
        self.username = ''
        self.password = ''

        self.ftpserver = None  # 所连接到的服务器实例
        self.current_remote_dir = None  # 当前服务器目录

        self.loginWin = LoginWin()
        self.ui = ClientUI()
        # self.ui.button.clicked.connect(self.handleCalc)

        # signal slots
        self.ui.eButton.clicked.connect(self.exit)  # 退出按键操作
        self.ui.ulButton.clicked.connect(self.upload)  # 上传按键操作
        self.ui.dButton.clicked.connect(self.download)  # 下载按键操作
        self.ui.upButton.setEnabled(False)  # 返回上层按键禁止
        self.ui.ulButton.setEnabled(False)  # 上传按键禁止
        self.ui.dButton.setEnabled(False)  # 下载按键禁止
        self.ui.tsButton.clicked.connect(self.trans_list)
        self.ui.qButton.clicked.connect(self.connect_server)  # 查询按键操作

        self.loginWin.connectBtn.clicked.connect(self.connect_shortcut)
        self.loginWin.closeBtn.clicked.connect(self.exit)

        self.client_root = 'home'
        self.modelt = QFileSystemModel()
        self.modelt.setRootPath(self.client_root)

        # 为控件添加模式。
        self.ui.treeView.setModel(self.modelt)
        self.ui.treeView.setRootIndex(self.modelt.index(self.client_root))  # 只显示设置的那个文件路径。
        self.ui.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.treeView.doubleClicked.connect(self.file_name)  # 双击文件打开

        # 远程文件目录的icon
        cur_dir = os.getcwd()
        icon_dir_path = os.path.join(cur_dir, 'resources/common/directory.png')
        icon_file_path = os.path.join(cur_dir, 'resources/common/text.png')
        icon_ukn_path = os.path.join(cur_dir, 'resources/common/unknown.png')
        self.icon_dir = QIcon()
        self.icon_file = QIcon()
        self.icon_ukn = QIcon()
        self.icon_dir.addPixmap(QPixmap(icon_dir_path))
        self.icon_file.addPixmap(QPixmap(icon_file_path))
        self.icon_ukn.addPixmap(QPixmap(icon_ukn_path))
        self.server_root = '/'
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.doubleClicked.connect(self.change_dir)

        self.remote_file = None
        self.remote_dir = ''
        self.local_file = None
        self.local_dir = None

        self.exception = ''
        self.msgthread = MsgThread()
        self.msgthread.msgSigal.connect(lambda: self.show_msg(self.exception))

        '''以下为传输列表相关'''
        self.trans = TransWin() #实例化窗口
        #self.trans_key=0        #变量控制窗口是否打开，1表示已打开，0表示未打开

    def show_msg(self, msg):
        QMessageBox.warning(self.ui, 'Warning', msg)

    def apply_client(self):

        username = self.ui.nameEdit.text()
        password = self.ui.pwEdit.text()
        host = self.ui.domainEdit.text()
        port = self.ui.portEdit.text()

        try:
            port = int(port)
            self.ftpuser = WHUFTPClient(username, password, host, port)
        except Exception as e:
            print(e)

    def download(self):
        #在传输列表中插入一行

        row_count=self.trans.DownloadList.rowCount()        #当前行数
        self.trans.DownloadList.insertRow(int(row_count))   #当前行后插入

        #获取文件名
        tmp = -1
        while (self.remote_file[tmp] != '/'):
            tmp -= 1
        if self.local_dir[-1] == '/':
            tmp += 1

        #插入文件名
        file_name = QTableWidgetItem(self.remote_file[tmp:])
        self.trans.DownloadList.setItem(row_count, 0, file_name)
        self.trans.DfileName.setText(self.remote_file[tmp:])
        #self.trans.DfileName.setReadOnly()
        #插入开始时间
        start_time = QTableWidgetItem(time.asctime())
        self.trans.DownloadList.setItem(row_count, 2, start_time)
        #插入文件大小
        size_kb = round(self.ftpserver.size(self.remote_file)/1024,3)
        file_size = QTableWidgetItem(str(size_kb)+'KB')
        self.trans.DownloadList.setItem(row_count, 1, file_size)

        '''这里是文件下载的函数调用
            进度条思路：
            获取获取当前已传输的文件大小a，
            已知文件总大小为b，
            进行如下赋值：self.trans.pv=100*a/b #pv为进度条对应的完成度
                        self.trans.UploadBar.setValue(self.trans.pv) #将上述值赋予进度条即可显示
            '''
        user.downloadfile(self.ftpserver, self.remote_file,self.local_dir + self.remote_file[tmp:])
        # print(os.path.getsize(self.local_dir + self.remote_file[tmp:]))
        # print("bendi")
        # print(self.ftpserver.size(self.remote_file))
        if(os.path.getsize(self.local_dir + self.remote_file[tmp:]) == self.ftpserver.size(self.remote_file)):
            self.trans.DownloadBar.setValue(self.trans.pv)
        #self.trans.pv=50
        #self.trans.DownloadBar.setValue(self.trans.pv)

        #插入结束时间
        end_time = QTableWidgetItem(time.asctime())
        for i in range(101):
            time.sleep((0.00001))
            self.trans.DownloadBar.setValue(i)


        self.trans.DownloadList.setItem(row_count, 3, end_time)

        self.trans_list()

        #print(sys.getsizeof(self.remote_file))


        #downLoader = downloadThread(self.local_dir + self.remote_file[tmp:], self.remote_file, self.ftpserver)  # 实例化一个下载类，并传入下载链接和保存路径
        #downLoader.download_proess_signal.connect(downLoader.change_progressbar_value)  # 处理下载类的信号
        #downLoader.start()  # 开启子线程
        #downLoader.exec()  # 保护子线程，否则主线程调用函数结束的时候子线程也被迫退出3.
        #PB.download_ftp(self.ftpserver, self.local_dir + self.remote_file[tmp:], self.remote_file)

        return 0

    def upload(self):
        #在传输列表中插入一行
        row_count=self.trans.UploadList.rowCount()        #当前行数
        self.trans.UploadList.insertRow(int(row_count))   #当前行后插入

        tmp = -1
        while (self.local_file[tmp] != '/'):
            tmp -= 1

        #插入文件名
        file_name = QTableWidgetItem(self.local_file[tmp+1:])
        self.trans.UploadList.setItem(row_count, 0, file_name)
        self.trans.UfileName.setText(self.local_file[tmp+1:])
        #self.trans.DfileName.setReadOnly()
        #插入开始时间
        start_time = QTableWidgetItem(time.asctime())
        self.trans.UploadList.setItem(row_count, 2, start_time)
        #插入文件大小
        size_kb = round(os.path.getsize(self.local_file)/1024,3)
        file_size = QTableWidgetItem(str(size_kb)+'KB')
        self.trans.UploadList.setItem(row_count, 1, file_size)

        #print(self.local_file)

        #print(self.local_file[tmp:])

        #print(self.remote_file)

        #print(self.remote_dir)

        #print(self.remote_dir + self.local_file[tmp:])

        '''
        1.下面一行代码会报错（闪退），注释后可正常运行其余部分
        2.代码主要实现文件上传
        3.该部分与图界面进度条交互未实现
        '''
        user.uploadfile(self.ftpserver, self.local_file, self.remote_dir + self.local_file[tmp:])

        self.trans_list()

        end_time = QTableWidgetItem(time.asctime())
        self.trans.UploadList.setItem(row_count, 3, end_time)


        #user.uploadfile(self.ftpserver, self.local_file, self.remote_dir + self.local_file[tmp:])
        #PB.upload_file(self.ftpserver, self.local_file, '/' + self.remote_dir + self.local_file[tmp:])

        # user.uploadfile(self.ftpserver,'D:/asoul.txt', '/'Francis/asoul.txt')
        # QMessageBox.about(
        #     self.ui, '登入信息',
        #     f'''域名：\n{self.ui.domainEdit.text()}\n端口：\n{self.ui.portEdit.text()}\n用户名：\n{self.ui.nameEdit.text()}\n口令：\n{self.ui.pwEdit.text()}'''
        # )

    def file_name(self, Qmodelidx):
        tm_path = self.modelt.filePath(Qmodelidx)
        # print(self.modelt.fileInfo(Qmodelidx).suffix())
        # print(self.modelt.filePath(Qmodelidx))  # 输出文件的地址。
        # print(self.modelt.fileName(Qmodelidx))  # 输出文件名
        if os.path.isfile(tm_path):  # 本地当前选中为文件
            self.local_file = tm_path
            self.ui.ulButton.setEnabled(True and self.remote_dir != None)  # 上传按键允许
        else:  # 本地当前选中为文件夹
            self.local_file = None
            self.local_dir = tm_path
            self.ui.ulButton.setEnabled(False)  # 上传按键禁止

    def exit(self):
        reply = QMessageBox.question(self.ui,
                                     '询问',
                                     "确定要退出客户端吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.saveConfig()

            sys.exit(0)  # 更正退出
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

        self.apply_client()

        self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(128, 128, 128, 200);")
        self.ui.serverLbl.setText('远程目录列表（连接中……）：')
        try:
            self.ftpserver = self.ftpuser.connect_server()
            self.current_remote_dir = self.ftpserver.pwd()

            self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(0, 170, 255, 200);")
            self.ui.serverLbl.setText('远程目录列表：')
            root_files = self.ftpuser.get_server_files(self.ftpserver)

            # 清空远程目录
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.clearContents()

            for Name, Size, Type, Date in root_files:
                file = [Name, Size, Type, Date]

                if file[-2] == 'file':
                    icon = self.icon_file
                elif file[-2] == 'dir':
                    icon = self.icon_dir
                else:
                    # unknown file type
                    icon = self.icon_ukn
                row_count = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_count)
                for col, text in enumerate(file):
                    if col == 0:
                        self.ui.tableWidget.setItem(row_count, col, QTableWidgetItem(icon, text))
                    else:
                        self.ui.tableWidget.setItem(row_count, col, QTableWidgetItem(text))
            # x = 1 / 0  # debug use
        except Exception as e:
            self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 0, 0, 200);")
            self.ui.serverLbl.setText('远程目录列表（连接失败！）：')
            # traceback.print_exc() # debug use
            self.exception = str(e)
            self.msgthread.start()

    def change_dir(self):
        row = self.ui.tableWidget.currentRow()
        target_type = self.ui.tableWidget.item(row, 2).text()
        target_dir = self.ui.tableWidget.item(row, 0).text()
        # print("ddddddddddddddddddddddddddddddddddddd"+target_dir)
        # print("[pppppppppppppppppppppppppppppppppppp"+target_type)
        cur_dir = self.ftpuser.get_server_files(self.ftpserver)
        # user.downloadfile(self.ftpserver, target_dir, 'D:/asoul.txt')

        # 返回上一级目录
        if row == 0 and target_dir == '..' and cur_dir != '/':
            self.ftpserver.cwd('..')
            files = self.ftpuser.get_server_files(self.ftpserver)
            cur_dir = self.ftpserver.pwd()
            if cur_dir == '/':  # 回到了根目录
                self.ui.tableWidget.setRowCount(0)
                self.ui.tableWidget.clearContents()
            else:  # 不是根目录
                self.ui.tableWidget.setRowCount(1)  # 第一行用于返回上一级目录
                self.ui.tableWidget.clearContents()
                for col, text in enumerate(['..', ' ', ' ', ' ', ' ']):
                    self.ui.tableWidget.setItem(0, col, QTableWidgetItem(text))
        # 进入子目录
        elif target_type == 'dir':
            self.ftpserver.cwd(target_dir)
            files =self.ftpuser.get_server_files(self.ftpserver)
            self.ui.tableWidget.setRowCount(1)
            self.ui.tableWidget.clearContents()
            for col, text in enumerate(['..', ' ', ' ', ' ', ' ']):
                self.ui.tableWidget.setItem(0, col, QTableWidgetItem(text))

        else:
            self.remote_dir = self.ftpserver.pwd()
            if target_type != 'file':
                self.remote_file = None
                self.ui.dButton.setEnabled(False)  # 下载按键禁止
            else:
                if self.remote_dir != '/':
                    self.remote_file = self.ftpserver.pwd() + '/' + target_dir
                else:
                    self.remote_file = '/' + target_dir
                self.ui.dButton.setEnabled(True)  # 下载按键允许
            # print('sdfsdf  ' + self.remote_dir+'\n',self.remote_file,self.ftpserver.pwd())
            return

        # 显示当前目录的文件并贴上图标
        for Name, Size, Type, Date in files:
            file = [Name, Size, Type, Date]
            if file[-2] == 'file':
                icon = self.icon_file
            elif file[-2] == 'dir':
                icon = self.icon_dir
            else:
                # unknown file type
                icon = self.icon_ukn
            row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_count)
            for col, text in enumerate(file):
                if col == 0:
                    self.ui.tableWidget.setItem(row_count, col, QTableWidgetItem(icon, text))
                else:
                    self.ui.tableWidget.setItem(row_count, col, QTableWidgetItem(text))

        self.remote_dir = self.ftpserver.pwd()[1:]
        if target_type != 'file':
            self.remote_file = None
            self.ui.dButton.setEnabled(False)  # 下载按键禁止
        else:
            self.remote_file = self.ftpserver.pwd() + '/' + target_dir
            self.ui.dButton.setEnabled(True)  # 下载按键允许
        # print('sdfsdf  ' + self.remote_dir + '\n', self.remote_file, self.ftpserver.pwd())

    def trans_list(self):
        self.trans.setWindowTitle('Transmission List')
        self.trans.show()




app = QApplication([])
stats = Client()
stats.loginWin.exec()
stats.ui.show()
sys.exit(app.exec())  # 安全结束
