# ==========================================================================================#
#   progress : Spawned subprocess from winFastText to show doing time consuming something.
# ==========================================================================================#
#   Author:
#     Kiyoshi Hirose, Representative of HIT Business Consulting Firm.
#   Abstract:
#      This program shows progress bar INDETERMINATE mode.
#   Github:
#      https://
#   License: MIT License.
#      Find License.txt for more detail.
#   Version history:
#      0.0.1 : 2019-11-xx
# ---
import tkinter as tk
from tkinter import ttk
import configparser

config = configparser.ConfigParser()
ini_file = './config.ini'
config.read(ini_file, encoding='utf-8')
ini_sc_bgright = config.get('screen', 'ini_sc_bgright')

root = tk.Tk()
root.title('Progress')
root.columnconfigure(0, weight=1);
root.rowconfigure(0, weight=1);
root.configure(background=ini_sc_bgright, borderwidth=8, relief=tk.RIDGE)

# === progress bar as indeterminate ===
tk.Label(root, text='   fasttext is in progress...   ', font=('Comic Sans MS', '14'), width=30,
         bg=ini_sc_bgright, fg='white').grid(row=0, column=0, pady=5)
pb = ttk.Progressbar(
        root, 
        orient='horizontal', 
        length=300,
        mode='indeterminate')
pb.configure(maximum=10, value=0)
pb.grid(row=1, column=0, pady=20)
pb.start(100)

root.mainloop()