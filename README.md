# WHU_FTP
An FTP server based on pyftpdlib and qt
developing platform:
>OS:Windows
>Lang:python 3.9

## Prerequisites 
install pyftpdlib(optional)
```bash
pip install pyftpdlib
pip install PyOpenSSL
```
install qt for python
```bash
pip install PyQt5
```

## Description
本FTP服务器具有图形化界面、上传、下载功能，实现断点续传功能
### Frontend
图形化界面
包含登录界面、日志显示、本地文件和服务器文件显示、可视化上传及下载进度等
（用户端）
上传包含选择上传的文件（弹出本地浏览文件窗口）
下载包含选择下载的文件
同时还应该有暂停以及继续按键
（管理端）
设置选项（例如端口、ip、最大上传下载速度等）
用户管理（用户名称、登入状态等）

---
一个用户端界面的例子如下（仅供参考）
![用户FTP界面](figures/user_FTP.png)
一个管理端界面的例子如下（仅供参考）
![管理FTP界面](figures/admin_ftp.gif)
