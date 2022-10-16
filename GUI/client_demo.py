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


if __name__ == '__main__':
    root.mainloop()