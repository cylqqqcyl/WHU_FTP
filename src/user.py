from ftplib import FTP
import datetime
import argparse


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


def main():  # for debugging?
    parser = argparse.ArgumentParser()
    # parser.add_argument("--host", type=str, default="172.16.20.1", help="host")
    # parser.add_argument("--username", type=str, default="user", help="username")
    # parser.add_argument("--password", type=str, default="123456", help="password")
    # parser.add_argument("--mode", type=str, required=True, help="upload or download")
    # parser.add_argument("--localpath", type=str, required=True, help="local file path")
    # parser.add_argument("--remotepath", type=str, required=True, help="remote file path")

    parser.add_argument("--host", type=str, default="172.16.20.1", help="host")
    parser.add_argument("--username", type=str, default="user", help="username")
    parser.add_argument("--password", type=str, default="123456", help="password")
    parser.add_argument("--mode", type=str, default='download', help="upload or download")
    parser.add_argument("--localpath", type=str, default='local_dir/local.txt', help="local file path")
    parser.add_argument("--remotepath", type=str, default='user_dir/local.txt', help="remote file path")

    args = parser.parse_args()

    ftp = ftpconnect(args.host, args.username, args.password)

    # if args.mode == "upload":
    #     uploadfile(ftp, args.localpath, args.remotepath)
    # elif args.mode == "download":
    #     downloadfile(ftp, args.localpath, args.remotepath)
    # else:
    #     raise ValueError("unsupported mode!\n"
    #                      "upload: upload some file to the host\n"
    #                      "download: download some file from the host")

    ftp.quit()


if __name__ == "__main__":
    main()
