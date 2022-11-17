import socket
import sys
from socket import _GLOBAL_DEFAULT_TIMEOUT

CRLF = '\r\n'


class Error(Exception): pass
class error_reply(Exception): pass
class error_perm(Exception): pass
class error_proto(Exception): pass
class error_temp(Exception): pass


class FTP_user:
    def __init__(self):
        self.host = ''
        self.port = 0
        self.source_address = None
        self.timeout = None
        self.encoding = 'utf-8'
        self.maxline = 8192
        self.debugging = 0
        self.passiveserver = True

    def connect(self, host='', port=0, timeout=-999, source_address=None):
        '''连接到服务器
         - host: 服务器的域名
         - port: 端口
         - timeout: 超时限制.
        '''
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        if self.timeout is not None and not self.timeout:
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        if source_address is not None:
            self.source_address = source_address
        sys.audit("ftp.connect", self, self.host, self.port)
        self.sock = socket.create_connection((self.host, self.port), self.timeout,
                                             source_address=self.source_address)
        self.af = self.sock.family
        self.file = self.sock.makefile('r', encoding=self.encoding)  # socket 的输出记录在file中
        self.welcome = self.getresp()
        return self.welcome

    def getwelcome(self):
        '''获取服务器的欢迎信息'''
        if self.debugging:
            print('*welcome*', self.welcome)
        return self.welcome

    def login(self, user='', passwd=''):
        '''登录，默认匿名.'''
        if not user:
            user = 'anonymous'
        if not passwd:
            passwd = ''
        if user == 'anonymous' and passwd in {'', '-'}:
            passwd = passwd + 'anonymous@'

        resp = self.sendcmd('USER ' + user)
        if resp[0] == '3':
            resp = self.sendcmd('PASS ' + passwd)
        if resp[0] != '2':
            raise Error(resp)
        return resp

    def set_pasv(self, val):
        '''采用主动或者被动的数据传输模式.
        False，采用 PORT 模式,
        True, 采用 PASV 命令.'''
        self.passiveserver = val

    def size(self, filename):
        '''获取文件大小.'''
        resp = self.sendcmd('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            return int(s)

    def sendcmd(self, cmd):
        '''发送命令并且返回答复'''
        self.putcmd(cmd)
        return self.getresp()

    def voidcmd(self, cmd):
        """发送一个指令，得到一个以'2'开头的答复."""
        self.putcmd(cmd)
        return self.voidresp()

    def putcmd(self, line):
        if self.debugging: print('*cmd*', line)
        self.putline(line)

    def putline(self, line):
        if '\r' in line or '\n' in line:
            raise ValueError('an illegal newline character should not be contained')
        sys.audit("ftp.sendcmd", self, line)
        line = line + CRLF
        if self.debugging > 1:
            print('*put*', line)
        self.sock.sendall(line.encode(self.encoding))

    def getresp(self):
        line = self.file.readline(self.maxline + 1)
        if len(line) > self.maxline:
            raise Error("got more than %d bytes" % self.maxline)
        # if self.debugging > 1:
        #     print('*get*', self.sanitize(line))
        if not line:
            raise EOFError
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        c = line[:1]
        if c in {'1', '2', '3'}:
            return line
        if c == '4':
            raise error_temp(line)
        if c == '5':
            raise error_perm(line)
        raise error_proto(line)

    def voidresp(self):
        """需要一个以 '2'开头的答复."""
        resp = self.getresp()
        if resp[:1] != '2':
            raise Error(resp)
        return resp

    def set_debuglevel(self, level):
        '''设定debug等级.
        0: 无输出（默认）
        1: 输出命令.
        2: 输出完整的字符串'''
        self.debugging = level

    def sendport(self, host, port):
        '''发送 PORT 指令.
        '''
        hbytes = host.split('.')
        pbytes = [repr(port//256), repr(port%256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.voidcmd(cmd)

    def sendeprt(self, host, port):
        '''发送 EPRT 指令'''
        af = 0
        if self.af == socket.AF_INET:
            af = 1
        if self.af == socket.AF_INET6:
            af = 2
        if af == 0:
            raise error_proto('unsupported address family')
        fields = ['', repr(af), host, repr(port), '']
        cmd = 'EPRT ' + '|'.join(fields)
        return self.voidcmd(cmd)

    def makeport(self):
        '''创建一个新的 socket 并且对其发送 PORT 指令.'''
        sock = socket.create_server(("", 0), family=self.af, backlog=1)
        port = sock.getsockname()[1] # Get proper port
        host = self.sock.getsockname()[0] # Get proper host
        if self.af == socket.AF_INET:
            resp = self.sendport(host, port)
        else:
            resp = self.sendeprt(host, port)
        if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(self.timeout)
        return sock

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        """以二进制模式上传文件.

        Args:
          cmd: STOR 命令.
          fp: 以 read(num_bytes) 方法打开的文件.
          blocksize: 块大小.  [default: 8192]
          callback: 回调.  [default: None]
          rest: 断点重传位置.  [default: None]

        Returns:
          回复.
        """
        self.voidcmd('TYPE I')
        with self.transfercmd(cmd, rest)[0] as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
        return self.voidresp()

    def transfercmd(self, cmd, rest=None):
        """发起一个数据传输命令.
        采用主动模式
        """
        size = None
        with self.makeport() as sock:
            if rest is not None:
                self.sendcmd("REST %s" % rest)
            resp = self.sendcmd(cmd)
            if resp[0] == '2':
                resp = self.getresp()
            if resp[0] != '1':
                raise error_reply(resp)
            conn, sockaddr = sock.accept()
            if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                conn.settimeout(self.timeout)
        if resp[:3] == '150':
            size = parse150(resp)
        return conn, size

    def retrbinary(self, cmd, callback, blocksize=8192, rest=None):
        """以二进制模式下载文件.

        Args:
          cmd:A RETR 命令.
          callback: 回调
          blocksize: 块大小
          rest: 断点重传位置.

        Returns:
          回复.
        """
        self.voidcmd('TYPE I')
        with self.transfercmd(cmd, rest) as conn:
            while 1:
                data = conn.recv(blocksize)
                if not data:
                    break
                callback(data)

        return self.voidresp()

    def retrlines(self, cmd, callback = None):
        """采用文本模式下载文件.

        Args:
          cmd:  RETR, LIST或 NLST 命令.
          callback: 回调函数

        Returns:
          回复
        """
        if callback is None:
            callback = print_line
        resp = self.sendcmd('TYPE A')
        with self.transfercmd(cmd)[0] as conn, \
                 conn.makefile('r', encoding=self.encoding) as fp:
            while 1:
                line = fp.readline(self.maxline + 1)
                if len(line) > self.maxline:
                    raise Error("got more than %d bytes" % self.maxline)
                if self.debugging > 2:
                    print('*retr*', repr(line))
                if not line:
                    break
                if line[-2:] == CRLF:
                    line = line[:-2]
                elif line[-1:] == '\n':
                    line = line[:-1]
                callback(line)
        return self.voidresp()

    def mlsd(self, path="", facts=[]):
        '''
        使用 MLSD 命令获取远程目录信息.
        '''
        if facts:
            self.sendcmd("OPTS MLST " + ";".join(facts) + ";")
        if path:
            cmd = "MLSD %s" % path
        else:
            cmd = "MLSD"
        lines = []
        self.retrlines(cmd, lines.append)
        for line in lines:
            facts_found, _, name = line.rstrip(CRLF).partition(' ')
            entry = {}
            for fact in facts_found[:-1].split(";"):
                key, _, value = fact.partition("=")
                entry[key.lower()] = value
            yield (name, entry)

    def cwd(self, dirname):
        '''更换目录'''
        if dirname == '..':
            try:
                return self.voidcmd('CDUP')
            except error_perm as msg:
                if msg.args[0][:3] != '500':
                    raise
        elif dirname == '':
            dirname = '.'  # 错误情况
        cmd = 'CWD ' + dirname
        return self.voidcmd(cmd)

    def pwd(self):
        '''当前目录.'''
        resp = self.voidcmd('PWD')
        if not resp.startswith('257'):
            return ''
        return parse257(resp)

    def quit(self):
        '''退出并关闭连接.'''
        resp = self.voidcmd('QUIT')
        self.close()
        return resp


    def close(self):
        '''无条件关闭连接.'''
        try:
            file = self.file
            self.file = None
            if file is not None:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock is not None:
                sock.close()

def parse150(resp):
    '''解析 RETR 请求的 150 回复.
    '''
    if resp[:3] != '150':
        raise error_reply(resp)
    global _150_re
    if _150_re is None:
        import re
        _150_re = re.compile(
            r"150 .* \((\d+) bytes\)", re.IGNORECASE | re.ASCII)
    m = _150_re.match(resp)
    if not m:
        return None
    return int(m.group(1))

def parse257(resp):
    '''解析 MKD 或 PWD 请求的 ‘257’ 回复.'''
    if resp[:3] != '257':
        raise error_reply(resp)
    if resp[3:5] != ' "':
        return ''
    dirname = ''
    i = 5
    n = len(resp)
    while i < n:
        c = resp[i]
        i = i+1
        if c == '"':
            if i >= n or resp[i] != '"':
                break
            i = i+1
        dirname = dirname + c
    return dirname

def print_line(line):
    '''默认 retrlines 回调函数'''
    print(line)

if __name__ == '__main__':  # debug
    pass
