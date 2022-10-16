from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import LogFormatter
import logging
import os
import argparse
import threading
from utils import get_config

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


class Admin():
    def __init__(self, config):
        self.root_dir = config.root_dir
        self.public_dir = config.public_dir
        self.private_dir = config.private_dir
        self.anonymous_dir = config.anonymous_dir
        self.log_dir = config.log_dir
        self.read_limit = config.read_limit
        self.write_limit = config.write_limit
        self.max_cons = config.max_cons
        self.max_cons_per_ip = config.max_cons_per_ip

        self._create_admin()
        self._create_logger()

    def _create_logger(self, filename='admin.log'):
        # TODO: 日志似乎没有写到文件里，可能要传到handler?
        logger = logging.getLogger('FTP-LOG')
        logger.setLevel(logging.DEBUG)

        cs = logging.StreamHandler()
        cs.setLevel(logging.INFO)

        root_dir = __file__.strip('src\\admin.py')
        log_path = os.path.join(root_dir, f'{self.log_dir}/{filename}')
        fs = logging.FileHandler(filename=log_path, mode='a', encoding='utf-8')
        fs.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s : %(message)s')

        cs.setFormatter(formatter)
        fs.setFormatter(formatter)

        logger.addHandler(cs)
        logger.addHandler(fs)

        self.logger = logger

    def _create_admin(self):
        authorizer = DummyAuthorizer()

        handler = FTPHandler
        handler.authorizer = authorizer
        handler.passive_ports = range(2000, 20033) # hardcoded
        dtp_handler = ThrottledDTPHandler
        dtp_handler.read_limit = self.read_limit
        dtp_handler.write_limit = self.write_limit
        handler.dtp_handler = dtp_handler

        server = FTPServer(('0.0.0.0', 21), handler)
        server.max_cons = self.max_cons
        server.max_cons_per_ip = self.max_cons_per_ip

        self.authorizer = authorizer
        self.handler = handler
        self.server = server

    def add_user(self, username='', password=''):
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
        root_dir = __file__.strip('src\\admin.py')
        if username == '':
            anonymous_dir = os.path.join(root_dir, self.anonymous_dir)
            self.authorizer.add_anonymous(anonymous_dir)
            self.logger.info('Add an anonymous user!')
        else:
            home_dir = os.path.join(root_dir, f'{self.private_dir}/{username}')
            # TODO: 赋予用户不同的权限
            perm = 'elradfmw'
            if not os.path.exists(home_dir):
                os.makedirs(home_dir)
            try:
                self.authorizer.add_user(username, password, home_dir, perm)
                self.logger.info(f'Add {username}!')
            except ValueError:
                self.logger.error('user %r already exists' % username)

    def start_serving(self):
        print('Start serving...')
        self.server.serve_forever()

    def end_serving(self):
        print('End serving...')
        self.server.close_all()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--config', type=str, required=True, help='configuration file path')
    #
    # args = parser.parse_args()
    #
    # config = get_config(args.config)
    config = get_config('../configs/config_admin.json')

    admin = Admin(config)
    # TODO: 在不关闭服务的情况下加入新用户
    thread = threading.Thread(target=admin.start_serving)
    thread.start()
    admin.add_user('user-1', '123456')
    thread.join()



