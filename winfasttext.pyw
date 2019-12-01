# =======================================================#
#   winFastText : Yet another fasttext on the Windows
# =======================================================#
#   Author:
#     Kiyoshi Hirose, Representative of HIT Business Consulting Firm.
#   Abstract:
#      This program is full compatible with command mode fasttext on the Linux.
#      You can execute fasttext command in this program with windows interface.
#   Github:
#      https://github.com/KiyoshiHirose/winFT-0.1.1
#   License: MIT License.
#      Find License.txt for more detail.
#   Version history:
#      0.0.1 : 2019-11-26
#      0.1.1 : 2019-11-29
# ---
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import configparser
import os, sys
import webbrowser
import subprocess
import fasttext as ft
import MeCab
import wmi


class winFastText(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.winftMenu()
        return

    # === winFT window initialize and build command menu ===
    def winftMenu(self):
        global v, pw_main, pw_right
        pw_main = tk.PanedWindow(self.master, orient='horizontal')
        pw_main.pack(expand=True, fill='both', side='left')
        pw_left = tk.PanedWindow(pw_main, bg=ini_sc_bgleft, orient='vertical')
        pw_right = tk.PanedWindow(pw_main, bg=ini_sc_bgright, orient='vertical')
        pw_right.option_add('*font', eval(ini_me_fontR))
        pw_left.option_add('*font', eval(ini_me_fontL))
        pw_main.add(pw_left)
        pw_main.add(pw_right)
        img = Image.open(ini_fi_logo)
        self.logo = ImageTk.PhotoImage(img)
        tk.Button(pw_left, image=self.logo, anchor='w', command=lambda: self.fthelp(), cursor='hand2') \
            .grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        tk.Label(pw_left, text='$ fasttext ', width=12, justify='left', fg='white',
                 bg=ini_sc_bgleft).grid(row=1, column=0)
        v = tk.IntVar()  # radio button on/off variable
        i = 1
        img = Image.open(ini_fi_helpIcon)
        self.icon = ImageTk.PhotoImage(img)
        for command in eval(ini_me_comList):
            # arrange command button
            tk.Radiobutton(pw_left, text=command, indicatoron=0, variable=v, value=i, borderwidth=2,
                           bg=ini_sc_bgright, fg='white', relief='groove', activebackground='coral',
                           selectcolor='coral', highlightcolor=ini_sc_bgright, anchor='w', cursor='hand2',
                           command=lambda command=command: self.dispatch(command)) \
                           .grid(row=i, column=1, sticky=tk.W+tk.E)
            # arrange help button following command button
            tk.Button(pw_left, image=self.icon, bd=0, bg=ini_sc_bgleft, activebackground=ini_sc_bgleft,
                      cursor='hand2',
                      command=lambda command=command: self.comHelp(command)).grid(row=i, column=3)
            i += 1
        # Reset button
        tk.Button(pw_left, text='Reset', command=lambda: self.reset(), width=6, activebackground='coral',
                  cursor='hand2',
                  bg=ini_sc_bgright, fg='white').grid(row=i, column=0, columnspan=3, padx=115, pady=176, sticky='w')
        # Exit button
        tk.Button(pw_left, text='Exit', command=self.master.destroy, width=6, activebackground='coral',
                  cursor='hand2',
                  bg=ini_sc_bgright, fg='white').grid(row=i, column=0, columnspan=3, padx=72, pady=176, sticky='e')
        # Welcome message on the right pane.
        tk.Label(pw_right, text='Welcome on board to the winFastText world!', fg='white', bg=ini_sc_bgright,
                 justify='center').grid(padx=230, pady=300)
        return

    # === Menu command dispatcher ===
    def dispatch(self, command):
        if command == 'Supervised':
            self.supervised()
        if command == 'Skipgram':
            self.skipgram()
        if command == 'CBOW':
            self.cbow()
        if command == 'Test-Label':
            self.test_label()
        if command == 'Predict-Prob':
            self.predict_prob()
        if command == 'Nearest Neighbors  ':
            self.nn()
        if command == 'Analogies':
            self.analogies()
        return

# ================================
#    fasttext command functions
# ================================
    # === $ fasttext supervised... ===
    def supervised(self):
        self.clearRightPane()  # clear right pane just in case.
        self.cd()  # change dir as set default working directory from now on.
        self.putLabel('$ fasttext supervised ...', 1, 0, 3)
        self.train('super')
        return

    # === $ fasttext skipgram... ===
    def skipgram(self):
        self.clearRightPane()  # clear right pane just in case.
        self.cd()  # change dir as set default working directory from now on.
        self.putLabel('$ fasttext skipgram ...  ', 1, 0, 3)
        self.train('skip')
        return

    # === $ fasttext cbow... ===
    def cbow(self):
        self.clearRightPane()  # clear right pane just in case.
        self.cd()  # change dir as set default working directory from now on.
        self.putLabel('$ fasttext cbow ...     ', 1, 0, 3)
        self.train('cbow')
        return

    # === $ fasttext test-label... ===
    def test_label(self):
        self.testCommon('test_label')
        return

    # === $ fasttext predict-prob... ===
    def predict_prob(self):
        self.testCommon('predict_prob')
        return

    # === $ fasttext nn... ===
    def nn(self):
        self.testCommon('nn')
        return

    # === $ fasttext analogies... ===
    def analogies(self):
        self.testCommon('analogies')
        return

    # === Reset menu button and erase right PaneWindow
    def reset(self):
        v.set(0)  # set left pane radio button off
        self.clearRightPane()
        tk.Label(pw_right, text='Welcome on board to the winFastText world!', fg='white',
                 bg=ini_sc_bgright).grid(padx=230, pady=300)
        return

    # === Erase right PaneWindow ===
    def clearRightPane(self):
        global pw_main, pw_right
        pw_main.forget(pw_right)
        pw_right = tk.PanedWindow(pw_main, bg=ini_sc_bgright, orient='vertical')
        pw_right.option_add('*font', eval(ini_me_fontR))
        pw_main.add(pw_right)
        return

    # === Display fasttext help on your browser ===
    def browsFtDoc(self, helpwin):
        fturl = 'https://fasttext.cc/'
        webbrowser.open(fturl)
        helpwin.destroy()
        return

    # === Popup window of fastText help ===
    #     It's same contents with $ fasttext (enter)
    def fthelp(self):
        with open(ini_fi_fthelp, 'r', encoding='utf-8') as f:
            msg = f.read()
        helpwin = tk.Toplevel(master=root)
        helpwin.title('Help fasttText')
        helpwin.geometry()
        tk.Label(helpwin, text=msg, bg=ini_sc_bgright, fg='white', font=eval(ini_me_helpFont),
                 justify='left').pack(padx=5, pady=5)
        tk.Button(helpwin, text='Brows fasttext document.', bg=ini_sc_bgleft, fg='white', font=eval(ini_me_helpFont),
                  activebackground='coral', cursor='hand2',
                  command=lambda: self.browsFtDoc(helpwin)).pack(fill='x')
        helpwin.focus_set()
        return

    # === Popup window of each command help ===
    #     It's same contents of each $ fasttext ft-comand (enter)
    def comHelp(self, command):
        if command == 'Supervised':
            file = ini_fi_supervised
        if command == 'Skipgram':
            file = ini_fi_skipgram
        if command == 'CBOW':
            file = ini_fi_cbow
        if command == 'Test-Label':
            file = ini_fi_test_l
        if command == 'Predict-Prob':
            file = ini_fi_predict_p
        if command == 'Nearest Neighbors  ':
            file = ini_fi_nn
        if command == 'Analogies':
            file = ini_fi_analogies
        with open(file, 'r', encoding='utf-8') as f:
            msg = f.read()
        helpwin = tk.Toplevel(master=root)
        helpwin.title('Help ' + command)
        helpwin.geometry()
        tk.Label(helpwin, text=msg, bg=ini_sc_bgright, fg='white', font=eval(ini_me_helpFont),
                 justify='left').pack(padx=5, pady=5)
        tk.Button(helpwin, text='Brows fasttext document.', bg=ini_sc_bgleft, fg='white', font=eval(ini_me_helpFont),
                  activebackground='coral', cursor='hand2',
                  command=lambda: self.browsFtDoc(helpwin)).pack(fill='x')
        helpwin.focus_set()
        return

    # === Progress bar ===
    def progress(self):
        global progBar
        prog = 'progress.pyw'
        progBar = subprocess.Popen(['pythonw', prog])
        return

    # === Common function of tk.Label(...) ===
    def putLabel(self, text, row, column, columnspan):
        tk.Label(pw_right, text=text, bg=ini_sc_bgright, fg='white', justify='left') \
            .grid(row=row, column=column, columnspan=columnspan, padx=10, sticky='w')
        return

    # === Change default working directory ===
    def cd(self):
        global defDir
        self.putLabel('$ cd', 0, 0, 5)
        defDir = tk.Entry(pw_right, width=41, justify='left')
        defDir.insert(tk.END, currentDir)
        defDir.grid(row=0, column=0, columnspan=5, padx=65, pady=5, sticky='w')
        img = Image.open(ini_fi_folderIcon)
        self.folderIcon1 = ImageTk.PhotoImage(img)
        tk.Button(pw_right, image=self.folderIcon1, command=lambda: self.dirExp(), bd=0, cursor='hand2',
                  bg=ini_sc_bgright, activebackground=ini_sc_bgright).grid(row=0, column=4, padx=5, sticky='e')
        return

    # === Directory search by Windows file explore ===
    def dirExp(self):
        global currentDir
        directory = tk.filedialog.askdirectory()
        if directory != '':
            currentDir = directory
            defDir.delete(0, tk.END)
            defDir.insert(0, currentDir)
        return

    # === File search by Windows file explore ===
    def fileExp(self, label):
        global ft_model, modelSemaphore
        filename = tk.filedialog.askopenfilename()
        if filename != '':
            label.delete(0, tk.END)
            label.insert(0, filename)
            fileSplit = filename.split('.')
            if len(fileSplit) > 1:         # > 1 : filename contains an extension like a xyz.txt,
                if fileSplit[1] == 'bin':  # else just a file name like a xyz
                    ft_model = filename
                    modelSemaphore = 0  # reset semaphore to load_model() for test_label, predict_prob, nn, analogies
        return

    # === File search by Windows file explore ===
    def preV(self):
        global Ent_pretrainedVectors
        vecFile = tk.filedialog.askopenfilename()
        if vecFile != '':
            Ent_pretrainedVectors.delete(0, tk.END)
            Ent_pretrainedVectors.insert(0, vecFile)
        return

    # === fasttext console message & exec fasttext as subprocess ===
    def execFastText(self, comStr):
        global progBar

        def ftResults(msg, fgColor, row, col,
                      colspan):  # create fasttext results show up window and display results
            tk.Label(ftWin, text=msg, bg=ini_sc_bgright, fg=fgColor, font=eval(ini_me_helpFont),
                     justify='left').grid(row=row, column=col, columnspan=colspan, sticky='w', padx=5, pady=5)
            return

        # === Start Progress bar ===
        self.progress()
        # === Exec fasttext as subprocess ===
        ftProc = subprocess.Popen(['pythonw', ini_fi_execFastTextPyw],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        msg1 = ftProc.communicate()
        msg2 = str(msg1[1]).replace("b'", "").replace('b"', '').replace("'", '').replace('"', '') \
                           .replace('\\r\\n', '\n').replace('\\r', '\n').replace('\\n', '\n') \
                           .replace('\n\n\n', '\n').replace('\n\n', '\n')
        returnCode = '{:X}'.format(ftProc.returncode)
        # === Terminate progress bar ===
        progBar.terminate()
        # === create fasttext results window ===
        ftWin = tk.Toplevel(master=root)
        ftWin.title('execFastText')
        ftWin.configure(background=ini_sc_bgright, borderwidth=7, relief=tk.RIDGE)
        ftWin.focus_set()
        # === Scan result statement from PIPE ===
        msg3 = '$ fasttext '+comStr+'\n\n'
        buff_1 = msg2.split('\n')
        buff_2 = ''
        del buff_1[-1]  # delete tail cell (tail cell is '')
        for i in range(len(buff_1)):
            if buff_1[i].startswith('Read'):
                Read_M = buff_1[i]
            elif buff_1[i].startswith('Number of words'):
                Num_w = buff_1[i]
            elif buff_1[i].startswith('Number of labels'):
                Num_l = buff_1[i]
            elif buff_1[i].startswith('Progress'):
                Prog = buff_1[i]
            else:
                buff_2 += buff_1[i]+'\n'
        msg3 += Read_M+'\n'+Num_w+'\n'+Num_l+'\n'+Prog+'\n'+buff_2
        if returnCode == '0':  # OK!
            fgColor = 'white'
            ftWin.geometry('900x300')
            msg3 += '\nCompleted'
        else:
            fgColor = 'yellow'
            ftWin.geometry('950x400')
            if returnCode == 'C0000409':
                msg3 += '\nError status: '+returnCode+'\nSTATUS_STACK_BUFFER_OVERRUN has occurred.\n'
                msg3 += 'Reconsider to reduce number of lr or epoch.'
            else:
                msg3 += '\nError status: ' + returnCode + '\nsomething wrong has happened.\n'
                msg3 += 'Reconsider to reduce number of lr or epoch.\nor\nCheck input or output file name.'
        ftResults(msg3, fgColor, 0, 0, 1)  # create fasttext results show up window and display results
        return

    # ==================================================
    #    common function for supervised/skipgram/cbow
    # ==================================================
    def train(self, command):
        global Ent_input, Ent_pretrainedVectors
        # command : 'super' - fasetext supervised
        #         : 'skip'  - fasttext skipgram
        #         : 'cbow'  - fasetext cbow

        # === save input parameters as linux utf-8 shell script ===
        def saveLinux():
            global currentDir
            errMsg = ''
            if currentDir.startswith('Click'):         errMsg += 'working dir has not set.\n'
            if Ent_input.get().startswith('Select'):   errMsg += '-input has not set.\n'
            if Ent_output.get().startswith('Specify'): errMsg += '-output has not set.\n'
            if errMsg != '':
                messagebox.showerror('SaveAsLinuxShell Error', errMsg)
            else:
                shell = '#!/usr/bin/bash\n'
                shell += 'fasttext '
                if command == 'super':
                    shell += 'supervised '
                if command == 'skip':
                    shell += 'skipgram '
                if command == 'cbow':
                    shell += 'cbow '
                shell += '-input '+Ent_input.get()+' -output '+Ent_output.get()+' \\\n'
                if Ent_lr.get() != '':            shell += ' -lr '+Ent_lr.get()
                if Ent_dim.get() != '':           shell += ' -dim '+Ent_dim.get()
                if Ent_ws.get() != '':            shell += ' -ws '+Ent_ws.get()
                if Ent_epoch.get() != '':         shell += ' -epoch '+Ent_epoch.get()
                if Ent_minCount.get() != '':      shell += ' -minCount '+Ent_minCount.get()
                if Ent_minn.get() != '':          shell += ' -minn '+Ent_minn.get()
                if Ent_maxn.get() != '':          shell += ' -maxn '+Ent_maxn.get()+' \\\n'
                if Ent_neg.get() != '':           shell += ' -neg '+Ent_neg.get()
                if Ent_wordNgrams.get() != '':    shell += ' -wordNgrams '+Ent_wordNgrams.get()
                if Ent_loss.get() != '':          shell += " -loss '"+Ent_loss.get()+"'"
                if Ent_bucket.get() != '':        shell += ' -bucket '+Ent_bucket.get()
                if Ent_thread.get() != '':        shell += ' -thread '+Ent_thread.get()
                if Ent_lrUpdateRate.get() != '':  shell += ' -lrUpdateRate '+Ent_lrUpdateRate.get()+' \\\n'
                if Ent_t.get() != '':             shell += ' -t '+Ent_t.get()
                if Ent_verbose.get() != '':       shell += ' -verbose '+Ent_verbose.get()
                if command == 'super':
                    if Ent_minCountLabel.get() != '': shell += ' -minCountLabel ' + Ent_minCountLabel.get()
                    if Ent_label.get() != '':             shell += " -label '"+Ent_label.get()+"'"
                    if Ent_pretrainedVectors.get() != '': shell += " -pretrinedVectors '"+Ent_pretrainedVectors.get()+"'"

                saveFile = currentDir+'/saveAsLinuxShell.sh'
                file = open(saveFile, 'w', newline='\n', encoding='utf-8')
                file.write(shell)
                file.close()
                msg = 'Shell script has been saved on '+currentDir+'.'
                messagebox.showinfo('SaveAsLinuxShell Succeeded', msg)
                return

        # === input parameters error check when 'Run fasttext' button pressed and exec when no errors ===
        def trainErrCheck():
            errMsg = ''
            if currentDir.startswith('Click'):         errMsg += 'working dir has not set.\n'
            if Ent_input.get().startswith('Select'):   errMsg += '-input has not set.\n'
            if Ent_output.get().startswith('Specify'): errMsg += '-output has not set.\n'
            if Ent_lr.get().replace('.', '').isnumeric():
                if float(Ent_lr.get()) >= 1.0:
                    errMsg += '-lr is too large.\n'
            else:
                if Ent_lr.get() != '':
                    errMsg += '-lr is neither float nor numeric.\n'
            if not(Ent_dim.get().isnumeric() or Ent_dim.get() == ''):
                errMsg += '-dim is not numeric.\n'
            if not(Ent_ws.get().isnumeric() or Ent_ws.get() == '') :
                errMsg += '-ws is not numeric.\n'
            if not(Ent_epoch.get().isnumeric() or Ent_epoch.get() == ''):
                errMsg += '-epoch is not numeric.\n'
            if not(Ent_minCount.get().isnumeric() or Ent_minCount.get() == ''):
                errMsg += '-minCount is not numeric.\n'
            if not(Ent_minn.get().isnumeric() or Ent_minn.get() == ''):
                errMsg += '-minn is not numeric.\n'
            if not(Ent_maxn.get().isnumeric() or Ent_maxn.get() == ''):
                errMsg += '-maxn is not numeric.\n'
            if not(Ent_neg.get().isnumeric() or Ent_neg.get() == ''):
                errMsg += '-neg is not numeric.\n'
            if not(Ent_wordNgrams.get().isnumeric() or Ent_wordNgrams.get() == ''):
                errMsg += '-wordNgrams is not numeric.\n'
            if not(Ent_bucket.get().isnumeric() or Ent_bucket.get() == ''):
                errMsg += '-bucket is not numeric.\n'
            if not(Ent_thread.get().isnumeric() or Ent_thread.get() == ''):
                errMsg += '-thread is not numeric.\n'
            if not(Ent_lrUpdateRate.get().isnumeric() or Ent_lrUpdateRate.get() == ''):
                errMsg += '-lrUpdateRate is not numeric.\n'
            if not(Ent_t.get().replace('.', '').isnumeric() or Ent_t.get() == ''):
                errMsg += '-t is neither float nor numeric.\n'
            if not(Ent_verbose.get().isnumeric() or Ent_verbose.get() == ''):
                errMsg += '-verbose is not numeric.\n'
            if command == 'super':
                if not(Ent_minCountLabel.get().isnumeric() or Ent_minCountLabel.get() == ''):
                    errMsg += '-minCountLabel is not numeric.\n'
                if Ent_label.get() == '' or ' ' in Ent_label.get():
                    errMsg += '-label has not set or invalid string for Label.\n'
                preV = Ent_pretrainedVectors.get()
                if preV != '':
                    if '.' in preV:
                        preV = preV.replace('.', '')
                    if not preV.isalnum(): errMsg += '-pretraindVectors is invalid.\n'

            if errMsg != '':
                messagebox.showerror('Error', errMsg)
            else:
                setAPIparam()
            return

        # === Set API parameter values into the ft.ini ===
        def setAPIparam():
            if command == 'super': comStr = 'supervised...'
            if command == 'skip':  comStr = 'skipgram...'
            if command == 'cbow':  comStr = 'cbow...'
            config = configparser.ConfigParser()
            section1 = 'general'
            config.add_section(section1)
            config.set(section1, 'ft_command', command)
            config.set(section1, 'ft_currentDir', currentDir)
            section2 = command
            config.add_section(section2)
            config.set(section2, 'Ent_input',        Ent_input.get())
            config.set(section2, 'Ent_output',       Ent_output.get())
            config.set(section2, 'Ent_lr',           Ent_lr.get())
            config.set(section2, 'Ent_dim',          Ent_dim.get())
            config.set(section2, 'Ent_ws',           Ent_ws.get())
            config.set(section2, 'Ent_epoch',        Ent_epoch.get())
            config.set(section2, 'Ent_minCount',     Ent_minCount.get())
            config.set(section2, 'Ent_minn',         Ent_minn.get())
            config.set(section2, 'Ent_maxn',         Ent_maxn.get())
            config.set(section2, 'Ent_neg',          Ent_neg.get())
            config.set(section2, 'Ent_wordNgrams',   Ent_wordNgrams.get())
            config.set(section2, 'Ent_loss',         Ent_loss.get())
            config.set(section2, 'Ent_bucket',       Ent_bucket.get())
            config.set(section2, 'Ent_thread',       Ent_thread.get())
            config.set(section2, 'Ent_lrUpdateRate', Ent_lrUpdateRate.get())
            config.set(section2, 'Ent_t',            Ent_t.get())
            config.set(section2, 'Ent_verbose',      Ent_verbose.get())
            if command == 'super':
                config.set(section2, 'Ent_minCountLabel',     Ent_minCountLabel.get())
                config.set(section2, 'Ent_label',             Ent_label.get())
                config.set(section2, 'Ent_pretrainedVectors', Ent_pretrainedVectors.get())
            with open(ini_fi_ftini, 'w', newline='\n', encoding='utf-8') as configfile:
                config.write(configfile)
            # === Execute fasttext as subprocess ===
            self.execFastText(comStr)
            return

    # === def train(self, command): main routine ===
        # row 2
        self.putLabel('  ', 2, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-input', 2, 1, 1)
        Ent_input = tk.Entry(pw_right, width=23, justify='left')
        if ft_input == '':
            Ent_input.insert(0, 'Select...')
        else:
            Ent_input.insert(0, ft_input)
        Ent_input.grid(row=2, column=2, columnspan=2, padx=10, sticky='w')
        img = Image.open(ini_fi_folderIcon)
        self.folderIcon2 = ImageTk.PhotoImage(img)
        tk.Button(pw_right, image=self.folderIcon2, command=lambda: self.fileExp(Ent_input), bd=0, cursor='hand2',
                  bg=ini_sc_bgright, activebackground=ini_sc_bgright).grid(row=2, column=3, sticky='e')
        self.putLabel('-output', 2, 4, 1)
        Ent_output = tk.Entry(pw_right, width=15, justify='left')
        Ent_output.insert(0, 'Specify...')
        Ent_output.grid(row=2, column=5, padx=10, sticky='w')
        # row 3
        if command == 'super':
            lr = 0.1
        else:
            lr = 0.05
        self.putLabel('  ', 3, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-lr', 3, 1, 1)
        Ent_lr = tk.Entry(pw_right, width=4, justify='right')
        Ent_lr.insert(tk.END, lr)
        Ent_lr.grid(row=3, column=2, padx=10, sticky='w')
        self.putLabel('-dim', 3, 3, 1)
        Ent_dim = tk.Entry(pw_right, width=4, justify='right')
        Ent_dim.insert(tk.END, 100)
        Ent_dim.grid(row=3, column=4, padx=10, sticky='w')
        # row 4
        self.putLabel('  ', 4, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-ws', 4, 1, 1)
        Ent_ws = tk.Entry(pw_right, width=2, justify='right')
        Ent_ws.insert(tk.END, 5)
        Ent_ws.grid(row=4, column=2, padx=10, sticky='w')
        self.putLabel('-epoch', 4, 3, 1)
        Ent_epoch = tk.Entry(pw_right, width=2, justify='right')
        Ent_epoch.insert(tk.END, 5)
        Ent_epoch.grid(row=4, column=4, padx=10, sticky='w')
        # row 5
        if command == 'super':
            mincount = 1
        else:
            mincount = 5
        self.putLabel('  ', 5, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-minCount', 5, 1, 1)
        Ent_minCount = tk.Entry(pw_right, width=2, justify='right')
        Ent_minCount.insert(tk.END, mincount)
        Ent_minCount.grid(row=5, column=2, padx=10, sticky='w')
        if command == 'super':
            self.putLabel('-minCountLabel', 5, 3, 1)
            Ent_minCountLabel = tk.Entry(pw_right, width=2, justify='right')
            Ent_minCountLabel.insert(tk.END, 0)
            Ent_minCountLabel.grid(row=5, column=4, padx=10, sticky='w')
        # row 6
        if command == 'super':
            minn = 0; maxn = 0
        else:
            minn = 3; maxn = 6
        self.putLabel('  ', 6, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-minn', 6, 1, 1)
        Ent_minn = tk.Entry(pw_right, width=2, justify='right')
        Ent_minn.insert(tk.END, minn)
        Ent_minn.grid(row=6, column=2, padx=10, sticky='w')
        self.putLabel('-maxn', 6, 3, 1)
        Ent_maxn = tk.Entry(pw_right, width=2, justify='right')
        Ent_maxn.insert(tk.END, maxn)
        Ent_maxn.grid(row=6, column=4, padx=10, sticky='w')
        # row 7
        self.putLabel('  ', 7, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-neg', 7, 1, 1)
        Ent_neg = tk.Entry(pw_right, width=2, justify='right')
        Ent_neg.insert(tk.END, 5)
        Ent_neg.grid(row=7, column=2, padx=10, sticky='w')
        self.putLabel('-wordNgrams', 7, 3, 1)
        Ent_wordNgrams = tk.Entry(pw_right, width=2, justify='right')
        Ent_wordNgrams.insert(tk.END, 1)
        Ent_wordNgrams.grid(row=7, column=4, padx=10, sticky='w')
        # row 8
        self.putLabel('  ', 8, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-loss', 8, 1, 1)
        Ent_loss = ttk.Combobox(pw_right, state='readonly', width=8,
                                values=('ns', 'hs', 'softmax', 'ova'))
        if command == 'super':
            cur = 2  # initial value: softmax
        else:
            cur = 0  # initial value: ns
        Ent_loss.current(cur)
        Ent_loss.grid(row=8, column=2, padx=10, sticky='w')
        self.putLabel('-bucket', 8, 3, 1)
        Ent_bucket = tk.Entry(pw_right, width=8, justify='right')
        Ent_bucket.insert(tk.END, 2000000)
        Ent_bucket.grid(row=8, column=4, padx=10, sticky='w')
        # row 9
        self.putLabel('  ', 9, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-thread', 9, 1, 1)
        Ent_thread = tk.Entry(pw_right, width=3, justify='right')
        if command == 'super':
            th = 12
        else:
            th = ''  # number of CPUs
        Ent_thread.insert(tk.END, th)
        Ent_thread.grid(row=9, column=2, padx=10, sticky='w')
        self.putLabel('-lrUpdateRate       ', 9, 3, 1)
        Ent_lrUpdateRate = tk.Entry(pw_right, width=4, justify='right')
        Ent_lrUpdateRate.insert(tk.END, 100)
        Ent_lrUpdateRate.grid(row=9, column=4, padx=10, sticky='w')
        # row 10
        self.putLabel('  ', 10, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('-t', 10, 1, 1)
        Ent_t = tk.Entry(pw_right, width=6, justify='right')
        Ent_t.insert(tk.END, 0.0001)
        Ent_t.grid(row=10, column=2, padx=10, sticky='w')
        self.putLabel('-verbose', 10, 3, 1)
        Ent_verbose = tk.Entry(pw_right, width=2, justify='right')
        Ent_verbose.insert(tk.END, 2)
        Ent_verbose.grid(row=10, column=4, padx=10, sticky='w')
        # row 11 (supervised only)
        if command == 'super':
            self.putLabel('  ', 11, 0, 1)  # dummy space to keep balance of column 0
            self.putLabel('-label', 11, 1, 1)
            Ent_label = tk.Entry(pw_right, width=8, justify='left')
            Ent_label.insert(tk.END, '__label__')
            Ent_label.grid(row=11, column=2, padx=10, sticky='w')
            self.putLabel('-pretrainedVectors', 11, 3, 1)
            Ent_pretrainedVectors = tk.Entry(pw_right, width=22, justify='left')
            Ent_pretrainedVectors.insert(tk.END, '')
            Ent_pretrainedVectors.grid(row=11, column=4, columnspan=3, padx=10, sticky='w')
            tk.Button(pw_right, image=self.folderIcon2, command=lambda: self.preV(), bd=0, cursor='hand2',
                      bg=ini_sc_bgright, activebackground=ini_sc_bgright)\
                .grid(row=11, column=4, columnspan=3, sticky='e')

        Ypad = 88
        if command != 'super': Ypad += 40
        tk.Button(pw_right, text='Run fasttext', command=lambda: trainErrCheck(), width=12,
                  activebackground='coral', cursor='hand2',
                  bg=ini_sc_bgleft, fg='white').grid(row=16, column=0, columnspan=6, padx=147, pady=Ypad, sticky='w')
        tk.Button(pw_right, text='Save as Linux shell', command=lambda: saveLinux(), width=18,
                  activebackground='coral', cursor='hand2',
                  bg=ini_sc_bgleft, fg='white').grid(row=16, column=0, columnspan=6, pady=Ypad)
        tk.Button(pw_right, text='Quit', command=lambda: self.reset(), width=12,
                  activebackground='coral', cursor='hand2',
                  bg=ini_sc_bgleft, fg='white').grid(row=16, column=0, columnspan=6, padx=147, pady=Ypad, sticky='e')
        return

    # ==============================================================
    #    common function for test-label/predict-prob/nn/analogies
    # ==============================================================
    def testCommon(self, command):
        global Ent_test, Ent_wordA, Ent_wordB, Ent_wordC, ft_model

        # === input parameters error check when 'Run fasttext' button pressed and exec when no errors ===
        def testErrCheck():
            global modelSemaphore, Ent_test, Ent_wordA, Ent_wordB, Ent_wordC, model

            def ftResults(msg, fgColor, row, col, colspan, side='w'):  # create fasttext results show up window
                tk.Label(ftWin, text=msg, bg=ini_sc_bgright, fg=fgColor, font=eval(ini_me_helpFont),
                         justify='left').grid(row=row, column=col, columnspan=colspan, sticky=side, padx=5, pady=5)
                return

            def test_nn(msg, fgColor):  # parse test_label/nearest neighbor results
                row = 3; col = 0
                if fgColor == 'white':
                    msg = msg.replace(' )', ')')
                    lineArray = msg.split('\n')
                    del lineArray[-1]  # delete final null cell
                    no = 1  # as sequence number
                    for line in lineArray:
                        ftResults(no, fgColor, row, col, 1, 'e')  # show seq. no.
                        no += 1; col += 1
                        item = line.split(' ')
                        for i in range(len(item)):
                            ftResults(item[i], fgColor, row, col, 1)
                            col += 1
                        row += 1; col = 0
                else:  # exception
                    ftResults(msg, fgColor, row, col, 7)
                    row += 1
                ftResults('Completed.', fgColor, row, 0, 1)
                return

            def predict_prob(msg, fgColor):  # parse predict_prob results
                row = 3; col = 1
                if fgColor == 'white':
                    item = msg.split(' ')
                    del item[-1]  # delete final null cell
                    no = 1  # as priorities of labels
                    for i in range(len(item)):
                        if i % 2 == 0:
                            ftResults(no, fgColor, row, col, 1, 'e')  # show seq. no. as priorities
                            no += 1; col += 1
                            ftResults(item[i], fgColor, row, col, 1)
                            col += 1
                        else:
                            ftResults(item[i], fgColor, row, col+1, 1)
                            row += 1; col = 1
                else:  # exception
                    ftResults(msg, fgColor, row, col, 6)
                ftResults('Completed.', fgColor, row + 1, 0, 1)
                return

            errMsg = ''
            if currentDir.startswith('Click'):       errMsg += 'working dir has not set.\n'
            if Ent_model.get().startswith('Select'): errMsg += 'Model file has not set.\n'
            if command == 'test_label' or command == 'predict_prob' or command == 'nn':
                if Ent_test.get().startswith('Select'):  errMsg += 'Test file has not set.\n'
                if not(Ent_k.get().isnumeric() or Ent_k.get() == ''): errMsg += 'k is mot numeric.\n'
                if command == 'test_label' or command == 'predict_prob':
                    if Ent_th.get().replace('.', '').isnumeric():
                        if float(Ent_th.get()) >= 1.0:
                            errMsg += 'threshold is too large.\n'
                    else:
                        if Ent_th.get() != '':
                            errMsg += 'threshold is neither float nor numeric.\n'
            else:  # command = analogies
                if Ent_wordA.get() == '': errMsg += 'word A has not set.\n'
                if Ent_wordB.get() == '': errMsg += 'word B has not set.\n'
                if Ent_wordC.get() == '': errMsg += 'word C has not set.\n'
                if not (Ent_k.get().isnumeric() or Ent_k.get() == ''): errMsg += 'k is mot numeric.\n'

            if errMsg != '':
                messagebox.showerror('Error', errMsg)
            else:
                # === Set API parameter values into the ft.ini & exec API ===
                if command == 'test_label':  comStr = 'test-label...'
                if command == 'predict_prob': comStr = 'predict-prob...'
                if command == 'nn': comStr = 'nn...'
                if command == 'analogies': comStr = 'analogies...'
                config = configparser.ConfigParser()
                section1 = 'general'
                config.add_section(section1)
                config.set(section1, 'ft_command', command)
                config.set(section1, 'ft_currentDir', currentDir)
                section2 = command
                config.add_section(section2)
                config.set(section2, 'Ent_model', Ent_model.get())
                if command == 'test_label' or command == 'predict_prob' or command == 'nn':
                    test = Ent_test.get()
                    config.set(section2, 'Ent_test',  test)
                else:  # command = analogies
                    wordA = Ent_wordA.get()
                    wordB = Ent_wordB.get()
                    wordC = Ent_wordC.get()
                    config.set(section2, 'Ent_wordA', wordA)
                    config.set(section2, 'Ent_wordB', wordB)
                    config.set(section2, 'Ent_wordC', wordC)
                config.set(section2, 'Ent_k', Ent_k.get())
                if command == 'test_label' or command == 'predict_prob':
                    config.set(section2, 'Ent_th', Ent_th.get())
                with open(ini_fi_ftini, 'w', newline='\n', encoding='utf-8') as configfile:
                    config.write(configfile)
                # === Execute each fasttext API ===
                self.progress()  # Start Progress bar
                exceptionFlag = 0
                if modelSemaphore == 0:
                    modelFile = ft_model.encode('sjis') if winJP else ft_model
                    model = ft.load_model(modelFile)
                    modelSemaphore += 1
                msg = ''
                if command == 'test_label':
                    try:
                        testFile = test.encode('sjis') if winJP else test
                        result = model.test_label(testFile, k=int(Ent_k.get()), threshold=float(Ent_th.get()))
                        for item in result:
                            line = result[item]
                            p = round(line['precision'], 5)
                            r = round(line['recall'], 5)
                            f1 = round(line['f1score'], 5)
                            msg += item + ' F1-Score ' + str(f1) + ' Precision ' + str(p) + ' Recall ' + str(r) + '\n'
                        result = model.test(testFile, k=int(Ent_k.get()))
                        msg += 'N ' + str(result[0]) + '\n'
                        msg += 'P@' + str(Ent_k.get()) + ' ' + str(round(result[1], 3)) + '\n'
                        msg += 'R@' + str(Ent_k.get()) + ' ' + str(round(result[2], 3)) + '\n'
                    except:
                        exceptionFlag = 1
                        exc = sys.exc_info()
                        msg += str(exc[0]).replace("<class '", "").replace("'>", "") + ' : '
                        msg += str(exc[1]).replace("'", "")
                if command == 'predict_prob' or command == 'nn':
                    # === make sure you are the Japanese user or not ===
                    if winJP and mecab():  # for Japanese users
                        dicDir = ini_cab_dir
                        wakatiParam = '-Owakati '
                        tagger = MeCab.Tagger(wakatiParam + dicDir)
                        wakati = tagger.parse(test).rstrip()  # remove tail \n
                    else:  # for other users
                        wakati = test
                if command == 'predict_prob':
                    # === Predict Prob ===
                    try:
                        result = model.predict(wakati, k=int(Ent_k.get()), threshold=float(Ent_th.get()))
                        for i in range(len(result[0])):
                            msg += result[0][i] + ' ' + str(round(result[1][i], 5)) + ' '
                    except:  # model file was not supervised
                        exceptionFlag = 1
                        exc = sys.exc_info()
                        msg += str(exc[0]).replace("<class '", "").replace("'>", "")+' : '
                        msg += str(exc[1]).replace("'", "")
                if command == 'nn' or command == 'analogies':
                    # === Nearest Neighbors or Analogies===
                    if command == 'nn':
                        nn_ana = model.get_nearest_neighbors(wakati, k=int(Ent_k.get()))
                    else:  # ft_command = analogies
                        nn_ana = model.get_analogies(wordA, wordB, wordC, k=int(Ent_k.get()))
                    for result in nn_ana:
                        msg += result[1] + ' ' + str(round(result[0], 5)) + '\n'

                progBar.terminate()  # Terminate progress bar
                # === create fasttext results window ===
                ftWin = tk.Toplevel(master=root)
                ftWin.title('execFastText')
                ftWin.configure(background=ini_sc_bgright, borderwidth=7, relief=tk.RIDGE)
                ftWin.geometry('900x800')
                ftWin.focus_set()
                fgColor = 'white' if exceptionFlag == 0 else 'yellow'
#                comLine = '$ fasttext ' + comStr + '\n'
                comLine = '$ fasttext ' + comStr
                work = ft_model.split('/')
                modelFile = work[len(work)-1]
                if comStr == 'test-label...':
                    ftResults(comLine, fgColor, 0, 0, 7)
                    ftResults('Model :  ' + modelFile, fgColor, 1, 0, 7)
                    ftResults('Test data :  ' + test, fgColor, 2, 0, 7)
                    test_nn(msg, fgColor)
                if comStr == 'predict-prob...':
                    ftResults(comLine, fgColor, 0, 0, 6)
                    ftResults('Model :  ' + modelFile, fgColor, 1, 0, 6)
                    ftResults('Test data :  ' + test, fgColor, 2, 0, 6)
                    predict_prob(msg, fgColor)
                if comStr == 'nn...':
                    ftResults(comLine, fgColor, 0, 0, 6)
                    ftResults('Model :  ' + modelFile, fgColor, 1, 0, 6)
                    ftResults('Test data :  ' + test, fgColor, 2, 0, 6)
                    test_nn(msg, fgColor)
                if comStr == 'analogies...':
                    ftResults(comLine, fgColor, 0, 0, 6)
                    analogy = 'Analogy words :  ' + wordA + '  -  ' + wordB + '  +  ' + wordC
                    ftResults('Model :  ' + modelFile, fgColor, 1, 0, 6)
                    ftResults(analogy, fgColor, 2, 0, 6)
                    test_nn(msg, fgColor)
            return

        def mecab():  # MaCab is a Japanese morphological analysis tool for Japanese users.
            global MeCab, ini_cab_dir
            try:
                import MeCab
                config = configparser.ConfigParser()
                ini_file = 'config.ini'
                config.read(ini_file, encoding='utf-8')
                ini_cab_dir = config.get('mecab', 'ini_cab_dir')
                return True
            except:
                return False

    # === def test(self, command): main routine ===
        self.clearRightPane()  # clear right pane just in case.
        self.cd()  # change dir as set default working directory from now on.
        self.putLabel('$ fasttext '+command+' ...', 1, 0, 3)
        self.putLabel('  ', 2, 0, 1)  # dummy space to keep balance of column 0
        self.putLabel('model file', 2, 1, 1)
        Ent_model = tk.Entry(pw_right, width=50, justify='left')
        if ft_model == '':
            Ent_model.insert(0, 'Select...')
        else:
            Ent_model.insert(0, ft_model)
        Ent_model.grid(row=2, column=2, columnspan=5, padx=10, sticky='w')
        img = Image.open(ini_fi_folderIcon)
        self.folderIcon = ImageTk.PhotoImage(img)
        tk.Button(pw_right, image=self.folderIcon, command=lambda: self.fileExp(Ent_model), bd=0, cursor='hand2',
                  bg = ini_sc_bgright, activebackground = ini_sc_bgright).grid(row=2, column=7, sticky='w')
        self.putLabel('  ', 3, 0, 1)  # dummy space to keep balance of column 0
        if command == 'test_label' or command == 'predict_prob' or command == 'nn':
            self.putLabel('test data', 3, 1, 1)
            Ent_test = tk.Entry(pw_right, width=50, justify='left')
            if command == 'test_label':
                Ent_test.insert(0, 'Select...')
                tk.Button(pw_right, image=self.folderIcon, command=lambda: self.fileExp(Ent_test), bd=0, cursor='hand2',
                          bg=ini_sc_bgright, activebackground=ini_sc_bgright).grid(row=3, column=7, sticky='w')
            else:
                if command == 'predict_prob':
                    Ent_test.insert(0, 'Enter the word(s) to see predicted label')
                else:
                    Ent_test.insert(0, 'Enter the word(s) to see what is your NN')
            Ent_test.grid(row=3, column=2, columnspan=5, padx=10, sticky='w')
            self.putLabel('  ', 4, 0, 1)  # dummy space to keep balance of column 0
            self.putLabel('top k labels', 4, 1, 1)
            Ent_k = tk.Entry(pw_right, width=3, justify='right')
            k = 10 if command == 'nn' else 1
            Ent_k.insert(0, k)
            Ent_k.grid(row=4, column=2, padx=10, sticky='w')
            if command == 'test_label' or command == 'predict_prob':
                self.putLabel('  ', 5, 0, 1)  # dummy space to keep balance of column 0
                self.putLabel('threshold', 5, 1, 1)
                Ent_th = tk.Entry(pw_right, width=3, justify='right')
                Ent_th.insert(0, '0.0')
                Ent_th.grid(row=5, column=2, padx=10, sticky='w')
        else:  # command = analogies
            self.putLabel('  ', 3, 0, 1)  # dummy space to keep balance of column 0
            self.putLabel('analogy words.  (eg.   tokyo   -        japan        +        france       =   paris)',
                          3, 1, 6)
            self.putLabel('  ', 4, 0, 1)  # dummy space to keep balance of column 0
            Ent_wordA = tk.Entry(pw_right, width=10, justify='left')
            Ent_wordA.grid(row=4, column=2, columnspan=3, padx=10, sticky='w')
            Ent_wordB = tk.Entry(pw_right, width=10, justify='left')
            Ent_wordB.grid(row=4, column=2, columnspan=3, padx=10)
            Ent_wordC = tk.Entry(pw_right, width=10, justify='left')
            Ent_wordC.grid(row=4, column=2, columnspan=3, padx=10, sticky='e')
            self.putLabel('  ', 5, 0, 1)  # dummy space to keep balance of column 0
            self.putLabel('top k labels', 5, 1, 1)
            Ent_k = tk.Entry(pw_right, width=3, justify='right')
            Ent_k.insert(0, 10)
            Ent_k.grid(row=5, column=2, padx=10, sticky='w')

        Ypad = 292
        if command == 'predict_prob': Ypad += 6
        if command == 'nn': Ypad += 40
        if command == 'analogies': Ypad += 6
        tk.Button(pw_right, text='Run fasttext', command=lambda: testErrCheck(), width=12,
                  activebackground='coral', cursor='hand2',
                  bg=ini_sc_bgleft, fg='white').grid(row=16, column=0, columnspan=6, padx=277, pady=Ypad, sticky='w')
        tk.Button(pw_right, text='Quit', command=lambda: self.reset(), width=12,
                  activebackground='coral', cursor='hand2',
                  bg=ini_sc_bgleft, fg='white').grid(row=16, column=0, columnspan=6, padx=124, pady=Ypad, sticky='e')
        return


# ==================
#   Main Routine
# ==================
def main():
    global root, currentDir, ft_input, ft_model, modelSemaphore, winJP, \
        ini_sc_bgleft, ini_sc_bgright, ini_fi_logo, ini_fi_helpIcon, ini_fi_folderIcon, ini_fi_fthelp, \
        ini_fi_supervised, ini_fi_test_l, ini_fi_predict_p, ini_fi_skipgram, ini_fi_cbow, ini_fi_nn, \
        ini_fi_analogies, ini_fi_execFastTextPyw, ini_fi_ftini, ini_me_comList, ini_me_fontL, \
        ini_me_fontR, ini_me_helpFont

    config = configparser.ConfigParser()
    ini_file = 'config.ini'
    if not os.path.exists(ini_file):
        errMsg = 'INI file (./config.ini) not found.\nPlease reinstall winFastText from github.'
        messagebox.showerror('Error', errMsg)
        sys.exit()
    config.read(ini_file, encoding='utf-8')
    ini_sc_title = config.get('screen', 'ini_sc_title')
    ini_sc_bgleft = config.get('screen', 'ini_sc_bgleft')
    ini_sc_bgright = config.get('screen', 'ini_sc_bgright')
    ini_sc_location = config.get('screen', 'ini_sc_location')
    ini_fi_logo = config.get('file', 'ini_fi_logo')
    ini_fi_folderIcon = config.get('file', 'ini_fi_folderIcon')
    ini_fi_helpIcon = config.get('file', 'ini_fi_helpIcon')
    ini_fi_fthelp = config.get('file', 'ini_fi_fthelp')
    ini_fi_supervised = config.get('file', 'ini_fi_supervised')
    ini_fi_test_l = config.get('file', 'ini_fi_test_l')
    ini_fi_predict_p = config.get('file', 'ini_fi_predict_p')
    ini_fi_skipgram = config.get('file', 'ini_fi_skipgram')
    ini_fi_cbow = config.get('file', 'ini_fi_cbow')
    ini_fi_nn = config.get('file', 'ini_fi_nn')
    ini_fi_analogies = config.get('file', 'ini_fi_analogies')
    ini_fi_execFastTextPyw = config.get('file', 'ini_fi_execFastTextPyw')
    ini_fi_ftini = config.get('file', 'ini_fi_ftini')  # ini file for fasttext subprocess of supervised/skipgram/CBOW
                                                       # ini file for predict_prob/Nearest neighbors/analogies
    ini_me_comList = config.get('menu', 'ini_me_comList')
    ini_me_fontL = config.get('menu', 'ini_me_fontL')
    ini_me_fontR = config.get('menu', 'ini_me_fontR')
    ini_me_helpFont = config.get('menu', 'ini_me_helpFont')
    ft_model = ''  # initialize model file name
    ft_input = ''  # initialize train file name
    if not os.path.exists(ini_fi_ftini):
        currentDir = 'Click folder icon to select working directory.'  # initialize location of current directory.
    else:
        config.read(ini_fi_ftini, encoding='utf-8')
        ft_command = config.get('general', 'ft_command')
        currentDir = config.get('general', 'ft_currentDir')
        if ft_command == 'super' or ft_command == 'skip' or ft_command == 'cbow':
            ft_input = config.get(ft_command, 'Ent_input')
            ft_model = ''
        else:
            ft_input = ''
            ft_model = config.get(ft_command, 'Ent_model')
    modelSemaphore = 0  # semaphore for test_label, predict_prob, NN, and analogies
                        # 0 : exec load_model(), 0> : skip load_model()
    pcLang = wmi.WMI().Win32_OperatingSystem()[0].OSLanguage  # make sure the language of your Windows PC
    winJP = True if pcLang == 1041 else False  # 1041 is the Japanese language code of Windows
    root = tk.Tk()
    winft = winFastText(master=root)
    winft.master.title(ini_sc_title)
    winft.master.geometry(ini_sc_location)
    winft.mainloop()


if __name__ == '__main__':
    main()
