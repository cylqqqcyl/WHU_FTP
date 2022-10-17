from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QAbstractItemView, QFileSystemModel

# from PySide2.QtUiTools import QUiLoader
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QFile
from PyQt5.QtCore import Qt
import PyQt5
import os

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile("FTP.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("FTP.ui")
        # self.ui.button.clicked.connect(self.handleCalc)
        self.ui.eButton.clicked.connect(self.exit)
        self.ui.ulButton.clicked.connect(self.upload)
        self.ui.upButton.setEnabled(False)
        self.ui.dButton.setEnabled(False)
        self.ui.eButton.setEnabled(False)
        self.ui.qButton.setEnabled(False)

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

        self.namelist = ["红楼梦", "耶路撒冷", "原神", "蒂法"]
        self.ui.listmodel = PyQt5.QtCore.QStringListModel()
        self.ui.listmodel.setStringList(self.namelist)
        # self.ui.listView.setModel(self.ui.listmodel)
        # self.ui.listView.setEditTriggers(QAbstractItemView.AnyKeyPressed
        #                                  | QAbstractItemView.DoubleClicked)

    def upload(self):
        QMessageBox.about(
            self.ui, '统计结果',
            f'''域名：\n{self.ui.domainEdit.text()}\n端口：\n{self.ui.portEdit.text()}\n用户名：\n{self.ui.nameEdit.text()}\n口令：\n{self.ui.pwEdit.text()}'''
        )

    def file_name(self, Qmodelidx):
        print(self.modelt.filePath(Qmodelidx))  #输出文件的地址。
        print(self.modelt.fileName(Qmodelidx))  #输出文件名

    def exit(self):
        return 0

    def handleCalc(self):
        info = self.ui.textEdit.toPlainText()

        self.ui.textEdit.clear()  #
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')

            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(
            self.ui, '统计结果', f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}''')


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec()