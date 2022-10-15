# 该脚本程序是运行在windows上的ftp，运行前需要安装pyftpdlib模块， pip3 install pyftpdlib
# 修改filesystems.py文件，将503 行的 "utf-8"修改成"gbk"（windows支持的gbk类型的bytes）即 yield line.encode('gbk', self.cmd_channel.unicode_errors
# 修改 handlers.py 文件，将1413行的"utf-8"修改成"gbk"（windows支持的gbk类型的bytes）即 return bytes.decode('gbk', self.unicode_errors)

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import LogFormatter
import logging

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

# 3.添加用户权限和路径，括号内的参数是(用户名、密码、用户目录、权限)，可以为不同的用户添加不同的目录和权限
authorizer.add_user('user', '123456', "d:/", perm="elradfmw")

# 4.添加匿名用户，只需要路径
authorizer.add_anonymous("d:/")

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

