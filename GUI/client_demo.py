import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.scrolledtext as st
import tkinter.font as tf
import time
import os

root = tk.Tk()
root.title('WHU FTP')
root.geometry('800x600')
root.resizable(width=False, height=False)
# flat, groove, raised, ridge, solid, or sunken
font_root_title = tf.Font(family='Arial', size=18, weight=tf.BOLD)
font_frame_title = tf.Font(family='Arial', size=14, weight=tf.BOLD)

label_titile = tk.Label(root, text='FTP Client Demo', pady=5,font=font_root_title).pack()

def select_local_file():
    path = filedialog.askopenfilename(filetypes=[('model path', '.*')])
    var_local_path.set(path)

var_local_path = tk.StringVar()

entry_local_path = tk.Entry(root, textvariable=var_local_path, width=30).place(x=100, y=75)

button_local_path = tk.Button(root, text='select', width=6, command=select_local_file)
button_local_path.place(x=325, y=70)

def upload_file():
    global var_local_path
    if var_local_path:
        cmd_line = 'python ../src/user.py --username %s --password %s --mode %s --localpath %s --remotepath %s' \
                   %(var_username.get(), var_password.get(), var_mode.get(), var_local_path.get(), var_remote_path.get())
        os.system(cmd_line)

var_username = tk.StringVar()
var_password = tk.StringVar()
var_mode = tk.StringVar()
var_remote_path = tk.StringVar()

entry_username = tk.Entry(root, textvariable=var_username, width=30).place(x=100, y=105)
entry_password = tk.Entry(root, textvariable=var_password, width=30).place(x=100, y=135)
entry_mode = tk.Entry(root, textvariable=var_mode, width=30).place(x=100, y=165)
entry_remote_path = tk.Entry(root, textvariable=var_remote_path, width=30).place(x=100, y=195)

if __name__ == '__main__':
    root.mainloop()