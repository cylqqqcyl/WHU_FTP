import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.scrolledtext as st
import tkinter.font as tf
import time
import threading
import os

root = tk.Tk()
root.title('WHU FTP')
root.geometry('800x600')
root.resizable(width=False, height=False)
# flat, groove, raised, ridge, solid, or sunken
font_root_title = tf.Font(family='Arial', size=18, weight=tf.BOLD)
font_frame_title = tf.Font(family='Arial', size=14, weight=tf.BOLD)

label_titile = tk.Label(root, text='FTP Server Demo', pady=5,font=font_root_title).pack()

def start_server():
    cmd_line = 'python ../src/admin.py'
    os.system(cmd_line)

button_start_server = tk.Button(root, text='start server', height=5, width=10, command=start_server)
button_start_server.place(x=325, y=70)
# button_stop_server = tk.Button(root, text='stop server', height=5, width=10, command=stop_server)
# button_stop_server.place(x=325, y=200)

if __name__ == '__main__':
    root.mainloop()