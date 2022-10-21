from ftplib import FTP
import datetime
import argparse

def ftpconnect(host, username='', password=''):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host,21) #填自己服务的端口号 一般是21
    ftp.login(username, password)
    ftp.set_pasv(False) #主动模式
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="172.27.240.1", help="host")
    parser.add_argument("--username", type=str, default="", help="username")
    parser.add_argument("--password", type=str, default="", help="password")
    parser.add_argument("--mode", type=str, required=True, help="upload or download")
    parser.add_argument("--localpath", type=str, required=True, help="local file path")
    parser.add_argument("--remotepath", type=str, required=True, help="remote file path")

    args = parser.parse_args()

    ftp = ftpconnect(args.host, args.username, args.password)
    print(args.mode)
    if args.mode == "upload":
        uploadfile(ftp, args.localpath, args.remotepath)
    elif args.mode == "download":
        downloadfile(ftp, args.localpath, args.remotepath)
    else:
        raise ValueError("unsupported mode!\n"
                         "upload: upload some file to the host\n"
                         "download: download some file from the host")

    ftp.quit()

if __name__ == "__main__":
    main()