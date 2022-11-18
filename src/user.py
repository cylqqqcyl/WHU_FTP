import os.path
from ftplib import FTP
import datetime
import argparse
from datetime import datetime
import STATUS.ProcessBar as Pb
import time
filesize = 0
current_size = 0
bar = None

def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024


def get_datetime_format(date_time):
    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human-readable date time string
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


def ftpconnect(host, username='', password='', port=21):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host, port)  # 填自己服务的端口号 一般是21
    ftp.login(username, password)
    ftp.set_pasv(False)  # 主动模式
    print(ftp.getwelcome())
    return ftp

def uploadfile(ftp, localpath, remotepath):
    # 从本地上传文件到ftp
    bufsize = 1024
    uploaded_size = ftp.size(remotepath)  # 断点续传
    fp = open(localpath, 'rb')
    fp.seek(uploaded_size)
    ftp.storbinary('STOR ' + remotepath, fp, bufsize, rest=uploaded_size)
    ftp.set_debuglevel(0)
    fp.close()

def downloadfile(ftp, remotepath, localpath):
    # 从ftp下载文件
    global bar
    global filesize
    global fpdownload
    global downloaded_size
    # bar = Pb.PopupProgressBar('ftp download file: ' + remotepath)
    # bar.start()
    bufsize = 1024
    filesize = ftp.size(remotepath)
    print("filesize")
    try:
        print(filesize)
    except filesize==0:
        print("为零")
    if os.path.exists(localpath):  # 防止续传覆盖
        fpdownload = open(localpath, 'rb+')
    else:
        fpdownload = open(localpath, 'wb')
    downloaded_size = os.path.getsize(localpath)  # 断点续传
    print("downloaded1")
    print(downloaded_size)
    fpdownload.seek(downloaded_size)
    ftp.retrbinary('RETR ' + remotepath, fpdownload.write, bufsize, rest=downloaded_size)
    print("downloaded2")
    print(downloaded_size)
    # if filesize == 0:
    #     time.sleep(5)
    #     bar.stop()
    ftp.set_debuglevel(0)
    fpdownload.close()

def download_file_cb(block):
    global current_size
    # 写文件到本地
    # 显示下载进度
    current_size = current_size + len(block)
    print("current_size")
    try:
        print(current_size)
    except current_size==0:
        print("错误")
    tmp = 50
    bar.value = tmp
    bar.text = format(tmp, '.2f') + '%'
    if bar.value >= 100:
        time.sleep(10)
        bar.stop()
    fpdownload.write(block)


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
            print(file_type)
            if file_type == "file":
                # if it is a file, change type of transfer data to IMAGE/binary
                ftp.voidcmd("TYPE I")
                # get the file size in bytes
                file_size = ftp.size(file_name)
                # convert it to human-readable format (i.e in 'KB', 'MB', etc)
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


# def main():  # for debugging?
#     parser = argparse.ArgumentParser()
#     # parser.add_argument("--host", type=str, default="172.16.20.1", help="host")
#     # parser.add_argument("--username", type=str, default="user", help="username")
#     # parser.add_argument("--password", type=str, default="123456", help="password")
#     # parser.add_argument("--mode", type=str, required=True, help="upload or download")
#     # parser.add_argument("--localpath", type=str, required=True, help="local file path")
#     # parser.add_argument("--remotepath", type=str, required=True, help="remote file path")
#
#     parser.add_argument("--host", type=str, default="192.168.3.60", help="host")
#     parser.add_argument("--username", type=str, default="wql", help="username")
#     parser.add_argument("--password", type=str, default="123456", help="password")
#     parser.add_argument("--mode", type=str, default='download', help="upload or download")
#     parser.add_argument("--localpath", type=str, default='local_dir/local.txt', help="local file path")
#     parser.add_argument("--remotepath", type=str, default='user_dir/local.txt', help="remote file path")
#
#     args = parser.parse_args()
#
#     ftp = ftpconnect(args.host, args.username, args.password)
#
#     downloadfile(ftp,args.remotepath,args.localpath)
#     print(get_server_files(ftp))
#
#     ftp.quit()
#
#
# # if __name__ == "__main__":
# #     main()
