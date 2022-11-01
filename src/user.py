from ftplib import FTP
import datetime
import argparse
from datetime import datetime


def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024


def get_datetime_format(date_time):
    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human readable date time string
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


def ftpconnect(host, username='', password='', port=21):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host, port)  # 填自己服务的端口号 一般是21
    ftp.login(username, password)
    ftp.set_pasv(False)  # 主动模式
    print(ftp.getwelcome())
    return ftp


def downloadfile(ftp, remotepath, localpath):
    # 从ftp下载文件
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def uploadfile(ftp, localpath, remotepath):
    # 从本地上传文件到ftp
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def get_server_files(ftp):
    '''
      字典返回FTP服务器文件及目录
      返回值:
        key: 文件/目录名
        value: 文件类型('dir','file','block')
    '''
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
                # convert it to human readable format (i.e in 'KB', 'MB', etc)
                file_size = get_size_format(file_size)
            else:
                # not a file, may be a directory or other types
                file_size = ""
            # date of last modification of the file
            last_modified = get_datetime_format(meta.get("modify"))
            # print all
            file_data_list = [file_name,file_size,file_type,last_modified]
            remote_files.append(file_data_list)
    return remote_files


def main():  # for debugging?
    parser = argparse.ArgumentParser()
    # parser.add_argument("--host", type=str, default="172.16.20.1", help="host")
    # parser.add_argument("--username", type=str, default="user", help="username")
    # parser.add_argument("--password", type=str, default="123456", help="password")
    # parser.add_argument("--mode", type=str, required=True, help="upload or download")
    # parser.add_argument("--localpath", type=str, required=True, help="local file path")
    # parser.add_argument("--remotepath", type=str, required=True, help="remote file path")

    parser.add_argument("--host", type=str, default="172.27.240.1", help="host")
    parser.add_argument("--username", type=str, default="user", help="username")
    parser.add_argument("--password", type=str, default="123456", help="password")
    parser.add_argument("--mode", type=str, default='download', help="upload or download")
    parser.add_argument("--localpath", type=str, default='local_dir/local.txt', help="local file path")
    parser.add_argument("--remotepath", type=str, default='user_dir/local.txt', help="remote file path")

    args = parser.parse_args()

    ftp = ftpconnect(args.host, args.username, args.password)

    print(get_server_files(ftp))

    ftp.quit()


if __name__ == "__main__":
    main()
