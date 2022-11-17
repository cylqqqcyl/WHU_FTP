from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import LogFormatter
import logging
import sqlite3
import sys
import os
import os.path
from src.FTP_user import FTP_user as FTP
import ftplib
import datetime
import argparse
from datetime import datetime


class WHUFTPServer:
    def __init__(self,
                 address, port,
                 read_limit, write_limit,
                 max_cons, max_cons_per_ip,
                 root_dir, log_path, db_path,
                 ):

        self.address = address  # 服务器地址
        self.port = port  # 端口
        self.read_limit = read_limit  # 读文件限速
        self.write_limit = write_limit  # 写文件限速
        self.max_cons = max_cons  # 最大连接数
        self.max_cons_per_ip = max_cons_per_ip  # 每个IP最大连接数
        self.root_dir = root_dir  # 服务器根目录
        self.log_path = log_path  # 日志路径
        self.db_path = db_path  # 数据库路径

    def apply_server(self):
        self.authorizer = DummyAuthorizer()
        self.handler = FTPHandler  # handler，之后使用MyHandler
        self.handler.authorizer = self.authorizer
        self.handler.passive_ports = range(2000, 20033)  # TODO: hardcode?
        self.dtp_handler = ThrottledDTPHandler
        self.dtp_handler.read_limit = self.read_limit
        self.dtp_handler.write_limit = self.write_limit
        self.handler.dtp_handler = self.dtp_handler
        self.server = FTPServer((self.address, self.port), self.handler)

        self.server.max_cons = self.max_cons
        self.server.max_cons_per_ip = self.max_cons_per_ip

        self.load_user()

    def start_server(self):
        self.server.serve_forever()

    def close_server(self):
        self.server.close_all()

    def reset_server(self):
        self.authorizer = None
        self.handler = None
        self.dtp_handler = None
        self.server = None

    def load_user(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('select * from user')
        except sqlite3.OperationalError:
            cursor.execute('create table user(username char(20) primary key not null,password char(20))')  # 用户名为主键

        user_info = cursor.fetchall()
        for username, password in user_info:
            user_dir = os.path.join(self.root_dir, username)
            try:
                os.mkdir(user_dir)  # 对每个用户创建文件夹
            except FileExistsError:
                pass
            # 需要实现删除用户时，删除对应文件夹
            self.authorizer.add_user(username, password, user_dir, perm="elradfmw")
        cursor.close()
        conn.close()

    def register(self, uname, password):  # 注册函数
        uname = str(uname)
        password = str(password)
        assert len(uname) < 21
        assert len(password) < 21
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('insert into user(username,password) values("{}","{}")'.format(uname, password))
        except Exception as e:
            print(e)
        else:
            # 分配单独的home dir
            user_dir = os.path.join(self.root_dir, uname)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            self.authorizer.add_user(uname, password, user_dir, perm="elradfmw")
        cursor.close()
        conn.commit()
        conn.close()

    def del_user(self, uname):  # 删除用户函数
        uname = str(uname)
        assert len(uname) < 21
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('delete from user where username="{}"'.format(uname))
        except Exception as e:
            print(e)
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def get_logger():
        logger = logging.getLogger('FTP-LOG')
        logger.setLevel(logging.DEBUG)

        cs = logging.StreamHandler()
        cs.setLevel(logging.INFO)

        fs = logging.FileHandler(filename='test.log', mode='a', encoding='utf-8')
        fs.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s : %(message)s')

        cs.setFormatter(formatter)
        fs.setFormatter(formatter)

        logger.addHandler(cs)
        logger.addHandler(fs)

        return logger


class WHUFTPClient:
    def __init__(self,
                 username,
                 password,
                 host,
                 port=21):

        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def connect_server(self):
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(self.host, self.port)
        ftp.login(self.username, self.password)
        ftp.set_pasv(False)
        print(ftp.getwelcome())

        return ftp

    @staticmethod
    def upload_file(ftp, local_path, remote_path, callback=None):
        # 从本地上传文件到ftp
        buffer_size = 1024
        try:
            ftp.voidcmd('TYPE I')  # 设置为二进制模式
            uploaded_size = ftp.size(remote_path)  # 断点续传
        except ftplib.error_perm:  # 如果还没有开始上传，那么uploaded_size=0
            uploaded_size = 0
        fp = open(local_path, 'rb')
        fp.seek(uploaded_size)
        ftp.storbinary('STOR ' + remote_path, fp, buffer_size, rest=uploaded_size, callback=callback)
        fp.close()

    @staticmethod
    def download_file(ftp, remote_path, local_path, callback=None):
        # 从ftp下载文件
        buffer_size = 1024
        if os.path.exists(local_path):  # 防止续传覆盖
            fp = open(local_path, 'rb+')
        else:
            fp = open(local_path, 'wb')
        downloaded_size = os.path.getsize(local_path)  # 断点续传
        fp.seek(downloaded_size)
        ftp.retrbinary('RETR ' + remote_path, fp.write, buffer_size, rest=downloaded_size,callback=callback)
        ftp.set_debuglevel(0)
        fp.close()

    def get_server_files(self, ftp):
        """
          字典返回FTP服务器文件及目录
          返回值:
            key: 文件/目录名
            value: 文件类型('dir','file','block')
        """
        # noinspection PyBroadException
        try:
            mlsd_result = ftp.mlsd()
        except Exception as e:
            return None
        else:
            remote_files = []
            for file_data in mlsd_result:
                # extract returning data
                file_name, meta = file_data
                # i.e directory, file or link, etc
                file_type = meta.get("type")
                if file_type == "file":
                    # if it is a file, change type of transfer data to IMAGE/binary
                    ftp.voidcmd("TYPE I")
                    # get the file size in bytes
                    file_size = ftp.size(file_name)
                    # convert it to human-readable format (i.e in 'KB', 'MB', etc)
                    file_size = self.get_size_format(file_size)
                else:
                    # not a file, may be a directory or other types
                    file_size = ""
                # date of last modification of the file
                last_modified = self.get_datetime_format(meta.get("modify"))
                # print all
                file_data_list = [file_name, file_size, file_type, last_modified]
                remote_files.append(file_data_list)

        return remote_files

    @staticmethod
    def get_size_format(n, suffix="B"):
        # converts bytes to scaled format (e.g KB, MB, etc.)
        for unit in ["", "K", "M", "G", "T", "P"]:
            if n < 1024:
                return f"{n:.2f}{unit}{suffix}"
            n /= 1024

    @staticmethod
    def get_datetime_format(date_time):
        # convert to datetime object
        date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
        # convert to human-readable date time string
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
