from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QAbstractItemView, QFileSystemModel

# from PySide2.QtUiTools import QUiLoader
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QFile
from PyQt5.QtCore import Qt
import PyQt5
import os
import sys
from src import user

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ftpserver = None  # 所连接到的服务器实例
        qfile_stats = QFile("FTP.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("FTP.ui")
        # self.ui.button.clicked.connect(self.handleCalc)
        self.ui.eButton.clicked.connect(self.exit)  # 退出按键操作
        self.ui.ulButton.clicked.connect(self.upload)  # 上传按键操作
        self.ui.upButton.setEnabled(False)  # 返回上层按键操作
        self.ui.dButton.setEnabled(False)  # 下载按键操作
        self.ui.qButton.clicked.connect(self.connect_server)  # 查询按键操作

        #设置背景图片
        image0 = QtGui.QPixmap('megumi1.jpg')
        image0=image0.scaled(self.ui.width(), self.ui.height()/1.5, \
                         Qt.KeepAspectRatioByExpanding, \
                         Qt.SmoothTransformation)
        palette1 = QtGui.QPalette()
        palette1.setBrush(self.ui.backgroundRole(), QtGui.QBrush(image0))
        self.ui.setPalette(palette1)
        self.ui.setAutoFillBackground(True)

        path = 'D:'
        self.modelt = QFileSystemModel()
        self.modelt.setRootPath(path)

        #为控件添加模式。
        self.ui.treeView.setModel(self.modelt)
        self.ui.treeView.setRootIndex(self.modelt.index(path))  #只显示设置的那个文件路径。
        self.ui.treeView.doubleClicked.connect(self.file_name)  #双击文件打开

        self.modelt2 = QFileSystemModel()
        ####################################################
        self.modelt2.setRootPath(path)  ##<-这里后续修改Path值#
        ####################################################

        self.ui.treeView_2.setModel(self.modelt2)
        self.ui.treeView_2.setRootIndex(self.modelt2.index(path))  # 只显示设置的那个文件路径。
        self.ui.treeView_2.doubleClicked.connect(self.file_name)  # 双击文件打开





    def upload(self):
        QMessageBox.about(
            self.ui, '登入信息',
            f'''域名：\n{self.ui.domainEdit.text()}\n端口：\n{self.ui.portEdit.text()}\n用户名：\n{self.ui.nameEdit.text()}\n口令：\n{self.ui.pwEdit.text()}'''
        )

    def file_name(self, Qmodelidx):
        print(self.modelt.filePath(Qmodelidx))  #输出文件的地址。
        print(self.modelt.fileName(Qmodelidx))  #输出文件名

    def exit(self):
        sys.exit(app.exec())  # 更正退出

    def connect_server(self):
        try:
            self.ftpserver=user.ftpconnect(
                host=self.ui.domainEdit.text(),
                username=self.ui.nameEdit.text(),
                password=self.ui.pwEdit.text(),
                port=int(self.ui.portEdit.text()))
        except Exception as e:
            QMessageBox.warning(self.ui, '警告',f'''{e}''')

app = QApplication([])
stats = Stats()
stats.ui.show()
sys.exit(app.exec()) # 安全结束