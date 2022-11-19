import math
import threading
import json
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5
import os
import sys
import time
from src.ClientServer import WHUFTPClient
from client import Ui_MainWindow
from login import Ui_loginForm
from Transmission import Ui_Form

from NewLogin import NewLogin_Form

import queue

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class EmitStr(QObject):  # 日志输出类
    textWrite = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWrite.emit(str(text))


# NOTE: 无法在子线程中弹窗。故弹窗动作要放在主线程，子线程只负责告诉主线程是否弹窗。
class MsgThread(QThread):
    msgSigal = pyqtSignal()  # 弹窗信号

    def __init__(self):
        super(MsgThread, self).__init__()

    def run(self):
        self.msgSigal.emit()  # 发送信号至主线程


class ProgressSignal(QObject):  # 传输进度信号类
    progressSignal = pyqtSignal(int)

    def update_progress(self, progress):
        self.progressSignal.emit(progress)


class LoginWin(QDialog, Ui_loginForm):
    def __init__(self, parent=None):
        super(LoginWin, self).__init__(parent)

        self.setupUi(self)
        self.closeBtn.clicked.connect(self.close)
        self.delBtn.setEnabled(False)

        # 获取上次的config
        with open('cache/config_client.json', "r") as f:
            data = f.read()
            if len(data) == 0:
                config = [] #用列表存储多个连接信息
            else:
                config = json.loads(data)
            for line in config:
                currentRowCount = self.sessionTbl.rowCount()
                self.sessionTbl.insertRow(currentRowCount)
                self.sessionTbl.setItem(currentRowCount, 0, QTableWidgetItem(line['name']))

                self.sessionTbl.setItem(currentRowCount, 1, QTableWidgetItem(line['username']))
                self.sessionTbl.setItem(currentRowCount, 2, QTableWidgetItem("FTP"))
                self.sessionTbl.setItem(currentRowCount, 3, QTableWidgetItem(line['port']))
                self.sessionTbl.setItem(currentRowCount, 4, QTableWidgetItem(line['domain']))
                self.sessionTbl.setItem(currentRowCount, 5, QTableWidgetItem(line['password']))
                self.sessionTbl.setColumnHidden(5, True)  # 隐藏密码

        self.sessionTbl.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置登录界面信息只读

    def get_selected_row(self):
        row = self.sessionTbl.currentIndex().row()
        user = self.sessionTbl.item(row, 1).text()
        port = self.sessionTbl.item(row, 3).text()
        host = self.sessionTbl.item(row, 4).text()
        password = self.sessionTbl.item(row, 5).text()

        return user, port, host, password


class NewLogin(QDialog,NewLogin_Form):
    def __init__(self, parent=None):
        super(NewLogin, self).__init__(parent)

        self.setupUi(self)

        self.Cancel.clicked.connect(self.close)


class ClientUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ClientUI, self).__init__(parent)

        self.setupUi(self)

        self.loginWin = LoginWin()

        # transmission log
        # sys.stdout = EmitStr(textWrite=self.outputWriteInfo)  # redirect stdout
        # sys.stderr = EmitStr(textWrite=self.outputWriteError)  # redirect stderr


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

    def outputWriteInfo(self, text):
        self.logBrowser.append(text)

    def outputWriteError(self, text):
        # 错误信息用红色输出
        self.logBrowser.append(f'<font color=\'#FF0000\'>{text}</font>')

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

        self.ftpuser = None
        self.username = ''
        self.password = ''

        self.ftpserver = None  # 所连接到的服务器实例
        self.current_remote_dir = None  # 当前服务器目录
        self.NewSession = NewLogin() #新建会话
        self.NewSession.setWindowTitle('New Session')
        self.loginWin = LoginWin()
        self.ui = ClientUI()
        # self.trans = TransWin()  # 传输窗口
        # self.ui.button.clicked.connect(self.handleCalc)

        # signal slots
        self.ui.eButton.clicked.connect(self.exit)  # 退出按键操作
        self.ui.ulButton.clicked.connect(self.upload)  # 上传按键操作
        self.ui.dButton.clicked.connect(self.download)  # 下载按键操作
        self.ui.ulButton.setEnabled(False)  # 上传按键禁止
        self.ui.dButton.setEnabled(False)  # 下载按键禁止
        self.ui.connectBtn.clicked.connect(self.connect_server)  # 连接服务器
        self.ui.disconnectBtn.setEnabled(False)  # 断开连接
        self.ui.disconnectBtn.clicked.connect(self.disconnect_server)
        self.loginWin.connectBtn.clicked.connect(self.connect_shortcut)

        self.client_root = 'home'
        self.modelt = QFileSystemModel()
        self.modelt.setRootPath(self.client_root)
        self.loginWin.NewBtn.clicked.connect(self.NewSessionList) #新建会话
        self.loginWin.sessionTbl.cellClicked.connect(self.deleteOpetion)  # 单击文件打开
        self.loginWin.delBtn.clicked.connect(self.deleteRow) #删除行
        self.NewSession.Confirm.clicked.connect(self.AddData) #添加数据到login

        # 左侧本地文件树设置
        self.ui.treeView.setModel(self.modelt)
        self.ui.treeView.setRootIndex(self.modelt.index(self.client_root))  # 只显示设置的那个文件路径。
        self.ui.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.treeView.doubleClicked.connect(self.file_name)  # 双击文件打开
        self.ui.treeView.clicked.connect(self.file_name)  # 单击文件打开

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
        # 右侧远程文件table设置
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.doubleClicked.connect(self.change_dir)  # 双击操作
        self.ui.tableWidget.cellClicked.connect(self.file_selected)  # 单击操作

        self.ui.UploadList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.DownloadList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.remote_file = None
        self.remote_dir = None
        self.local_file = None
        self.local_dir = None
        self.cur_upload_count = 0  # 已上传文件block总量
        self.cur_download_size = 0.0  # 已下载文件总量
        self.target_upload_count = 0  # 上传文件block总量
        self.target_download_size = 0.0  # 下载文件总量

        # 初始状态下禁用上传下载列表的所有按钮
        self.ui.DeleteUploadBtn.setEnabled(False)
        self.ui.PauseUploadBtn.setEnabled(False)
        self.ui.ContinueUploadBtn.setEnabled(False)
        self.ui.PauseDownloadBtn.setEnabled(False)
        self.ui.DeleteDownloadBtn.setEnabled(False)
        self.ui.ContinueDownloadBtn.setEnabled(False)

        self.ui.UploadList.cellClicked.connect(self.upload_selected)
        self.ui.DownloadList.cellClicked.connect(self.download_selected)

        self.ui.DeleteUploadBtn.clicked.connect(self.delete_upload)
        self.ui.DeleteDownloadBtn.clicked.connect(self.delete_download)
        self.ui.PauseUploadBtn.clicked.connect(self.pause_upload)
        self.ui.PauseDownloadBtn.clicked.connect(self.pause_download)
        self.ui.ContinueUploadBtn.clicked.connect(self.continue_upload)
        self.ui.ContinueDownloadBtn.clicked.connect(self.continue_download)

        self.exception = ''
        self.msgthread = MsgThread()
        self.msgthread.msgSigal.connect(lambda: self.show_msg(self.exception))

        self.download_progressChanged = ProgressSignal(progressSignal=self.ui.DownloadBar.setValue)
        self.upload_progressChanged = ProgressSignal(progressSignal=self.ui.UploadBar.setValue)

        self.download_queue = queue.Queue()
        self.download_no = 0  # 下载队列中的任务数
        self.upload_queue = queue.Queue()
        self.upload_no = 0  # 上传队列中的任务数

        self.download_thread = None
        self.download_closing_event = threading.Event()
        self.upload_thread = None
        self.upload_closing_event = threading.Event()

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
        if self.local_dir:
            file_name = self.ui.tableWidget.selectedItems()[0].text()
            row_count = self.ui.DownloadList.rowCount()  # 当前行数
            self.ui.DownloadList.insertRow((int(row_count)))  # 当前行后插入

            self.download_queue.put((self.local_dir, file_name, row_count))
            # 插入任务序号
            download_no = QTableWidgetItem(str(self.download_no))
            self.ui.DownloadList.setItem(row_count, 0, download_no)

            # 插入文件名
            file_name_qt = QTableWidgetItem(file_name)
            self.ui.DownloadList.setItem(row_count, 1, file_name_qt)
            self.ui.DfileName.setText(str(self.download_no)+'.'+file_name)

            self.download_no += 1

            # 插入开始时间
            start_time = QTableWidgetItem(time.asctime())
            self.ui.DownloadList.setItem(row_count, 3, start_time)
            # 插入文件大小
            file_size = self.ftpuser.get_size_format(self.ftpserver.size(file_name))
            file_size = QTableWidgetItem(file_size)
            self.ui.DownloadList.setItem(row_count, 2, file_size)

            if self.download_thread is None or not self.download_thread.is_alive():
                self.download_thread = threading.Thread(target=lambda: self._download())
                self.download_thread.setDaemon(True)
                self.download_thread.start()
            else:
                pass
        else:
            QMessageBox.warning(self.ui, 'warning', '请先选择保存位置！')
            pass

    def download_resume(self):
        assert self.download_closing_event.is_set()
        self.download_closing_event.clear()
        assert self.download_thread is not None
        assert not self.download_thread.is_alive()
        self.download_thread = threading.Thread(target=lambda: self._download())
        self.download_thread.setDaemon(True)
        self.download_thread.start()

    def _download(self):
        # 远程目录自动切换，不需要再在本地文件名前加上远程目录
        while not self.download_queue.empty():
            local_dir, file_name, row_count = self.download_queue.queue[0]
            assert local_dir is not None
            assert file_name is not None
            remote_path = file_name
            local_path = os.path.join(local_dir, file_name)

            target_size = self.ftpserver.size(remote_path)  # bytes
            old_size = 0.0
            cur_size = 0.0

            self.target_download_size += target_size
            thread = threading.Thread(
                target=lambda: self.ftpuser.download_file(self.ftpserver, remote_path, local_path))
            thread.setDaemon(True)
            thread.start()

            # 下载中
            while thread.is_alive():
                if os.path.exists(local_path):
                    cur_size = os.path.getsize(local_path)
                    increment = cur_size - old_size
                    #  log = f'cur: {cur_size}, old: {old_size}, incre: {increment}'
                    # print(log) # debug use
                    self.cur_download_size += increment
                    old_size = cur_size
                    try:
                        pv_download = int(100 * (self.cur_download_size / self.target_download_size))
                    except ZeroDivisionError:
                        pv_download = 100
                    self.download_progressChanged.update_progress(pv_download)  # 由于是进程之间，所以需要信号槽
                    if cur_size == target_size:
                        end_time = QTableWidgetItem(time.asctime())

            if self.download_closing_event.is_set():
                break

            self.download_queue.get()   # 从队列中删除

            print(f'{file_name}已下载完成！')

            # 下载完成，该任务的target_size = 0
            self.target_download_size = 0
            self.cur_download_size = 0

            # 插入结束时间
            self.ui.DownloadList.setItem(row_count, 4, end_time)

    def upload_callback(self, buf):
        # this function is called on each block of data after it is sent.
        # By default, block size is 1024, namely 1KB, as configurated in user.py.
        self.cur_upload_count += 1
        try:
            pv_upload = int(math.ceil(100 * (self.cur_upload_count / self.target_upload_count)))
        except ZeroDivisionError:
            pv_upload = 100
        self.upload_progressChanged.update_progress(pv_upload)

    def upload(self):
        if self.local_file:
            # 在传输列表中插入一行
            row_count = self.ui.UploadList.rowCount()  # 当前行数
            self.ui.UploadList.insertRow(int(row_count))  # 当前行后插入

            file_name = os.path.split(self.local_file)[1]

            self.upload_queue.put((self.local_file, file_name, row_count))

            # 插入任务序号
            upload_no = QTableWidgetItem(str(self.upload_no))
            self.ui.UploadList.setItem(row_count, 0, upload_no)

            # 插入文件名
            file_name_qt = QTableWidgetItem(file_name)
            self.ui.UploadList.setItem(row_count, 1, file_name_qt)
            self.ui.UfileName.setText(str(self.upload_no)+'.'+file_name)

            self.upload_no += 1

            # 插入开始时间
            start_time = QTableWidgetItem(time.asctime())
            self.ui.UploadList.setItem(row_count, 3, start_time)

            target_size = self.ftpuser.get_size_format(os.path.getsize(self.local_file))
            target_size = QTableWidgetItem(target_size)
            self.ui.UploadList.setItem(row_count, 2, target_size)

            if self.upload_thread is None or not self.upload_thread.is_alive():
                self.upload_thread = threading.Thread(target=lambda: self._upload())
                self.upload_thread.setDaemon(True)
                self.upload_thread.start()
            else:
                pass
        else:
            QMessageBox.warning(self.ui, 'warning', '请先选择上传的文件！')
            pass

    def upload_resume(self):
        assert self.upload_closing_event.is_set()
        self.upload_closing_event.clear()
        assert self.upload_thread is not None
        assert not self.upload_thread.is_alive()
        self.upload_thread = threading.Thread(target=lambda: self._upload())
        self.upload_thread.setDaemon(True)
        self.upload_thread.start()

    def _upload(self):
        # NOTE: 已经transWin界面加入到主窗口，调用时由self.trans变为self.ui
        # 远程目录自动切换，不需要再在本地文件名前加上远程目录
        while not self.upload_queue.empty():
            local_path, file_name, row_count = self.upload_queue.queue[0]
            assert os.path.exists(local_path)  # 本地文件路径

            remote_path = file_name

            # 文件大小
            target_count = max((os.path.getsize(local_path)) // 1024, 1)  # 传输块数（最少是1）
            self.target_upload_count += target_count

            thread = threading.Thread(target=lambda: self.ftpuser.upload_file(self.ftpserver, local_path, remote_path,
                                                                              callback=self.upload_callback))
            thread.setDaemon(True)
            thread.start()
            thread.join()

            if self.upload_closing_event.is_set():  # 终止上传
                break

            self.upload_queue.get()  # 从队列中删除
            end_time = QTableWidgetItem(time.asctime())
            print('removing {} from upload queue'.format(file_name))

            self.ui.UploadList.setItem(row_count, 4, end_time)
            self.refresh_dir()
            # 上传完成，任务的upload_count清零
            self.target_upload_count = 0
            self.cur_upload_count = 0

    def file_name(self, Qmodelidx):
        tm_path = self.modelt.filePath(Qmodelidx)
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
        rowcount = self.loginWin.sessionTbl.rowCount()
        if rowcount == 0:
            QMessageBox.warning(self.ui, 'warning', '请建立连接！')
        else:
            user, port, host, password = self.loginWin.get_selected_row()

            self.ui.nameEdit.setText(user)
            self.ui.portEdit.setText(port)
            self.ui.domainEdit.setText(host)
            self.ui.pwEdit.setText(password)
            self.loginWin.close()


    def connect_server(self):

        # 禁用connect button
        self.ui.connectBtn.setDisabled(True)

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

            # 启用disconnect button
            self.ui.disconnectBtn.setDisabled(False)
            self.remote_dir = self.ftpserver.pwd()
        except Exception as e:
            self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 0, 0, 200);")
            self.ui.serverLbl.setText('远程目录列表（连接失败！）：')
            # traceback.print_exc() # debug use
            self.exception = str(e)
            self.msgthread.start()
            # 启用connect button
            self.ui.connectBtn.setDisabled(False)

    def disconnect_server(self):
        self.ui.disconnectBtn.setDisabled(True)
        self.ui.serverLbl.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(128, 128, 128, 200);")
        self.ui.serverLbl.setText('远程目录列表（未连接）：')
        self.ftpserver.quit()
        self.ftpserver = None
        self.remote_dir = None

        # 禁用上传下载按钮
        self.ui.ulButton.setDisabled(True)
        self.ui.dButton.setDisabled(True)
        # 清空远程目录
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.clearContents()

        self.ui.connectBtn.setDisabled(False)

    def change_dir(self):
        row = self.ui.tableWidget.currentRow()
        target_type = self.ui.tableWidget.item(row, 2).text()
        target_dir = self.ui.tableWidget.item(row, 0).text()
        cur_dir = self.ftpserver.pwd()

        if target_type == 'file':
            return
        # 返回上一级目录
        elif row == 0 and target_dir == '..' and cur_dir != '/':
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

            self.ui.tableWidget.setRowCount(1)
            self.ui.tableWidget.clearContents()
            for col, text in enumerate(['..', ' ', ' ', ' ', ' ']):
                self.ui.tableWidget.setItem(0, col, QTableWidgetItem(text))

        else:
            self.remote_dir = self.ftpserver.pwd()
            return

        # 显示当前目录的文件并贴上图标
        self.refresh_dir()
        self.remote_dir = self.ftpserver.pwd()[1:]

    def refresh_dir(self):
        # 刷新当前目录
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

    def file_selected(self):
        row = self.ui.tableWidget.currentRow()
        target_type = self.ui.tableWidget.item(row, 2).text()
        if target_type != 'file' or self.local_file is not None:  # 选择的不是文件或者没有选中本地目录
            self.ui.dButton.setEnabled(False)  # 下载按键禁止
        else:
            self.ui.dButton.setEnabled(True)  # 下载按键允许
        return

    '''
       因为存在队列
      上传和下载列表中的删除：只能删除已完成的任务
      上传下载列表中的暂停：只能暂停当前的任务
       上传下载列表中的继续：只能继续当前的任务
    '''
    def upload_selected(self):
        selected_row = self.ui.UploadList.selectedItems()[0].row()
        self.ui.DeleteUploadBtn.setEnabled(True)
        if self.ui.ContinueUploadBtn.isEnabled():
            pass
        else:
            if self.ui.UploadList.item(selected_row, 4) is None:  # 未上传完毕
                if self.ui.UploadList.item(selected_row, 0).text() == self.ui.UfileName.text().split('.')[0]: # 如果当前选中的文件正在上传
                    self.ui.PauseUploadBtn.setEnabled(True)
                    self.ui.ContinueUploadBtn.setEnabled(False)
                else:
                    self.ui.PauseUploadBtn.setEnabled(False)
                    self.ui.ContinueUploadBtn.setEnabled(False)
            else:
                self.ui.PauseUploadBtn.setEnabled(False)
                self.ui.ContinueUploadBtn.setEnabled(False)

    def delete_upload(self):
        try:
            selected_row = self.ui.UploadList.selectedItems()[0].row()
        except IndexError:
            self.ui.DeleteUploadBtn.setEnabled(False)
            QMessageBox.warning(self.ui, 'warning', '当前已无上传任务！')
            return
        if self.ui.UploadList.item(selected_row, 4) is None: # 未上传完毕
            if self.ui.PauseUploadBtn.isEnabled():  # 当前正在上传，但是要删除
                self.pause_upload() # 暂停上传然后删除
            else:
                pass
        else:
            pass
        self.ui.UploadList.removeRow(selected_row)
        self.ui.PauseUploadBtn.setEnabled(False)
        self.ui.ContinueUploadBtn.setEnabled(False)

    def pause_upload(self):
        self.ftpserver.abort()
        self.upload_closing_event.set()
        self.ui.PauseUploadBtn.setEnabled(False)
        self.upload_thread.join()
        self.ui.ContinueUploadBtn.setEnabled(True)

    def continue_upload(self):
        self.ui.PauseUploadBtn.setEnabled(True)
        self.ui.ContinueUploadBtn.setEnabled(False)
        self.upload_resume()

    def download_selected(self):
        selected_row = self.ui.DownloadList.selectedItems()[0].row()
        self.ui.DeleteDownloadBtn.setEnabled(True)
        if self.ui.ContinueDownloadBtn.isEnabled():  # 当前处于暂停状态
            pass
        else:
            if self.ui.DownloadList.item(selected_row, 4) is None:
                if self.ui.DownloadList.item(selected_row, 0).text() == self.ui.DfileName.text().split('.')[0]:
                    self.ui.PauseDownloadBtn.setEnabled(True)
                    self.ui.ContinueDownloadBtn.setEnabled(False)
                else:
                    self.ui.PauseDownloadBtn.setEnabled(False)
                    self.ui.ContinueDownloadBtn.setEnabled(False)
            else:
                self.ui.PauseDownloadBtn.setEnabled(False)
                self.ui.ContinueDownloadBtn.setEnabled(False)

    def delete_download(self):
        try:
            selected_row = self.ui.DownloadList.selectedItems()[0].row()
        except IndexError:
            self.ui.DeleteDownloadBtn.setEnabled(False)
            QMessageBox.warning(self.ui, 'warning', '当前已无下载任务！')
            return
        if self.ui.DownloadList.item(selected_row, 4) is None:  # 未下载完毕
            if self.ui.PauseDownloadBtn.isEnabled():
                self.pause_download()
            else:
                pass
        else:
            pass
        self.ui.DownloadList.removeRow(selected_row)
        self.ui.PauseDownloadBtn.setEnabled(False)
        self.ui.ContinueDownloadBtn.setEnabled(False)

    def pause_download(self):
        self.ftpserver.abort()
        self.download_closing_event.set()
        self.ui.PauseDownloadBtn.setEnabled(False)
        self.download_thread.join()
        self.ui.ContinueDownloadBtn.setEnabled(True)

    def continue_download(self):
        self.ui.PauseDownloadBtn.setEnabled(True)
        self.ui.ContinueDownloadBtn.setEnabled(False)
        self.download_resume()


    def NewSessionList(self):
        self.NewSession.exec_()


    def AddData(self):
        name = self.NewSession.Name.text()
        username = self.NewSession.User.text()
        password = self.NewSession.Host.text()
        host = self.NewSession.Host_2.text()
        port = self.NewSession.Port.text()

        if len(name) == 0 or len(username) == 0 or len(password) ==0 or len(host) ==0 or len(port) == 0:
            QMessageBox.warning(self.ui, 'warning', '请补全连接！')

        else:
            ip = host.split('.')
            if len(ip) == 4 and ip[0].isdigit() and int(ip[0]) in range(0,255) and ip[1].isdigit() and int(ip[1]) in range(0,255) and ip[2].isdigit() and int(ip[2]) in range(0,255) and ip[3].isdigit() and int(ip[3]) in range(0,255):
                dict = {"name": "whuftp", "username": username, "protocol": "FTP", "port": port, "domain": host, "password": password}
                with open('cache/config_client.json', mode='r', encoding='utf-8') as f:
                    data = f.read()
                list= []
                if not len(data)==0:
                    list = json.loads(data)
                list.append(dict)
                print(list)
                with open('cache/config_client.json', mode='w', encoding='utf-8') as f:
                    json.dump(list, f)      #将数据保存到json里
                currentRowCount = self.loginWin.sessionTbl.rowCount()
                self.loginWin.sessionTbl.insertRow(currentRowCount) #将页面的数据插入到login中
                self.loginWin.sessionTbl.setItem(currentRowCount, 0, QTableWidgetItem(name))
                self.loginWin.sessionTbl.setItem(currentRowCount, 1, QTableWidgetItem(username))
                self.loginWin.sessionTbl.setItem(currentRowCount, 2, QTableWidgetItem("FTP"))
                self.loginWin.sessionTbl.setItem(currentRowCount, 3, QTableWidgetItem(port))
                self.loginWin.sessionTbl.setItem(currentRowCount, 4, QTableWidgetItem(host))
                self.loginWin.sessionTbl.setItem(currentRowCount, 5, QTableWidgetItem(password))
                self.NewSession.Name.clear() #清空之前的输入
                self.NewSession.User.clear()
                self.NewSession.Port.clear()
                self.NewSession.Host.clear()
                self.NewSession.Host_2.clear()
                self.NewSession.close()
            else:
                QMessageBox.warning(self.ui, 'warning', '主机格式不正确！')


    def deleteOpetion(self):
        self.loginWin.delBtn.setEnabled(True)


    def deleteRow(self):
        row = self.loginWin.sessionTbl.currentRow()
        self.loginWin.sessionTbl.removeRow(row)
        self.loginWin.delBtn.setEnabled(False)
        with open('cache/config_client.json', mode='r', encoding='utf-8') as f:
            data = f.read()
        list = []
        if not len(data) == 0:
            list = json.loads(data)
            del list[row]
        with open('cache/config_client.json', mode='w', encoding='utf-8') as f:
            json.dump(list, f)


app = QApplication([])
stats = Client()
stats.loginWin.exec()
stats.ui.show()
sys.exit(app.exec())  # 安全结束
