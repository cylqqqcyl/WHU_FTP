import os
import os.path
from backend.FTP_user import FTP_user as FTP
from backend.FTP_user import error_perm
import datetime
from datetime import datetime


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
        # print(ftp.getwelcome())

        return ftp

    @staticmethod
    def upload_file(ftp, local_path, remote_path, callback=None):
        # 从本地上传文件到ftp
        buffer_size = 1024
        try:
            ftp.voidcmd('TYPE I')  # 设置为二进制模式
            uploaded_size = ftp.size(remote_path)  # 断点续传
        except error_perm:  # 如果还没有开始上传，那么uploaded_size=0
            uploaded_size = 0
        fp = open(local_path, 'rb')
        fp.seek(uploaded_size)
        ftp.storbinary('STOR ' + remote_path, fp, buffer_size, rest=uploaded_size, callback=callback)
        fp.close()

    @staticmethod
    def download_file(ftp, remote_path, local_path):
        # 从ftp下载文件
        buffer_size = 1024
        if os.path.exists(local_path):  # 防止续传覆盖
            fp = open(local_path, 'rb+')
        else:
            fp = open(local_path, 'wb')
        downloaded_size = os.path.getsize(local_path)  # 断点续传
        fp.seek(downloaded_size)
        ftp.retrbinary('RETR ' + remote_path, fp.write, buffer_size, rest=downloaded_size)
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