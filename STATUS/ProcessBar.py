from ftplib import FTP
import sys, getpass, os.path

import tkinter as Tkinter
# from mttkinter import mtTkinter as Tkinter
# Tkinter.CallWrapper=TkErrorCatcher
from tkinter import ttk
# from mttkinter.mtTkinter import ttk
import time
import threading

# HOST = '192.168.1.8'  # ftp地址
# PORT = 21
TIMEOUT = 30  # 超时时间
# USER_NAME = 'linxinfa'  # ftp账号
# PASS_WORD = '123456'  # ftp密码
# BLOCK_SIZE = 8192  # 每帧上传的数据大小

file_name = ''  # 上传的文件名，ui部分显示用
file_size = 0  # 文件总大小，计算进度时用
upload_size = 0  # 已上传的数据大小，计算进度时用
bar = None  # 进度条对象


class PopupProgressBar:
    def __init__(self, title):
        self.title = title
        self.root = None
        self.bar = None
        self.bar_lock = threading.Lock()
        self.thread = None
        self.thread_upd = None
        self.is_stop_thread_upd = False
        self.value = 0
        self.text = ""
        self.labelText = None  # Tkinter.StringVar()
        if not self.title:
            self.title = "PopupProgressBar"

    def start(self):
        print("start")
        self.thread = threading.Thread(target=PopupProgressBar._run_, args=(self,))
        self.thread.setDaemon(False)
        self.thread.start()

    def _run_(self):
        root = Tkinter.Tk()
        root.geometry('500x80+500+200')
        root.title(self.title)

        self.labelText = Tkinter.StringVar()
        self.labelText.set(self.text)

        ft = ttk.Frame()
        ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

        label1 = Tkinter.Label(ft, textvariable=self.labelText)
        label1.pack(fill=Tkinter.X, side=Tkinter.TOP)

        pb_hD = ttk.Progressbar(ft, orient='horizontal', length=300, mode='determinate')
        pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

        self.root = root
        self.bar = pb_hD
        self.bar["maximum"] = 100
        self.bar["value"] = 0

        self.thread_upd = threading.Thread(target=PopupProgressBar._update_, args=(self,))
        self.thread_upd.setDaemon(False)
        self.thread_upd.start()

        self.root.mainloop()

    def _update_(self):
        while not self.is_stop_thread_upd:
            self.update_data(self.value)
            self.labelText.set(self.text)
            time.sleep(0.01)
        print("hhhhhhhhhhhhhhhhhhhhhhhh")

    def update_data(self, value):
        if not self.bar:
            return
        if self.bar_lock.acquire():
            self.bar["value"] = value
            self.bar_lock.release()

    def stop(self):
        if self.thread_upd:
            self.is_stop_thread_upd = True
            print("okkkkkkkkkkkkkkkkkkkkkk")

        self.thread_upd.join()
        print("joinjoinjoinjoinjoinjoinjoin")
        self.root.quit()


# localfile 本机要上传的文件与路径
# remotepath ftp服务器的路径 (ftp://192.168.1.8/xxx)
def upload_file(cur_ftp,localpath, remotepath):
    global file_size
    global bar
    bar = PopupProgressBar('ftp upload file: ' + localpath)
    bar.start()

    bufsize = 1024
    fp = open(localpath, 'rb')
    file_size = os.path.getsize(localpath)
    cur_ftp.storbinary('STOR ' + remotepath, fp, bufsize, callback=upload_file_cb)
    cur_ftp.set_debuglevel(0)
    fp.close()


    # cur_ftp = FTP()
    # cur_ftp.connect(HOST, PORT, TIMEOUT)  # 连接ftp服务器
    # cur_ftp.login(USER_NAME, PASS_WORD)  # 登录ftp服务器
    # cur_ftp.cwd(remotepath)  # 设置ftp服务器端的路径
    # cur_file = open(localfile, 'rb')  # 打开本地文件
    # file_size = os.path.getsize(localfile)
    # cur_ftp.storbinary('STOR %s' % os.path.basename(localfile), cur_file, blocksize=BLOCK_SIZE,
    #                    callback=upload_file_cb)  # 上传文件到ftp服务器
    # print('upload_file done')
    # cur_file.close()  # 关闭本地文件
    # cur_ftp.quit()  # 退出


def upload_file_cb(block):
    global upload_size
    upload_size = upload_size + len(block)
    bar.value = upload_size / file_size * 100
    bar.text = format(upload_size / file_size * 100, '.2f') + '%'
    if bar.value >= 100:
        time.sleep(0.2)
        bar.stop()


download_size = 0
fp = None


# ftp下载
def download_ftp(ftp, localpath, remotepath):
    global file_size
    global bar
    global fp
    bar = PopupProgressBar('ftp download file: ' + remotepath)
    bar.start()
    # 从ftp下载文件
    bufsize = 1024
    fp = open(localpath, 'wb')
    # fp = open(localpath, 'r')
    file_size = ftp.size(remotepath)
    ftp.retrbinary('RETR ' + remotepath,blocksize= bufsize, callback=download_file_cb)
    ftp.set_debuglevel(0)
    fp.close()



    # cur_ftp = FTP()
    # cur_ftp.connect(HOST, PORT, TIMEOUT)  # 连接ftp服务器
    # cur_ftp.login(USER_NAME, PASS_WORD)  # 登录ftp服务器
    # cur_ftp.cwd(remotepath)  # 设置ftp服务器端的路径
    # file_size = cur_ftp.size(filename)
    # fwriter = open(product_name, 'wb')  # 以写模式在本地打开文件，如果不存在，则会创建该文件
    # # ftp下载，这个函数是阻塞的，会通过callback回调
    # ftp.retrbinary("RETR %s" % filename, blocksize=bufsize, callback=download_file_cb)
    # fwriter.close()  # 关闭文件
    # cur_ftp.close()


# ftp下载回调
def download_file_cb(block):
    global download_size
    global fp
    # 写文件到本地
    fp.write(block)
    # 显示下载进度
    download_size = download_size + len(block)
    bar.value = download_size / file_size * 100
    bar.text = format(download_size / file_size * 100, '.2f') + '%'
    if bar.value >= 100:
        time.sleep(0.2)
        bar.stop()

i=0

def f1():
    global i
    global ct
    i+=1
    print(i)
    if i<2:
        ct= Tkinter.Tk()
        t2 = threading.Thread(target=f2)
        t2.start()
        ct.mainloop()
    else:
        time.sleep(2)
        ct.quit()
        ct=Tkinter.Tk()
        ct.mainloop()
        print("quit")

def f2():
    time.sleep(5)
    print("sdfdsf")

if '__main__' == __name__:

    t1=threading.Thread(target=f1)
    t1.start()
    # t1.join()
    # time.sleep(2)
    t2=threading.Thread(target=f1)

    t2.start()
    # ct = Tkinter.Tk()
    # ct.mainloop()
    # upload_file('./test.apk', '/')
    # print('ok')