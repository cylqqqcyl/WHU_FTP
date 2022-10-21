from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import LogFormatter
import logging
import sqlite3
import os

class MyHandler(FTPHandler): # customized event handler

    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)


cur_dir = __file__.strip('src\\admin.py')
user_dir = cur_dir+"\\user_dir"

# 1.记录日志输出到文件和终端
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


# 2.实例化虚拟用户，这是FTP的首要条件
authorizer = DummyAuthorizer()

def load_user(authorizer): # 加载用户参数
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('select * from user')
    user_info = cursor.fetchall()
    for username, password in user_info:
        authorizer.add_user(username, password, user_dir, perm="elradfmw")
    cursor.close()
    conn.close()

def register(uname,password,authorizer): # 注册函数
    uname = str(uname)
    password = str(password)
    assert len(uname)<21
    assert len(password)<21
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute('insert into user(username,password) values("{}","{}")'.format(uname,password))
    except Exception as e:
        print(e)
    else:
        authorizer.add_user(uname, password, user_dir, perm="elradfmw")
    cursor.close()
    conn.commit()
    conn.close()
# 3.添加用户权限和路径，括号内的参数是(用户名、密码、用户目录、权限)，可以为不同的用户添加不同的目录和权限

'''
1、读权限：
e ：改变文件目录
l ：列出文件
r ：从服务器接收文件
2、写权限
a ：文件上传
d ：删除文件
f ：文件重命名
m ：创建文件
w ：写权限
M：文件传输模式（通过FTP设置文件权限）

'''
load_user(authorizer)
# 4.添加匿名用户，只需要路径
authorizer.add_anonymous(user_dir)

# 5.初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

# 6.添加被动端口范围
handler.passive_ports = range(2000,20033)

# 7.上传下载的速度设置
dtp_handler = ThrottledDTPHandler
dtp_handler.read_limit = 300 * 1024          # 300 kb/s
dtp_handler.write_limit = 300 * 1024         # 300 kb/s
handler.dtp_handler = dtp_handler

# 8.监听ip和端口 ， linux里需要root用户才能使用21端口
server = FTPServer(('0.0.0.0', 21), handler)

# 9.最大连接数
server.max_cons = 150
server.max_cons_per_ip = 15

# 10.开始服务，自带打印日志信息
server.serve_forever()

