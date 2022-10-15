from ftplib import FTP
import datetime

def ftpconnect(host, username, password):
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

if __name__ == "__main__":
    cur_dir = __file__.strip('src\\user.py')
    local_dir = cur_dir + "\\local_Dir"

    ftp = ftpconnect("192.168.3.202", "user", "123456")
    local_file = local_dir+"\\local.txt"
    target_file = 'local.txt'
    uploadfile(ftp, local_file, target_file)
    downloadfile(ftp, "test.txt",local_dir+"\\test.txt")
    ftp.quit()