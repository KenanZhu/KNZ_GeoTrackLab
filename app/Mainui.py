import math
import threading
import time

import Trocor

from base64 import b64decode
from ctypes import *
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk

import tkinter.font as tkfont
import tkinter as tk
import matplotlib as mpl
import numpy as np

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

dll = cdll.LoadLibrary('./brdm2pos.dll')
dll.Start.restype = c_double
#
#
#
# Sat color
SatColor = ["#FF0000","#FFA500","#FFFF00","#00FF00","#00FFFF","#0000FF","#A020F0"]
# Color register part
enucolor    = ["#0080FF","#0080FF","#0080FF"]
enucolormid = ["#0080FF","#0080FF","#0080FF"]
enulinew    = [   "0.80",   "0.80",   "0.80"]
satncolor   = ["#0080FF"]
satncolormid= ["#0080FF"]
satnlinew   = [   "1.50"]
# Ion & tro register part
ioncormode = ['OFF', 'Ion-Free LC', 'Broadcast']
ioncorstate = 0
trocormode = ['OFF', 'Hopfield', 'Saastamoinen']
trocorstate = 0
#Sat system register part
satsysdict = {1: "G", 4:"R", 2:"C", 3:"E", 5:"S"}
satellite_system = 1
##Combox Count-er
ComboxObsCount = 0
ComboxNavCount = 0
ComboxOutCount = 0
#
#
#
def OptionsIN(hwnd):
    OPTGUI(hwnd)

def ExecutIN(hwnd):
    EXECUDUI(hwnd)

def ViewIN(hwnd):
    VIEWGUI(hwnd)

def Abo_windows():
    abo = tk.Toplevel(root)
    abo.title("About")
    abo.attributes('-toolwindow', 2)
    abo.geometry('200x100')
    abo.minsize(200, 100)
    abo.maxsize(200, 100)

    About = tk.Label(abo, text="\nKNZ_GeoTrackLab ver1.5.1\n\nCopyright (c) 2024 by KenanZhu\nAll Right Reserved.")
    About.pack(side=tk.TOP, expand=tk.YES)

class FUNCTION:

    @staticmethod
    def Colorchoose(i, label, mode):
        # Brief # choice to change the color of draw
        # Param # i : only for mode 1
        # Param # label : match the label with the button
        # Param # mode : color register type
        #               undo choice == 0 &
        #               middle choice store == 1 &
        #               final confirm == 3 &
        #               satn color == 4
        # Return# none
        global enucolor
        if mode == 0:
            enucolor = ["#0080FF", "#0080FF", "#0080FF"]
            satncolor[0] = "#0080FF"
            label.config(bg=enucolor[0])
        elif mode == 1:
            colorvalue = tk.colorchooser.askcolor()
            enucolormid[i] = str(colorvalue[1])
            label.config(bg=str(colorvalue[1]))
        elif mode == 3:
            enucolor[0] = enucolormid[0]
            enucolor[1] = enucolormid[1]
            enucolor[2] = enucolormid[2]
            satncolor[0] = satncolormid[0]
        elif mode == 4:
            colorvalue = tk.colorchooser.askcolor()
            satncolormid[0] = str(colorvalue[1])
            label.config(bg=str(colorvalue[1]))

    @staticmethod
    def Linewchoose(entry0, entry1, entry2, mode):
        # Brief # input to change the width of line
        # Param # entry0 : the entry box of e
        # Param # entry1 : the entry box of n
        # Param # entry2 : the entry box of u
        # Param # mode : width of line register type
        #               undo choice == 0 &
        #               final confirm == 1
        # Return# none

        global enulinew
        if mode == 0:
            enulinew = ["0.80", "0.80", "0.80"]
            entry0.set(enulinew[0])
            entry1.set(enulinew[1])
            entry2.set(enulinew[2])

        elif mode == 1:
            if (0 < float(entry0.get()) <= 5 and
                    0 < float(entry1.get()) <= 5 and
                    0 < float(entry2.get()) <= 5):

                enulinew[0] = entry0.get()
                enulinew[1] = entry1.get()
                enulinew[2] = entry2.get()
            elif (float(entry0.get()) <= 0 or
                  float(entry1.get()) <= 0 or
                  float(entry2.get()) <= 0):
                while not messagebox.showerror("ERROR !", "The line width value is invalid !"):
                    break
                enulinew = ["0.80", "0.80", "0.80"]
                entry0.set(enulinew[0])
                entry1.set(enulinew[1])
                entry2.set(enulinew[2])

            elif (5 < float(entry0.get()) or
                  5 < float(entry1.get()) or
                  5 < float(entry2.get())):
                msg = messagebox.askyesno("NOTICE", "The width of the line is too large\n"
                                                    "affecting the mapping.\n"
                                                    "Are you sure to continue ?")
                if not msg:
                    enulinew = ["0.80", "0.80", "0.80"]
                    entry0.set(enulinew[0])
                    entry1.set(enulinew[1])
                    entry2.set(enulinew[2])
                    pass
                elif msg:
                    enulinew[0] = entry0.get()
                    enulinew[1] = entry1.get()
                    enulinew[2] = entry2.get()

    def Calcu_confirm(self, v, cboxi, cboxt):
        # Brief # choice to change the ion & tro correction && confirm the sat system
        # Param # v sat system radio button value
        # Param # cboxi the combo box of ion correction
        # Param # cboxt the combo box of tro correction
        # Return# none
        global ioncorstate
        global trocorstate
        global satellite_system

        ioncorstate = self.Ion_and_Trocbox(cboxi, 0)
        trocorstate = self.Ion_and_Trocbox(cboxt, 1)
        satellite_system = self.Satsys_button(v)

        print(ioncorstate, trocorstate, satellite_system)

    @staticmethod
    def Satsys_button(v):
        # Brief # get the value of radio button of sat system
        # Param # v : the value of radio button
        # Return# the sat system code
        Systemdict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
        return int(Systemdict.get(v.get()))

    @staticmethod
    def Ion_and_Trocbox(cbox, cortype):
        # Brief # get the value of combo box
        # Param # cortype: correction type of
        #                            ion == 0 &
        #                            tro == 1
        # Param # cbox:
        # Return# ion | tro state code
        count = -1
        if cortype == 0:
            for ionmode in ioncormode:
                count += 1
                if cbox.get() == ionmode:
                    return count

        elif cortype == 1:
            for tromode in trocormode:
                count += 1
                if cbox.get() == tromode:
                    return count

    @staticmethod
    def GetObsFilePath(ObsFileSelectBox):
        global ComboxObsCount
        path = filedialog.askopenfilename(title='RINEX OBS File',
                                          filetypes=[('RINEX OBS File(*.o*.*.*obs.*.*d)', '*.*o;*.*obs;*.*d'),
                                                     ('All Files', '*.*')])
        if path and path not in ObsFileSelectBox['value']:
            ObsFileSelectBox['value'] += (path,)
            ComboxObsCount += 1
            ObsFileSelectBox.current(ComboxObsCount)

    @staticmethod
    def GetNavFilePath(NavFileSelectBox):
        global ComboxNavCount
        path = filedialog.askopenfilename(title='RINEX NAV File',
                                          filetypes=[('RINEX NAV File(*.*nav.*.hnav.*.gnav.*.qnav.*.*n.*.*g.*.*h.*.*q.*.*p)',
                                                      '*.*nav;*.hnav;*.gnav;*.qnav;*.*n;*.*g;*.*h;*.*q;*.*p'),
                                                     ('All Files', '*.*')])
        if path and path not in NavFileSelectBox['value']:
            NavFileSelectBox['value'] += (path,)
            ComboxNavCount += 1
            NavFileSelectBox.current(ComboxNavCount)

    @staticmethod
    def AskDirectory(AskDirectorySelectBox):
        global ComboxOutCount
        path = filedialog.askdirectory()
        if path and path not in AskDirectorySelectBox['value']:
            AskDirectorySelectBox['value'] += (path + "/*.sp",)
            ComboxOutCount += 1
            AskDirectorySelectBox.current(ComboxOutCount)

    @staticmethod
    def AskOrNotCheck(AskOrNotCheckVar,
                      AskDirectorySelectBox,
                      AskDirectorySelectButton):

        if AskOrNotCheckVar.get() == 0:
            AskDirectorySelectBox.config(state=tk.DISABLED)
            AskDirectorySelectButton.config(state=tk.DISABLED)
        else:
            AskDirectorySelectBox.config(state=tk.NORMAL)
            AskDirectorySelectButton.config(state=tk.NORMAL)

    def ExecuteFile(self,ExecuteState,
                    ObsSelectBoxVar,
                    NavSelectBoxVar,
                    AskOrNotCheckVar,
                    DirectorySelectBoxVar):
        obsfile = ""
        res_path = ""

        state3 = ["","",""]
        statemsg = ""
        if not ObsSelectBoxVar.get():
            state3[0] = "  obs file."
        if not NavSelectBoxVar.get():
            state3[1] = "  nav file."
        if not DirectorySelectBoxVar.get():
            if AskOrNotCheckVar.get():
                state3[2] = "  solution directory."
        for state in state3:
            statemsg += state
        if statemsg:
            ExecuteState.config(text='No file: %s !'%statemsg)
            return 0

        obs_path = ObsSelectBoxVar.get()
        nav_path = NavSelectBoxVar.get()
        DirectoryOut = DirectorySelectBoxVar.get()
        # Get the obs file name---------------------------#
        obspath = len(obs_path)
        while obspath > 0:
            flag = obs_path[obspath - 1:obspath]
            if flag == "/":
                obsfile = satsysdict.get(satellite_system) + "-" + obs_path[obspath:-4]
                break
            obspath -= 1
        # Get the file's father folder-------------------#
        if DirectoryOut:
            pathlon = len(DirectoryOut)
            while pathlon - 3 > 0:
                flag = DirectoryOut[pathlon - 3 - 1:pathlon - 3]
                if flag == "/":
                    res_path = DirectoryOut[:pathlon - 3] + obsfile + ".sp"
                    break
                pathlon -= 1
        else:
            res_path = obs_path[0:obspath] + obsfile + ".sp"
        # -----------------------------------------------#

        ExecuteState.config(text='Processing...... file : %s' % obs_path[obspath:])
        dll.Start(nav_path.encode(), obs_path.encode(), res_path.encode(), satellite_system)
        ExecuteState.config(text='Complete generate file : %s!' % obsfile + ".sp")

    def _ExecuteFile(self,ExecuteState,
                     ObsSelectBoxVar,
                     NavSelectBoxVar,
                     AskOrNotCheckVar,
                     DirectorySelectBoxVar):
        T = threading.Thread(target=lambda: self.ExecuteFile(ExecuteState,
                                                            ObsSelectBoxVar,
                                                            NavSelectBoxVar,
                                                            AskOrNotCheckVar,
                                                            DirectorySelectBoxVar))
        T.start()

class MAINGUI:
    def  __init__(self, hwnd):

        self.satvisb = None
        self.sattrack = None
        self.satn = None
        self.canvas2 = None
        self.canvas1 = None
        self.canvas0 = None
        self.ux = None
        self.nx = None
        self.ex = None
        self.plotstate = None
        self.initGUI(hwnd)

        self.Drawcards = tk.ttk.Notebook(hwnd)

        self.frmFigure0 = tk.Frame(hwnd)
        self.frmFigure0.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        self.frmFigure1 = tk.Frame(hwnd)
        self.frmFigure1.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        self.frmFigure2 = tk.Frame(hwnd)
        self.frmFigure2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        self.initTOPMENU(hwnd)

        self.initPLOT()

        self.Drawcards.add(self.frmFigure0, text='ENU-Draw')
        self.Drawcards.add(self.frmFigure1, text='Sat Number')
        self.Drawcards.add(self.frmFigure2, text='Sat Track')
        self.Drawcards.pack(fill=tk.BOTH, expand=True, padx='2px', pady='0px')

        hwnd.protocol("WM_DELETE_WINDOW", hwnd.quit)
        hwnd.mainloop()

    def initGUI(self, hwnd):
        hwnd.title("KNZ_GeoTrackLab ver1.5.1")
        hwnd.geometry('1200x700')
        hwnd.minsize(1200, 700)

        icon_img = (b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMS4xMTGQMDAwKgAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxMTE0MjIy7jMzM/8zMzPrMDAwLwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvLy8QMTExSAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAMTExNDIyMu4zMzP/MzMz/zMzM/8zMzPrMDAwLwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALy8vEDIyMsoyMjLKAAAAAAAAAAAAAAAAAAAAADExMTQyMjLuMzMz/zIy'
                    b'MvsxMTGaMjIy/TMzM/8zMzPrMTExLgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAyMjJRMjIy3TExMbgyMjLKMzMz/zIyMtkAAAAAMDAwOioqKgYAAAAAMTExszMzM/8yMjL7MDAwWQAAAAAxMTFhMjIy/TMz'
                    b'M/8zMzPrMTExLgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIyMt0zMzP/MzMz/zMz'
                    b'M/8zMzP/MTExrjExMU0yMjL4MTExsyoqKgYqKioMMjIyvzAwMFkAAAAAAAAAAAAAAAAxMTFhMjIy/TMzM/8zMzPrMTExLgAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTExuDMzM/8zMzP/MzMz/zMzM/8xMTGaMjIy+DMz'
                    b'M/8zMzP/MTExsyoqKgYAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAxMTFhMjIy/jMzM/8yMjLfAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAC8vLxAyMjLKMzMz/zMzM/8zMzP/MzMz9TIyMvkzMzP/MzMz/zMzM/8zMzP/MTExsyoq'
                    b'KgYAAAAAAAAAAAAAAAAAAAAAAAAAADExMY8zMzP/MzMz/zMzM8gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAvLy8QMjIyyjMzM/8zMzP/MzMz/zMzM/UyMjL+MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MTExsyoqKgYAAAAAAAAAAAAA'
                    b'AAAxMTGPMzMz/zMzM/8yMjLTMDAwFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMUgyMjLKMjIy2DEx'
                    b'Ma4xMTGaMjIy+TMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MTExsyoqKgYAAAAAMTExbDMzM/8zMzP/MjIy0zAw'
                    b'MBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTExTTIyMvgzMzP/MzMz/zMz'
                    b'M/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MTExsyoqKgYqKioMMzMzwzIyMtMwMDAVAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAwMDoyMjL4MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMz'
                    b'M/8zMzP/MzMz/zMzM/8zMzP/MTExsyoqKgYqKioMMDAwFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAKioqBjIyMrIzMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMz'
                    b'M/8zMzP/MTExsyoqKgYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAKioqBjIyMrIzMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MjIyfgAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTExNDExMbMqKioMKioqBjIy'
                    b'MrIzMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8xMTGUAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAwMDUyMjLvMzMz/zIyMsAAAAABKioqBjIyMrIzMzP/MzMz/zMz'
                    b'M/8zMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8zMzP/MjIy3i0tLRwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAwMDA1MjIy7zMzM/8yMjL7MDAwWQAAAAAAAAAAKioqBjIyMrIzMzP/MzMz/zMzM/8zMzP/MzMz/zMz'
                    b'M/8zMzP/MzMz/zIyMt4zMzMeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMDAwLzIy'
                    b'Mu8zMzP/MjIy+zAwMFkAAAAAAAAAAAAAAAAAAAAAKioqBjIyMrIzMzP/MzMz/zMzM/8zMzP/MzMz/zMzM/8yMjLeMzMzHgAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxMTGQMzMz/zMzM/8zMzObAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAKioqBjIyMrIzMzP/MzMz/zMzM/8zMzP/MjIy3jMzMx4AAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMSkzMzPrMzMz/zIyMv0xMTFiAAAAAAAAAAAAAAAAAAAAADEx'
                    b'MWwqKioMKioqBjIyMrIzMzP/MzMz/zIyMt4zMzMeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMS4zMzPrMzMz/zIyMv0xMTFiAAAAAAAAAAAxMTGQMzMz/zMzM8MqKioMKioqBjIy'
                    b'Mn4xMTGULy8vGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAADExMS4zMzPrMzMz/zIyMv0xMTFiMTExkDMzM/8zMzP/MjIy0zAwMBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADEx'
                    b'MS4zMzPrMzMz/zIyMv4zMzP/MzMz/zIyMtMwMDAVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMS4zMzPrMzMz/zMz'
                    b'M/8yMjLTMDAwFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADExMS4yMjLfMTExxzAwMBUAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////////////////////////'
                    b'/////////////////x////4P//58B//8eAP/4EhB/+AA4P/gAfD/wAHw/4AA4P+AAEH/8AAD/+AAB//gAA//8AAP/8AAD/+A'
                    b'AA//BgAf/g8AP/4fgH/+DwD//wYB//+AH///wD///+B////w//8=')

        icon_img = b64decode(icon_img)
        icon_img = ImageTk.PhotoImage(data=icon_img)
        hwnd.tk.call('wm', 'iconphoto', hwnd._w, icon_img)

        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=9)

        stateframe = tk.Frame(hwnd)
        stateframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.plotstate = ttk.Label(stateframe, text="None")
        self.plotstate.pack(side=tk.LEFT, anchor='w')

    def initTOPMENU(self, hwnd):

        topmenu = tk.Menu(hwnd)
        filemenu = tk.Menu(topmenu, tearoff=False)
        openmenu = tk.Menu(filemenu, tearoff=False)
        openmenu.add_command(label="Open Pos Solution",command=lambda :self.PO_openfile(hwnd), accelerator='Ctrl+S')
        openmenu.add_command(label="Open Sat Solution", command=lambda: self._SPP_calculat(hwnd), accelerator='Ctrl+S')
        openmenu.add_command(label="Open RINEX",command=lambda :ExecutIN(hwnd), accelerator='Ctrl+P')
        filemenu.add_cascade(label="Open...", menu=openmenu)
        filemenu.add_command(label="Clear", command=self.Clear_canvas)
        filemenu.add_command(label="View", command=lambda :ViewIN(hwnd))
        filemenu.add_command(label="Exit", command=hwnd.quit, accelerator='Ctrl+E')
        topmenu.add_cascade(label="File", menu=filemenu)

        optmenu = tk.Menu(topmenu, tearoff=False)
        optmenu.add_cascade(label="Options...",command=lambda :OptionsIN(hwnd))
        topmenu.add_cascade(label="Options", menu=optmenu)

        helpmenu = tk.Menu(topmenu, tearoff=False)
        helpmenu.add_command(label="About", command=Abo_windows)
        topmenu.add_cascade(label="Help", menu=helpmenu)

        hwnd.config(menu=topmenu)

    def initPLOT(self):
        # --------------------------------------------------------------------------------
        plt.rc('font', family='Segoe UI')
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        fig, (self.ex, self.nx, self.ux) = plt.subplots(3, 1, figsize=(10, 0), sharex=True)

        for spine in [ 'right', 'left']:
            self.ex.spines[spine].set_visible(False)
        self.ex.set_facecolor('#f5f5f5')

        for spine in [ 'right', 'left']:
            self.nx.spines[spine].set_visible(False)
        self.nx.set_facecolor('#f5f5f5')

        for spine in [ 'right', 'left']:
            self.ux.spines[spine].set_visible(False)
        self.ux.set_facecolor('#f5f5f5')

        fig.subplots_adjust(left=0, bottom=0.040, right=1, top=1, hspace=0.0)
        self.canvas0 = FigureCanvasTkAgg(fig, self.frmFigure0)
        self.canvas0.draw()
        self.canvas0.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        toolbar = NavigationToolbar2Tk(self.canvas0, self.frmFigure0, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.LEFT)

        # --------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------
        plt.rc('font', family='Segoe UI')
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        fig, (self.satn, self.satvisb) = plt.subplots(2, 1, figsize=(10, 0), sharex=True)
        fig.subplots_adjust(left=0, bottom=0.045, right=1, top=0.95, hspace=0.0)

        for spine in [ 'right', 'left']:
            self.satn.spines[spine].set_visible(False)
        self.satn.set_facecolor('#f5f5f5')

        for spine in [ 'right', 'left']:
            self.satvisb.spines[spine].set_visible(False)
        self.satvisb.set_facecolor('#f5f5f5')

        self.canvas1 = FigureCanvasTkAgg(fig, self.frmFigure1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        toolbar = NavigationToolbar2Tk(self.canvas1, self.frmFigure1, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.LEFT)

        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------
        plt.rc('font', family='Segoe UI')
        fig = plt.figure()
        self.sattrack = fig.add_subplot(projection='3d')
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

        for spine in ['right', 'left']:
            self.sattrack.spines[spine].set_visible(False)
        self.sattrack.set_facecolor('#f5f5f5')

        self.canvas2 = FigureCanvasTkAgg(fig, self.frmFigure2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        toolbar = NavigationToolbar2Tk(self.canvas2, self.frmFigure2, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.TOP, anchor='w')

    def Clear_canvas(self):
        # Brief # clear the canvas
        # Return# none
        self.ex.clear()
        self.nx.clear()
        self.ux.clear()
        self.satn.clear()
        self.satvisb.clear()
        self.sattrack.clear()
        self.canvas0.draw()
        self.canvas1.draw()
        self.canvas2.draw()
        self.plotstate.config(text="None")
        root.update()

    def PO_openfile(self, hwnd):
        # Brief # read the .po file & draw in the canvas
        # Return# none
        ENU_O = np.empty((3, 0))
        # Sat numbers register part
        satnumnarry = np.empty((1, 0))
        f_path = filedialog.askopenfilename(title='Pos Solution File',
                                            filetypes=[('Pos Solution File(*.po)', '*.po'),
                                                       ('All Files', '*.*')])
        if not f_path.find(".po") >= 0:
            self.plotstate.config(text="Error !: format is invalid.")
            hwnd.update()
            return
        with open(f_path, 'r') as f:
            while 1:
                line = f.readline()
                if line.find("X-rec") >= 0:
                    self.plotstate.config(text="Reading...")
                    hwnd.update()
                    while 1:
                        line = f.readline()
                        if line != "" and line[1:2] != "-":
                            E = float(line[45 + 22:55 + 22])
                            N = float(line[56 + 22:66 + 22])
                            U = float(line[67 + 22:77 + 22])
                            satnum = int(line[64:67])

                            ENU_O = np.hstack((ENU_O, [[E], [N], [U]]))
                            satnumnarry = np.hstack((satnumnarry, [[satnum]]))
                        if line[1:2] == "-":
                            ENU_O = np.hstack((ENU_O, [[0], [0], [0]]))
                            satnumnarry = np.hstack((satnumnarry, [[0]]))
                        if line == "":
                            self.ex.clear()
                            self.nx.clear()
                            self.ux.clear()
                            self.ex.plot(ENU_O[0, :], color=enucolor[0], linewidth=enulinew[0], marker='.', linestyle=':',
                                    ms=enulinew[0])
                            self.ex.set_title(' E-W(m)', x=0.02, y=0, fontsize=8)
                            self.ex.grid(True, linestyle='--', alpha=0.7)
                            self.nx.plot(ENU_O[1, :], color=enucolor[1], linewidth=enulinew[1], marker='.', linestyle=':',
                                    ms=enulinew[1])
                            self.nx.set_title(' N-S(m)', x=0.02, y=0, fontsize=8)
                            self.nx.grid(True, linestyle='--', alpha=0.7)
                            self.ux.plot(ENU_O[2, :], color=enucolor[2], linewidth=enulinew[2], marker='.', linestyle=':',
                                    ms=enulinew[2])
                            self.ux.set_title(' U-D(m)', x=0.02, y=0, fontsize=8)
                            self.ux.grid(True, linestyle='--', alpha=0.7)
                            self.canvas0.draw()

                            self.satn.clear()
                            self.satn.plot(satnumnarry[0, :], marker='_', linestyle=None, color=satncolor[0], linewidth=0)
                            self.satn.set_title('Valid Sat Numbers', loc='left', fontsize=8)
                            self.satn.set_xlabel('Epochs')
                            self.satn.grid(True, linestyle='--', alpha=0.7)
                            self.canvas1.draw()
                            break
                elif line == "":
                    self.plotstate.config(text="Plot   form: %s" % f_path)
                    break

    def SPP_calculat(self, hwnd):
        # Brief # read .sp file & draw in the canvas & output the .po file
        # Return# none

        # Const define
        self.sattrack.clear()
        C_V = 299792458
        f1 = 1575.42
        f2 = 1227.60

        match satsysdict.get(satellite_system):
            case 'G':
                f1 = 1575.42
                f2 = 1227.60
            case 'E':
                f1 = 1575.42
                f2 = 1278.75
            case 'C':
                f1 = 1561.098
                f2 = 1207.140

        ENU_O = np.empty((3, 0))
        GDOP = np.empty((1, 0))
        # Sat numbers register part
        satnumnarry = np.empty((1, 0))
        res_path = filedialog.askopenfilename(title='Sat Solution File',
                                              filetypes=[('Sat Solution File(*.sp)', '*.sp'),
                                                         ('All Files', '*.*')])
        if not res_path.find(".sp") >= 0:
            self.plotstate.config(text="Error !:  format is invalid.")
            hwnd.update()
            return
        with open(res_path, 'r') as f:
            while 1:
                line = f.readline()
                if line.find("APPROX POSITION XYZ") >= 0:
                    apX = float(line[23:35])
                    apY = float(line[36:48])
                    apZ = float(line[49:61])
                elif line.find("APPROX POSITION BLH") >= 0:
                    apB = float(line[23:35])
                    apL = float(line[36:48])
                    apH = float(line[49:61])
                elif line.find("OBS FILE PATH") >= 0:
                    Obs = line[23:300]
                elif line.find("NAV FILE PATH") >= 0:
                    pass
                elif line.find("END OF HEADER") >= 0:
                    break
            # Get the obs file name---------------------------#
            obspath = len(Obs)
            while obspath > 0:
                flag = Obs[obspath - 1:obspath]
                if flag == "/":
                    obsfile = satsysdict.get(satellite_system) + "-" + Obs[obspath:-4]
                    break
                obspath -= 1
            # Get the file's father folder-------------------#
            pathlon = len(res_path)
            while pathlon - 3 > 0:
                flag = res_path[pathlon - 3 - 1:pathlon - 3]
                if flag == "/":
                    o_path = res_path[:pathlon - 3] + obsfile + "po"
                    break
                pathlon -= 1
            # -----------------------------------------------#

            # Generate the data header-----------------------#
            with open(o_path, 'w+') as of:  # Initialize-------#
                of.close()
            of = open(o_path, 'a+')
            print("@ GENERATE PROGRAM   : KNZ_SN Visual Lab v1.5.1\n"
                  "@ GENERATE TYPE      : Receiver Station Position\n"
                  "@ GENERATE TIME      : %s\n"
                  "@ GENERATE SYS       : %s\n"
                  "@ IONOS OPT          : %s\n"
                  "@ TROPO OPT          : %s\n"
                  "@\n\n" % (time.asctime(time.localtime())
                             , satsysdict.get(satellite_system)
                             , ioncormode[ioncorstate]
                             , trocormode[trocorstate]), file=of)
            print(
                "GPST                     X-rec(m)     Y-rec(m)      Z-rec(m)   Sn(n)   dE(m)      dN(m)      dU(m)     ",
                file=of)

            # Coordinate transformation matrix---------------#
            S = np.array([
                [-math.sin(apL), math.cos(apL), 0],
                [-math.sin(apB) * math.cos(apL), -math.sin(apB) * math.sin(apL), math.cos(apB)],
                [math.cos(apB) * math.cos(apL), math.cos(apB) * math.sin(apL), math.sin(apB)]
            ])
            # -----------------------------------------------#
            self.plotstate.config(text="Reading...")
            hwnd.update()

            global epoch_last
            epoch_last = 0
            while 1:
                line = f.readline()
                if line == "":
                    break
                flag = line[0: 1]
                if flag == ">":
                    satnum = 0
                    sPRN = []
                    satX = np.empty((1, 0))
                    satY = np.empty((1, 0))
                    satZ = np.empty((1, 0))
                    C1 = np.empty((1, 0))
                    C2 = np.empty((1, 0))
                    ma = np.empty((1, 0))
                    np.empty((1, 0))
                    Dt = np.empty((1, 0))

                    year = int(line[6:10])
                    month = int(line[11:13])
                    day = int(line[14:16])
                    hour = int(line[17:19])
                    min = int(line[20:22])
                    sec = float(line[23:30])
                    epoch = int(line[2:6])

                    count = 0
                    # Check the lost epoch
                    while count < epoch - epoch_last - 1:
                        ENU_O = np.hstack((ENU_O, [[0], [0], [0]]))
                        satnumnarry = np.hstack((satnumnarry, [[0]]))
                        print("------------ MISSING EPOCH DATA", file=of)
                        count += 1
                    epoch_last = epoch
                    # Calculate start
                    while 1:
                        line = f.readline()
                        if line == "\n":
                            
                            # The sampling rate of 3D draw  
                            if epoch % 15 == 0:
                                self.sattrack.scatter(satX[0,:], satY[0,:], satZ[0,:], s=5, zdir='z', c=SatColor[6] )

                            # Get the viald satellite number
                            satnumnarry = np.hstack((satnumnarry, [[satnum]]))

                            match satsysdict.get(satellite_system):
                                case 'G':
                                    MINSAT = 4
                                case 'E':
                                    MINSAT = 4
                                case 'R':
                                    MINSAT = 5
                                case 'C':
                                    MINSAT = 4

                            if satnum >= MINSAT:
                                stop = 0
                                Qtrace = 0
                                X = ap_X = apX
                                Y = ap_Y = apY
                                Z = ap_Z = apZ
                                while math.fabs(ap_X - X) > 1.0e-7 or ap_X == X:
                                    stop += 1
                                    if stop >= 4:
                                        break
                                    count = 0
                                    ap_X = X
                                    ap_Y = Y
                                    ap_Z = Z
                                    Ptem = []
                                    B = np.empty((0, 4))
                                    L = np.empty((0, 1))
                                    while 1:
                                        # Linear the observation equation
                                        R = math.sqrt(
                                            pow((satX[0, count] - ap_X), 2) + pow((satY[0, count] - ap_Y), 2) + pow(
                                                (satZ[0, count] - ap_Z), 2))
                                        l = -((satX[0, count] - ap_X) / R)
                                        m = -((satY[0, count] - ap_Y) / R)
                                        n = -((satZ[0, count] - ap_Z) / R)
                                        B = np.vstack((B, [l, m, n, 1]))
                                        Ptem.append(pow(math.sin(math.radians(ma[0, count])), 2))
                                        Pl = 0
                                        # Get the tropsphere correction
                                        match trocorstate:
                                            case 0:
                                                Tro = 0
                                            case 1:
                                                Tro = Trocor.Hop_tro_cor(apH, ma[0, count])
                                            case 2:
                                                Tro = Trocor.Sas_tro_cor(apB, apH, ma[0, count])
                                                pass
                                        # Get the ionsphere correction
                                        match ioncorstate:
                                            case 0:
                                                if C1[0, count] == 0 and C2[0, count] != 0:
                                                    Pl = C2[0, count]

                                                elif C1[0, count] != 0 and C2[0, count] == 0:
                                                    Pl = C1[0, count]
                                            case 1:
                                                if C2[0, count] != 0 and C1[0, count] != 0:
                                                    Pl = (f1 * f1 * C1[0, count]) / (f1 * f1 - f2 * f2) - (
                                                            f2 * f2 * C2[0, count]) / (f1 * f1 - f2 * f2)

                                                elif C1[0, count] == 0 and C2[0, count] != 0:
                                                    Pl = C2[0, count]

                                                elif C1[0, count] != 0 and C2[0, count] == 0:
                                                    Pl = C1[0, count]
                                            case 2:
                                                pass
                                        # Omc matrix
                                        L = np.vstack(
                                            ( L, [Pl - R + C_V * Dt[0, count] - Tro] )
                                        )

                                        count += 1
                                        if count == satnum:
                                            break
                                    
                                    # Construct the Least Squares
                                    P = np.diag(Ptem)
                                    BTP = np.dot(np.transpose(B), P)
                                    BTPB = np.dot(BTP, B)
                                    Q = np.linalg.inv(BTPB)
                                    Qtrace = np.trace(Q)
                                    D_X = np.dot(np.dot(np.dot(Q, np.transpose(B)), P), L)  # Coordinate correction
                                    X = D_X[0, 0] + ap_X
                                    Y = D_X[1, 0] + ap_Y
                                    Z = D_X[2, 0] + ap_Z

                                DeltaXYZ = np.array([[X - apX], [Y - apY], [Z - apZ]])
                                ENU = S @ DeltaXYZ
                                #if math.fabs(ENU[0, 0]) > 25 or math.fabs(ENU[1, 0]) > 25 or math.fabs(ENU[2, 0]) > 50:
                                #   ENU_O = np.hstack((ENU_O, [[0], [0], [0]]))
                                #   print("------------ ANOMALY RESOLUTION", file=of)
                                #else:

                                ENU_O = np.hstack((ENU_O, [[ENU[0, 0]], [ENU[1, 0]], [ENU[2, 0]]]))
                                GDOP = np.hstack((GDOP, [ [math.sqrt(Qtrace)] ]))

                                print(
                                        "%4d\\%02d\\%02d\\%02d\\%02d\\%04.1f %12.4f %12.4f %12.4f %3d %10.5f %10.5f %10.5f"
                                        % (year, month, day, hour, min, sec, X, Y, Z, satnum,
                                           float(ENU[0, 0]),
                                           float(ENU[1, 0]),
                                           float(ENU[2, 0]) ), file=of)
                                break
                            else:
                                break

                        flag = line[0:1]
                        if flag == satsysdict.get(satellite_system):
                            satnum += 1
                            sPRN.append(int(line[2:4]))
                            satX = np.hstack((satX, [[float(line[6:21])]]))
                            satY = np.hstack((satY, [[float(line[22:37])]]))
                            satZ = np.hstack((satZ, [[float(line[38:53])]]))
                            C1   = np.hstack((C1,   [[float(line[55:69])]]))
                            C2   = np.hstack((C2,   [[float(line[71:85])]]))
                            ma   = np.hstack((ma,   [[float(line[86:101])]]))
                            Dt   = np.hstack((Dt,   [[float(line[102:118])]]))

                elif line.find("END") >= 0:
                    self.ex.clear()
                    self.nx.clear()
                    self.ux.clear()

                    self.ex.plot(ENU_O[0, :], color=enucolor[0], linewidth=enulinew[0], marker='.', linestyle=':',
                            ms=enulinew[0])
                    self.ex.plot( GDOP[0, :], color='#808080', alpha=0.5, linewidth=enulinew[0], marker='.', linestyle=':',
                            ms=enulinew[0])
                    self.ex.set_title(' E-W(m)', x=0.02, y=0, fontsize=8)
                    self.ex.grid(True, linestyle='--', alpha=0.7)

                    self.nx.plot(ENU_O[1, :], color=enucolor[1], linewidth=enulinew[1], marker='.', linestyle=':',
                            ms=enulinew[1])
                    self.nx.set_title(' N-S(m)', x=0.02, y=0, fontsize=8)
                    self.nx.grid(True, linestyle='--', alpha=0.7)

                    self.ux.plot(ENU_O[2, :], color=enucolor[2], linewidth=enulinew[2], marker='.', linestyle=':',
                            ms=enulinew[2])
                    self.ux.set_title(' U-D(m)', x=0.02, y=0, fontsize=8)
                    self.ux.grid(True, linestyle='--', alpha=0.7)

                    self.canvas0.draw()

                    self.satn.clear()
                    self.satn.plot(satnumnarry[0, :], marker='_', ms=10, linestyle=None, color=satncolor[0], linewidth=0)
                    self.satn.set_title('Valid Satellite Numbers',loc='left', fontsize=8)
                    self.satn.set_xlabel('Epochs')
                    self.satn.grid(True, linestyle='--', alpha=0.7)
                    self.canvas1.draw()
                    self.canvas2.draw()

                    f.close()
                    self.plotstate.config(text="Plot   form: %s" % res_path)
                    break

    def _SPP_calculat(self, hwnd: object) -> object:
        T = threading.Thread(target=lambda :self.SPP_calculat(hwnd))
        T.start()

class OPTGUI:
    def __init__(self,hwnd):

        self.ulinewidth = None
        self.nlinewidth = None
        self.elinewidth = None
        self.Main2Frame0 = None
        self.v = None
        self.ctrobox = None
        self.cionbox = None
        self.Main1Frame0 = None
        self.opthwnd = None

        self.initGUI(hwnd)

        self.Cmd = FUNCTION()

    def initGUI(self,hwnd):
        self.opthwnd = tk.Toplevel(hwnd)
        self.opthwnd.title("Options")
        self.opthwnd.resizable(0, 0)
        self.opthwnd.geometry('320x250')
        self.opthwnd.minsize(320, 250)
        self.opthwnd.maxsize(320, 250)

        icon_img2 = (b'AAABAAEAICAAAAAAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAADjsAAA47AAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'ABAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAACQAAABIAAAASAAAACQAAAAAAAAACAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAABwAAAJAAAADqAAAA7gAAAO4AAADqAAAAk'
                     b'QAAAAcAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAACQAAAA/wAAAPw'
                     b'AAAD/AAAA/wAAAPwAAAD/AAAAkAAAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAQAAAADAAAAAQAAAAEAAAAAA'
                     b'AAACwAAAOMAAAD/AAAA/AAAAP4AAAD+AAAA/AAAAP8AAADjAAAACgAAAAAAAAABAAAAAQAAAAMA'
                     b'AAAEAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAABAAAAAAA'
                     b'AAAAAAAABAAAABQAAAAAAAAATAAAA7QAAAP8AAAD+AAAA/wAAAP8AAAD+AAAA/wAAAO0AAAATAA'
                     b'AAAAAAAAUAAAABAAAAAAAAAAAAAAABAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AABAAAAAAAAABEAAABTAAAAUQAAAA8AAAAAAAAAAAAAAEQAAAD/AAAA/gAAAP8AAAD/AAAA/wAA'
                     b'AP8AAAD+AAAA/wAAAEQAAAAAAAAAAAAAAA8AAABRAAAAUwAAABEAAAAAAAAAAQAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAgAAAAAAAAAwAAAA5QAAAP8AAAD/AAAA4QAAAHYAAAB2AAAA6QAAAP8AAA'
                     b'D+AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA6QAAAHYAAAB1AAAA4QAAAP8AAAD/AAAA5QAAA'
                     b'DAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAwAAAMoAAAD/AAAA+gAAAPwAAAD/AAAA'
                     b'/wAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/gAAAP4AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAP8AAAD'
                     b'/AAAA/AAAAPoAAAD/AAAAywAAAAMAAAAAAAAAAQAAAAAAAAAAAAAAAwAAAAAAAABrAAAA/wAAAP'
                     b'oAAAD/AAAA/wAAAP0AAAD7AAAA+wAAAP4AAAD/AAAA/AAAAP0AAAD/AAAA/wAAAP0AAAD8AAAA/'
                     b'wAAAP4AAAD7AAAA+wAAAP0AAAD/AAAA/wAAAPoAAAD/AAAAawAAAAAAAAADAAAAAAAAAAEAAAAA'
                     b'AAAAAwAAANUAAAD/AAAA/QAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA/wAAAPI'
                     b'AAADyAAAA/wAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8AAADVAAAAAw'
                     b'AAAAAAAAABAAAAAQAAAAAAAAATAAAA7AAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9A'
                     b'AAA/wAAAK8AAAA8AAAAFQAAABUAAAA8AAAArgAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8A'
                     b'AAD+AAAA/wAAAOwAAAATAAAAAAAAAAEAAAAAAAAAAQAAAAAAAADBAAAA/wAAAPoAAAD/AAAA/wA'
                     b'AAP8AAAD/AAAA/QAAAP8AAAB3AAAAAAAAAAIAAAAAAAAAAAAAAAIAAAAAAAAAdwAAAP8AAAD9AA'
                     b'AA/wAAAP8AAAD/AAAA/wAAAPoAAAD/AAAAwQAAAAAAAAABAAAAAAAAAAAAAAACAAAAAAAAADEAA'
                     b'ADmAAAA/wAAAP0AAAD/AAAA/wAAAPwAAAD/AAAAqwAAAAAAAAAEAAAAAwAAAAEAAAABAAAABAAA'
                     b'AAQAAAAAAAAArAAAAP8AAAD8AAAA/wAAAP8AAAD9AAAA/wAAAOYAAAAwAAAAAAAAAAIAAAAAAAA'
                     b'AAAAAAAAAAAABAAAAAAAAAA0AAACuAAAA/wAAAP0AAAD/AAAA/QAAAP8AAABCAAAAAAAAAAMAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAABCAAAA/wAAAP0AAAD/AAAA/QAAAP8AAACvAAAADQAAA'
                     b'AAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAACAAAAD4AAAA/wAAAP0AAAD/AAAA'
                     b'8gAAABgAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAABgAAADyAAAA/wAAAP0AAAD'
                     b'/AAAA+AAAACAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAIAAAAP'
                     b'gAAAD/AAAA/QAAAP8AAADyAAAAGAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAG'
                     b'AAAAPIAAAD/AAAA/QAAAP8AAAD4AAAAIAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB'
                     b'AAAAAAAAAA0AAACuAAAA/wAAAP0AAAD/AAAA/QAAAP8AAABCAAAAAAAAAAMAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAwAAAAAAAABCAAAA/wAAAP0AAAD/AAAA/QAAAP8AAACuAAAADQAAAAAAAAABAAAAAA'
                     b'AAAAAAAAAAAAAAAgAAAAAAAAAxAAAA5gAAAP8AAAD9AAAA/wAAAP8AAAD8AAAA/wAAAKsAAAAAA'
                     b'AAABAAAAAMAAAABAAAAAQAAAAMAAAAEAAAAAAAAAKsAAAD/AAAA/AAAAP8AAAD/AAAA/QAAAP8A'
                     b'AADmAAAAMAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAMEAAAD/AAAA+gAAAP8AAAD/AAAA/wA'
                     b'AAP8AAAD9AAAA/wAAAHcAAAAAAAAAAgAAAAAAAAAAAAAAAgAAAAAAAAB3AAAA/wAAAP0AAAD/AA'
                     b'AA/wAAAP8AAAD/AAAA+gAAAP8AAADBAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAATAAAA7AAAAP8AA'
                     b'AD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAAK4AAAA8AAAAFQAAABUAAAA8AAAArgAA'
                     b'AP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAOwAAAATAAAAAAAAAAEAAAABAAA'
                     b'AAAAAAAMAAADWAAAA/wAAAP0AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAAP8AAA'
                     b'DyAAAA8gAAAP8AAAD/AAAA/QAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA1QAAA'
                     b'AMAAAAAAAAAAQAAAAAAAAADAAAAAAAAAGsAAAD/AAAA+gAAAP8AAAD/AAAA/QAAAPsAAAD7AAAA'
                     b'/gAAAP8AAAD8AAAA/QAAAP8AAAD/AAAA/QAAAPwAAAD/AAAA/gAAAPsAAAD7AAAA/QAAAP8AAAD'
                     b'/AAAA+gAAAP8AAABrAAAAAAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAAAwAAAMsAAAD/AAAA+gAAAP'
                     b'wAAAD/AAAA/wAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/gAAAP4AAAD/AAAA/wAAAP8AAAD+AAAA/'
                     b'wAAAP8AAAD/AAAA/AAAAPoAAAD/AAAAywAAAAMAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAIAAAAA'
                     b'AAAAMQAAAOYAAAD/AAAA/wAAAOEAAAB2AAAAdgAAAOkAAAD/AAAA/gAAAP8AAAD/AAAA/wAAAP8'
                     b'AAAD+AAAA/wAAAOkAAAB2AAAAdgAAAOEAAAD/AAAA/wAAAOYAAAAxAAAAAAAAAAIAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEQAAAFQAAABRAAAADwAAAAAAAAAAAAAARAAAAP8AAAD+A'
                     b'AAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAARAAAAAAAAAAAAAAADwAAAFEAAABUAAAAEQAAAAAA'
                     b'AAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAABAAAAAAAAAAAAAAABAAAABQA'
                     b'AAAAAAAATAAAA7QAAAP8AAAD+AAAA/wAAAP8AAAD+AAAA/wAAAO0AAAATAAAAAAAAAAUAAAABAA'
                     b'AAAAAAAAAAAAABAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAA'
                     b'AAEAAAABAAAAAEAAAABAAAAAAAAAAsAAADjAAAA/wAAAPwAAAD+AAAA/gAAAPwAAAD/AAAA4wAA'
                     b'AAoAAAAAAAAAAQAAAAEAAAAEAAAABAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAJAAAAD/AAAA/AAAAP8AAA'
                     b'D/AAAA/AAAAP8AAACQAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAA'
                     b'BwAAAJAAAADqAAAA7gAAAO4AAADqAAAAkQAAAAcAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAkAAAASAAAAEgAAAAoAAAAAAAAAAgAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAM'
                     b'AAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/9GL//'
                     b'+kJf//kAn//5AJ/+ggBBfTIATLqCAEFZAAAAkgAAAEIAAABEAAAAJAAAACIAQgBKAIEAVQClAKq'
                     b'AmQFagJkBVQClAKoAgQBSAEIARAAAACQAAAAiAAAAQgAAAEkAAACaggBBXTIATL6CAEF/+QCf//'
                     b'kAn//6Ql///Ri/8=')

        icon_img2 = b64decode(icon_img2)
        icon_img2 = ImageTk.PhotoImage(data=icon_img2)
        self.opthwnd.tk.call('wm', 'iconphoto', self.opthwnd._w, icon_img2)

        Optionscards = tk.ttk.Notebook(self.opthwnd)

        self.initCARDCALCU()
        self.initCARDDRAW()

        Optionscards.add(self.Main1Frame0, text='Calc options')
        Optionscards.add(self.Main2Frame0, text='Draw options')
        Optionscards.pack(fill=tk.BOTH, expand=True, padx='2px', pady='0px')

        self.initCONFIRM()

    def initCARDCALCU(self):
        self.Main1Frame0 = tk.Frame(self.opthwnd)

        # ION correction#
        TOP1Frame0 = ttk.Frame(self.Main1Frame0)
        TOP1Frame0.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        ioncor = ttk.Label(TOP1Frame0, text='Ionosphere Correction')
        ioncor.pack(side=tk.LEFT, anchor='w', padx='1px')

        self.cionbox = ttk.Combobox(TOP1Frame0, width=15, height=4)
        self.cionbox['state'] = 'readonly'
        self.cionbox['value'] = ('OFF', 'Ion-Free LC', 'Broadcast')
        self.cionbox.current(ioncorstate)
        self.cionbox.pack(side=tk.RIGHT, anchor='e')

        # TRO correction#
        TOP2Frame0 = ttk.Frame(self.Main1Frame0)
        TOP2Frame0.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        ioncor = ttk.Label(TOP2Frame0, text='Troposphere Correction')
        ioncor.pack(side=tk.LEFT, anchor='w', padx='1px')

        self.ctrobox = ttk.Combobox(TOP2Frame0, width=15, height=4)
        self.ctrobox['state'] = 'readonly'
        self.ctrobox['value'] = ('OFF', 'Hopfield', 'Saastamoinen')
        self.ctrobox.current(trocorstate)
        self.ctrobox.pack(side=tk.RIGHT, anchor='e')

        # GNSS Options#
        TOP5Frame0 = ttk.LabelFrame(self.Main1Frame0, text='Satellite system', labelanchor='nw')
        TOP5Frame0.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        satsys = [("GPS", 1), ("GLO", 4), ("BeiDou", 2), ("Galileo", 3), ("SBAS", 5)]
        self.v = tk.IntVar()

        for sys, num in satsys:
            radio_button = ttk.Radiobutton(TOP5Frame0, text=sys, variable=self.v, value=num)
            radio_button.pack(side=tk.LEFT, padx='3px', anchor='w')

        self.v.set(satellite_system)

    def initCARDDRAW(self):

        self.Main2Frame0 = tk.Frame(self.opthwnd)

        self.initDRAWCOLOR()
        self.initDRAWLINE()

    def initDRAWLINE(self):
        # Line's weight options#
        Right2Frame1 = ttk.LabelFrame(self.Main2Frame0, text='Draw configs', labelanchor='nw')
        Right2Frame1.pack(side=tk.RIGHT, expand=tk.YES, padx='1px', pady='1px', fill=tk.Y)

        EFrameR2 = tk.Frame(Right2Frame1)
        EFrameR2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        elinewopt = tk.Label(EFrameR2, text='Eline:', width=5, height=1)
        elinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.elinewidth = ttk.Spinbox(EFrameR2, from_=0, to=10, increment=0.01, width=10)
        self.elinewidth.set(enulinew[0])
        self.elinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        NFrameR2 = tk.Frame(Right2Frame1)
        NFrameR2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        nlinewopt = tk.Label(NFrameR2, text='Nline:', width=5, height=1)
        nlinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.nlinewidth = ttk.Spinbox(NFrameR2, from_=0, to=10, increment=0.01, width=10)
        self.nlinewidth.set(enulinew[1])
        self.nlinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        UFrameR2 = tk.Frame(Right2Frame1)
        UFrameR2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ulinewopt = tk.Label(UFrameR2, text='Uline:', width=5, height=1)
        ulinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.ulinewidth = ttk.Spinbox(UFrameR2, from_=0, to=10, increment=0.01, width=10)
        self.ulinewidth.set(enulinew[2])
        self.ulinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        LineConR2 = tk.Frame(Right2Frame1)
        LineConR2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        linewre = ttk.Button(LineConR2, text='Undo', width=10,
                             command=lambda: self.Cmd.Linewchoose(self.elinewidth,
                                                                  self.nlinewidth,
                                                                  self.ulinewidth, 0))
        linewre.pack(side=tk.LEFT, expand=tk.YES, padx='1px')

    def initDRAWCOLOR(self):

        # Satnum plot options#
        Buttom1Frame1 = ttk.LabelFrame(self.Main2Frame0, text='Satn configs', labelanchor='nw')
        Buttom1Frame1.pack(side=tk.BOTTOM, expand=tk.YES, padx='1px', pady='1px', fill=tk.BOTH)

        SatnFrameB1 = tk.Frame(Buttom1Frame1)
        SatnFrameB1.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        satncolopt = ttk.Button(SatnFrameB1, text='Satn Color', width=10,
                                command=lambda: self.Cmd.Colorchoose(0, satncollab, 4))
        satncolopt.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        satncollab = tk.Label(SatnFrameB1, width=5, height=1, bg=satncolormid[0])
        satncollab.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

        LineConB1 = tk.Frame(Buttom1Frame1)
        LineConB1.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        linewre = ttk.Button(LineConB1, text='Undo', width=10,
                             command=lambda: self.Cmd.Colorchoose(0, satncollab, 0))
        linewre.pack(side=tk.LEFT, expand=tk.YES, padx='1px')

        # Line's colors options#
        Left2Frame1 = ttk.LabelFrame(self.Main2Frame0, text='ENU colors', labelanchor='nw')
        Left2Frame1.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='1px', fill=tk.Y)

        EFrameL2 = tk.Frame(Left2Frame1)
        EFrameL2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ecolopt = ttk.Button(EFrameL2, text='E Color', width=10,
                             command=lambda: self.Cmd.Colorchoose(0, ecollab, 1))
        ecolopt.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        ecollab = tk.Label(EFrameL2, width=5, height=1, bg=enucolor[0])
        ecollab.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

        NFrameL2 = tk.Frame(Left2Frame1)
        NFrameL2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ncolopt = ttk.Button(NFrameL2, text='N Color', width=10,
                             command=lambda: self.Cmd.Colorchoose(1, ncollab, 1))
        ncolopt.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        ncollab = tk.Label(NFrameL2, width=5, height=1, bg=enucolor[1])
        ncollab.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

        UFrameL2 = tk.Frame(Left2Frame1)
        UFrameL2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ucolopt = ttk.Button(UFrameL2, text='U Color', width=10,
                             command=lambda: self.Cmd.Colorchoose(2, ucollab, 1))
        ucolopt.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        ucollab = tk.Label(UFrameL2, width=5, height=1, bg=enucolor[2])
        ucollab.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

        ColorConL2 = tk.Frame(Left2Frame1)
        ColorConL2.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        colorcon = ttk.Button(ColorConL2, text='Undo', width=10,
                              command=lambda: [self.Cmd.Colorchoose(0, ecollab, 0)
                                  , self.Cmd.Colorchoose(0, ncollab, 0)
                                  , self.Cmd.Colorchoose(0, ucollab, 0)])
        colorcon.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

    def initCONFIRM(self):
        # TOTAL Confirm#
        Bottom0Frame0 = ttk.Frame(self.opthwnd)
        Bottom0Frame0.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.Y)
        TotalCancel = ttk.Button(Bottom0Frame0, text='Cancel', width=10,
                                 command=lambda: [self.opthwnd.destroy()])
        TotalCancel.pack(side=tk.RIGHT, padx='1px', anchor='e')
        TotalCon = ttk.Button(Bottom0Frame0, text='Confirm', width=10,
                              command=lambda: [self.Cmd.Colorchoose(0, None, 3),
                                               self.Cmd.Linewchoose(self.elinewidth,
                                                                    self.nlinewidth,
                                                                    self.ulinewidth, 1),
                                               self.Cmd.Calcu_confirm(self.v, self.cionbox, self.ctrobox),
                                               self.opthwnd.destroy()])
        TotalCon.pack(side=tk.RIGHT, padx='1px', anchor='e')

class EXECUDUI:
    def __init__(self,hwnd):
        self.exehwnd = None
        self.initGUI(hwnd)
        ##Combox Var
        self.ObsSelectBoxVar = tk.StringVar()
        self.NavSelectBoxVar = tk.StringVar()
        self.DirectorySelectBoxVar = tk.StringVar()
        ##CheckButton Var
        self.AskOrNotCheckButtonVar = tk.IntVar()

        self.initIO()

        self.Cmd = FUNCTION()

    def initGUI(self,hwnd):
        self.exehwnd = tk.Toplevel(hwnd)
        self.exehwnd.title("RINEX Processor")
        self.exehwnd.resizable(0, 0)
        self.exehwnd.geometry('400x215')
        self.exehwnd.minsize(400, 215)
        self.exehwnd.maxsize(400, 215)

        global icon_img3
        icon_img3 = (b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAADjsAAA47AAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAAAEAAAAAQ'
                     b'AAAAAAAAAAAAAAAQAAAAQAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'QAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAADAAAAAAAAAAAAAAABAAAADQAAAA0AAAABAAAA'
                     b'AAAAAAAAAAADAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAABAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAwAAAAAAAAAzAAAAlgAAANQAAADwAAAA8AAAANQAAACWAAAAMwAAAAAAAAADAA'
                     b'AAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAgAAAARAAAAEAAAABAAAAAPAAAAAQAAAAAAAAAAA'
                     b'AAAAQAAAAAAAAAIAAAAlwAAAP4AAAD/AAAA/wAAAPcAAAD3AAAA/wAAAP8AAAD+AAAAlwAAAAgAAAAAAAAAAQAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAgAAAAAAAABRAAAA5gAAAPIAAADwAAAA9gAAAOIAAAAQAAAAAAAAAAIAAAAAAAAACAAAALsAAAD'
                     b'/AAAA8gAAAIsAAAAyAAAAFAAAABQAAAAyAAAAiwAAAPIAAAD/AAAAuwAAAAgAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAA'
                     b'AAAAAABgAAANwAAAD/AAAA8QAAAPEAAAD2AAAA4gAAABAAAAAAAAAABAAAAAAAAACWAAAA/wAAAN0AAAAuAAAAAAAAAAIAA'
                     b'AAAAAAAAAAAAAIAAAAAAAAALgAAAN0AAAD/AAAAlgAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAARAAAA8AAAAPEA'
                     b'AAAfAAAADAAAABIAAAAPAAAAAQAAAAIAAAAAAAAANgAAAP8AAAD2AAAAMwAAAAAAAAAHAAAAAgAAAAAAAAAFAAAABAAAAAY'
                     b'AAAAAAAAAMwAAAPYAAAD/AAAANgAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAABAAAADxAAAA8gAAABAAAAAAAAAAAQAAAA'
                     b'AAAAAAAAAABAAAAAAAAACSAAAA/wAAAIoAAAAAAAAAAAAAABUAAACiAAAAJwAAAAAAAAADAAAAAwAAAAYAAAAAAAAAigAAA'
                     b'P8AAACSAAAAAAAAAAQAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADyAAAAEQAAAAAAAAACAAAAAQAAAAEAAAAAAAAAAAAA'
                     b'ANAAAAD/AAAANwAAAAAAAAAAAAAAEQAAAO8AAAD7AAAAfgAAAAgAAAAAAAAAAwAAAAAAAAA3AAAA/wAAANAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAQAAAAAAAAAQAAAA8gAAAPIAAAAQAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAAOAAAA7QAAAPcAAAAWAAAAAA'
                     b'AAAAAAAAARAAAA6gAAAP8AAAD/AAAA5gAAAFYAAAAAAAAAAAAAABYAAAD3AAAA7QAAAA0AAAAAAAAAAQAAAAAAAAABAAAAA'
                     b'AAAABAAAADyAAAA8gAAABAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAA4AAADtAAAA9gAAABYAAAAAAAAAAAAAABEAAADqAAAA'
                     b'/wAAAP8AAADmAAAAVgAAAAAAAAAAAAAAFgAAAPcAAADtAAAADQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADyAAA'
                     b'AEAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAANAAAAD/AAAANgAAAAAAAAAAAAAAEQAAAO8AAAD7AAAAfgAAAAgAAAAAAA'
                     b'AAAwAAAAAAAAA3AAAA/wAAANAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAQAAAA8gAAAPIAAAAQAAAAAAAAAAEAAAAAA'
                     b'AAAAAAAAAQAAAAAAAAAkgAAAP8AAACJAAAAAAAAAAAAAAAVAAAAogAAACcAAAAAAAAAAwAAAAMAAAAGAAAAAAAAAIoAAAD/'
                     b'AAAAkwAAAAAAAAAEAAAAAAAAAAAAAAABAAAAAAAAABAAAADyAAAA8gAAABAAAAAAAAAAAQAAAAAAAAAAAAAAAgAAAAAAAAA'
                     b'2AAAA/wAAAPUAAAAyAAAAAAAAAAcAAAACAAAAAAAAAAUAAAAEAAAABgAAAAAAAAAyAAAA9gAAAP8AAAA2AAAAAAAAAAIAAA'
                     b'AAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADyAAAAEAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAgAAAAAAAACWAAAA/wAAANwAA'
                     b'AAuAAAAAAAAAAIAAAAAAAAAAAAAAAIAAAAAAAAALgAAAN0AAAD/AAAAlgAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAQAAAAAA'
                     b'AAAQAAAA8gAAAPIAAAAQAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAgAAAC7AAAA/wAAAPEAAACKAAAAMgAAABQ'
                     b'AAAAUAAAAMgAAAIoAAADyAAAA/wAAALsAAAAIAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAABAAAADyAAAA8gAAAB'
                     b'AAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAgAAACXAAAA/wAAAP8AAAD/AAAA9gAAAPcAAAD/AAAA/wAAA'
                     b'P8AAACXAAAACAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADyAAAAEQAAAAAAAAACAAAAAQAA'
                     b'AAEAAAABAAAAAQAAAAEAAAACAAAAAwAAAAAAAAA0AAAAlgAAANUAAADwAAAA8AAAANUAAACXAAAANAAAAAAAAAADAAAAAgA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAQAAAA8gAAAPIAAAAQAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAABAAAAAAAAABAAAADyAAAA8wAAAB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAA'
                     b'EwAAABQAAAAQAAAADAAAAAwAAAAQAAAAFAAAABMAAAAQAAAAEgAAABAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAA'
                     b'AEQAAAO4AAAD/AAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPMAAADzAA'
                     b'AA8wAAAPMAAADyAAAA8gAAAPEAAADyAAAA3QAAABAAAAAAAAAAAQAAAAAAAAAAAAAAAQAAAAAAAAARAAAA7gAAAP8AAADyA'
                     b'AAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADy'
                     b'AAAA8gAAAP8AAADuAAAAEQAAAAAAAAABAAAAAAAAAAAAAAABAAAAAAAAABAAAADyAAAA8wAAAB8AAAAMAAAAEQAAABAAAAA'
                     b'QAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEQAAAAwAAAAfAAAA8gAAAPEAAA'
                     b'AQAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADyAAAAEAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAABAAAADyAAAA8gAAABAAAAAAAAAAAQAAAAAA'
                     b'AAAAAAAAAQAAAAAAAAAQAAAA8QAAAPIAAAAQAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADxAAAAEAAAAAAAAAABAAAAAAAAAAAAAAABAAAAAAAAAB'
                     b'EAAADwAAAA8QAAAB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAA'
                     b'BAAAAAQAAAAEQAAAAwAAAAfAAAA8QAAAPAAAAARAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAABgAAANwAAAD/AAAA8QAA'
                     b'APIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gA'
                     b'AAPEAAAD/AAAA3AAAAAYAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAUgAAAOYAAADyAAAA8gAAAPIAAADyAAAA8g'
                     b'AAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAOYAAABSAAAAA'
                     b'AAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAACAAAABEAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAA'
                     b'EAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAARAAAACAAAAAAAAAABAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAIAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAB'
                     b'AAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//2Mb+gSYZfS9IBLqBgABZAUAAmgFCEIoAhIhKFIhEShGMFGoVDAwqFQwMKhW'
                     b'MFGoUiERKFISIShZCEIoWQACaFoABWhAIBJoX+hf6AAAAWgAAAFoAAABaAAAAWhf/6FoX/+haAAAAWgAAAFkAAACagAABXS'
                     b'//9L6AAAF/////8='
)
        icon_img3 = b64decode(icon_img3)
        icon_img3 = ImageTk.PhotoImage(data=icon_img3)
        self.exehwnd.tk.call('wm', 'iconphoto', self.exehwnd._w, icon_img3)

    def initIO(self):
        MainFrame0 = tk.Frame(self.exehwnd)
        MainFrame0.pack()
        TopFrame1 = ttk.Frame(MainFrame0)
        TopFrame1.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        # -----------------------------------------------------------------------------------
        ObsInFrame3 = ttk.LabelFrame(TopFrame1, text='RINEX Obs File')
        ObsInFrame3.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)
        ObsFileSelectBox = ttk.Combobox(ObsInFrame3, width=46, height=4, values=('',),
                                        textvariable=self.ObsSelectBoxVar)
        ObsFileSelectBox.pack(side=tk.LEFT, anchor='w', padx='1px', pady='1px')

        ObsFileSelectButton = ttk.Button(ObsInFrame3, text='...', width=3,
                                         command=lambda: self.Cmd.GetObsFilePath(ObsFileSelectBox))
        ObsFileSelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='1px')
        # -----------------------------------------------------------------------------------

        #-----------------------------------------------------------------------------------
        NavInFrame3 = ttk.LabelFrame(TopFrame1, text='RINEX Nav File')
        NavInFrame3.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)
        NavFileSelectBox = ttk.Combobox(NavInFrame3, width=46, height=4, values=('',),
                                        textvariable=self.NavSelectBoxVar)
        NavFileSelectBox.pack(side=tk.LEFT, anchor='w', padx='1px', pady='1px')

        NavFileSelectButton = ttk.Button(NavInFrame3, text='...', width=3,
                                         command=lambda: self.Cmd.GetNavFilePath(NavFileSelectBox))
        NavFileSelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='1px')
        # -----------------------------------------------------------------------------------

        BottomFrame1 = ttk.Frame(MainFrame0)
        BottomFrame1.pack(side=tk.BOTTOM, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        FileOutFrame3 = ttk.LabelFrame(BottomFrame1, text='Output Directory')
        FileOutFrame3.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        ## CheckButton Initialize
        AskOrNotCheckButton = ttk.Checkbutton(FileOutFrame3, text='Directory',
                                              variable=self.AskOrNotCheckButtonVar, onvalue=1, offvalue=0,
                                              command=lambda: self.Cmd.AskOrNotCheck(
                                                                            self.AskOrNotCheckButtonVar,
                                                                            AskDirectorySelectBox,
                                                                            AskDirectorySelectButton))
        AskOrNotCheckButton.pack(side=tk.LEFT, anchor='w', padx='1px', pady='0px')

        ## SelectBox Initialize
        AskDirectorySelectBox = ttk.Combobox(FileOutFrame3, width=36, height=4, values=('',),
                                             state=tk.DISABLED, textvariable=self.DirectorySelectBoxVar)
        AskDirectorySelectBox.pack(side=tk.LEFT, anchor='w', padx='1px', pady='0px')

        ## SelectButton Initialize
        AskDirectorySelectButton = ttk.Button(FileOutFrame3, text='...', width=3,
                                              state=tk.DISABLED, command=lambda: self.Cmd.AskDirectory(AskDirectorySelectBox))
        AskDirectorySelectButton.pack(side=tk.RIGHT, anchor='e', padx='2px', pady='0px')

        ExeFrame3 = ttk.Frame(BottomFrame1)
        ExeFrame3.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        ExitButton = ttk.Button(ExeFrame3, text='Exit', width=10,
                                command=self.exehwnd.destroy)
        ExitButton.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        ExecuteButton = ttk.Button(ExeFrame3, text='Execute', width=10,
                                   command=lambda :self.Cmd._ExecuteFile(ExecuteState,
                                                                self.ObsSelectBoxVar,
                                                                self.NavSelectBoxVar,
                                                                self.AskOrNotCheckButtonVar,
                                                                self.DirectorySelectBoxVar))

        ExecuteButton.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        # Execute state bar
        StateFrame = ttk.Frame(BottomFrame1)
        StateFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')
        ExecuteState = ttk.Label(StateFrame, text="None")
        ExecuteState.pack(side=tk.LEFT, anchor='nw')

def View_windowshow(text, view):
    # Brief # get the file path of reading and show in the text ctr box
    # Param # text : the show box of file of choice
    # Param # view : the father window of text ctr box
    # Return# none
    f_path = filedialog.askopenfilename()
    view.title('Viewing: %s' % f_path)
    text.delete('1.0', 'end')
    with open(f_path, 'r') as f:
        fcon = f.read()
        text.insert('insert', fcon)
    text.config()

class VIEWGUI:
    def __init__(self, hwnd):
        self.initGUI(hwnd)

    @staticmethod
    def initGUI(hwnd):
        view = tk.Toplevel(hwnd)
        view.title("View")
        view.geometry('900x600')
        view.minsize(1000, 600)

        global icon_img1
        icon_img1 = (b'AAABAAEAMDAAAAEAIACoJQAAFgAAACgAAAAwAAAAYAAAAAEAIAAAAAAAACQAAPY6AQD2OgEAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAQAAA'
                     b'ABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAEAAAAAQAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAACAAAAAgAAAAAAAAABAAAADQAAABIAAAARAAAAEQAAABEAAAARAAAAEQAAAB'
                     b'EAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAASAAAAD'
                     b'QAAAAEAAAAAAAAAAgAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAACQAAAHEAAADMAAAA6wAAAO8'
                     b'AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7g'
                     b'AAAO4AAADuAAAA7gAAAO4AAADvAAAA6wAAAMwAAAByAAAACQAAAAAAAAACAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAA'
                     b'AAAdAAAAzwAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wA'
                     b'AAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AA'
                     b'AA0AAAAB0AAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAABAAAAAAAAAAgAAADMAAAA/wAAAPoAAAD6AAAA/gAAAP8AAAD/AAAA/wAA'
                     b'AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAA'
                     b'A/wAAAP8AAAD/AAAA/gAAAPoAAAD6AAAA/wAAAMwAAAAIAAAAAAAAAAEAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAHIAAAD/AAAA+QAAA'
                     b'P8AAAD/AAAA9wAAAO0AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA'
                     b'7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADtAAAA9wAAAP8AAAD/AAAA+QAAAP8AAAB'
                     b'xAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAABAAAAAAAAAMcAAAD/AAAA+gAAAP8AAACtAAAAGQAAABEAAAASAAAAEQAAABEAAAARAAAAE'
                     b'QAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAAUAAAAFgAAABUAAAAR'
                     b'AAAAGQAAAK0AAAD/AAAA+gAAAP8AAADHAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAADQAAAOgAAAD/AAAA/wAAAPkAAAAjAAAAAA'
                     b'AAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAACMAAAD5AAAA/wAAAP8AAADnAAAADQAAAAAA'
                     b'AAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgA'
                     b'AAO0AAAD/AAAA/wAAAO0AAAATAAAAAAAAAAIAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAA'
                     b'AAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAABQAAAAAAAAA/AAAAkwAAAE0AAAAAAAAAAAAAABQAA'
                     b'ADtAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAEAAAAAAAAAEQAAAO0AAAD/AAAA/wAAAO4AAAASAAAAAAAAAAEAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAQAAAAEAAAABAAAAAIAAAAFAAAAAAAAAFsAAA'
                     b'D/AAAA/gAAAP8AAABNAAAAAAAAABUAAADuAAAA/wAAAP8AAADtAAAAEQAAAAAAAAABAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA'
                     b'/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAADAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAIAAAAAAAAAXAAAAP8AAAD9AAAA9QAAAP8AAACIAAAAAAAAABUAAADuAAAA/wAAAP'
                     b'8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAgAAAAIAAAAAAAAAKgAAAGcAAAB7AAAAaAAAAB0AAABaAAAA/wAAAP0AAAD8AAAA/QAAAP8'
                     b'AAAA/AAAAAAAAABQAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARA'
                     b'AAAAAAAAAEAAAAAAAAAAAAAAAAAAAACAAAAAAAAABYAAACrAAAA/gAAAP8AAAD+AAAA/wAAAPcA'
                     b'AAD4AAAA/gAAAP0AAAD9AAAA/wAAAFwAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgA'
                     b'AAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAA'
                     b'AAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAGAAAANgAA'
                     b'AD/AAAA/QAAAPkAAAD2AAAA+QAAAP8AAAD9AAAA/gAAAP8AAAD/AAAAXAAAAAAAAAAFAAAAAAAA'
                     b'ABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAA'
                     b'AAAAAAAAAAAAIAAAAAAAAArAAAAP8AAAD5AAAA/QAAAP8AAAD/AAAA/wAAAP0AAAD+AAAA/wAAA'
                     b'P8AAABbAAAAAAAAAAUAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD'
                     b'/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAgAAAAAAAAAwAAAA/gAAAP0AAAD+AAAA/wAAAM'
                     b'YAAACAAAAAygAAAP8AAAD9AAAA/wAAAPoAAAAmAAAAAAAAAAIAAAABAAAAAAAAABEAAADuAAAA/'
                     b'wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAABAAAAAA'
                     b'AAABqAAAA/wAAAPkAAAD/AAAAxQAAAAMAAAAAAAAABgAAAMsAAAD/AAAA+QAAAP8AAABkAAAAAA'
                     b'AAAAQAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4A'
                     b'AAARAAAAAAAAAAEAAAAAAAAABAAAAAAAAAB/AAAA/wAAAPcAAAD/AAAAggAAAAAAAAASAAAAAAA'
                     b'AAIoAAAD/AAAA9wAAAP8AAAB4AAAAAAAAAAQAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAA'
                     b'AAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAA'
                     b'AAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAABAAAAAAAAABrAAAA/wAA'
                     b'APkAAAD/AAAAwQAAAAAAAAAAAAAAAwAAAMcAAAD/AAAA+QAAAP8AAABkAAAAAAAAAAQAAAABAAA'
                     b'AAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAA'
                     b'AEAAAAAAAAAAgAAAAAAAAAyAAAA/wAAAP0AAAD+AAAA/wAAAMEAAAB4AAAAxAAAAP8AAAD+AAAA'
                     b'/gAAAPwAAAArAAAAAAAAAAIAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAA'
                     b'BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO'
                     b'0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAIAAAAAAAAAsAAAAP8AAAD5AAAA/'
                     b'QAAAP8AAAD/AAAA/wAAAP0AAAD5AAAA/wAAAKkAAAAAAAAAAgAAAAAAAAABAAAAAAAAABEAAADu'
                     b'AAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAA'
                     b'AAAAEAAAAAAAAAHAAAAN0AAAD/AAAA/AAAAPgAAAD2AAAA+AAAAPwAAAD/AAAA2AAAABgAAAAAA'
                     b'AAAAQAAAAAAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wA'
                     b'AAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAACAAAAAAAAABsAAAC0AAAA/wAAAP8AAAD+AA'
                     b'AA/wAAAP8AAACvAAAAGAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AA'
                     b'ADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAQAAAAEAAAABAAA'
                     b'AAwAAAAIAAAAAAAAAMQAAAG8AAACEAAAAbgAAAC8AAAAAAAAAAgAAAAMAAAABAAAAAQAAAAAAAA'
                     b'ABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAA'
                     b'AAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAA'
                     b'AAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAE'
                     b'gAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAABAAAAEAAAABIAAAASAAAAEgAAABIAAAAS'
                     b'AAAAFAAAABYAAAAWAAAAFgAAABQAAAASAAAAEgAAABIAAAASAAAAEAAAAAEAAAABAAAAAAAAABE'
                     b'AAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAAAAAAQA'
                     b'AAA3QAAAPIAAADsAAAA7QAAAO0AAADtAAAA7QAAAO0AAADtAAAA7QAAAO0AAADtAAAA7QAAAOwA'
                     b'AADyAAAA3QAAABAAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AA'
                     b'AA/wAAAO4AAAARAAAAAAAAAAAAAAASAAAA7QAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AA'
                     b'AD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7QAAABIAAAAAAAAAAAAAABEAAADuAAAA/wAA'
                     b'AP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAAAAAASAAAA7QAAAP8AAA'
                     b'D+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7QAAA'
                     b'BIAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAA'
                     b'RAAAAAAAAAAAAAAAQAAAA3QAAAPIAAADtAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO'
                     b'4AAADuAAAA7gAAAO0AAADyAAAA3QAAABAAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAE'
                     b'gAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA'
                     b'AAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAABAAAAEAAAABIAAAARAAAAEQAAABE'
                     b'AAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAASAAAAEAAAAAEAAAABAAAAAA'
                     b'AAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AA'
                     b'AD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAABEAAADuAAA'
                     b'A/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAEAAAABAAAAEAAAA'
                     b'BIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAASAAAA'
                     b'EAAAAAEAAAABAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO'
                     b'4AAAARAAAAAAAAAAAAAAAQAAAA3QAAAPIAAADsAAAA7QAAAO0AAADtAAAA7QAAAO0AAADtAAAA7'
                     b'QAAAO0AAADtAAAA7QAAAOwAAADyAAAA3QAAABAAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADt'
                     b'AAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE'
                     b'AAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAAAAAASAAAA7QAAAP8AAAD+AAAA/w'
                     b'AAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7QAAABIAAAAAA'
                     b'AAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/wAAAO4AAAARAAAAAAA'
                     b'AAAAAAAASAAAA7QAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AA'
                     b'AA/wAAAP4AAAD/AAAA7QAAABIAAAAAAAAAAAAAABEAAADuAAAA/wAAAP8AAADtAAAAEgAAAAAAA'
                     b'AABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAA'
                     b'AO0AAAD/AAAA/wAAAO4AAAARAAAAAAAAAAAAAAAQAAAA3QAAAPIAAADsAAAA7QAAAO0AAADtAAA'
                     b'A7QAAAO0AAADtAAAA7QAAAO0AAADtAAAA7QAAAOwAAADyAAAA3QAAABAAAAAAAAAAAAAAABEAAA'
                     b'DuAAAA/wAAAP8AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAEAAAAAAAAAEQAAAO0AAAD/AAAA/wAAAO4AAAASAAAAAAAAAAEAAAABAAAA'
                     b'EAAAABIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAASAAAAEgAAABIAAAA'
                     b'SAAAAEAAAAAEAAAABAAAAAAAAABIAAADuAAAA/wAAAP8AAADtAAAAEQAAAAAAAAABAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEgAAAO0AAAD/AAAA/'
                     b'wAAAO0AAAATAAAAAAAAAAIAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAACAAAAAAAAABMAAADtAAAA/wAAAP8'
                     b'AAADtAAAAEgAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAEAAAAAAAAADQAAAOgAAAD/AAAA/wAAAPkAAAAjAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAACAAAAAAAAACMAAAD5AAAA/wAAAP8AAADnAAAADQAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAMcAAAD/AAAA+gAAAP8AAACtAA'
                     b'AAGQAAABEAAAASAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAA'
                     b'AARAAAAEQAAABEAAAARAAAAEQAAABIAAAARAAAAGQAAAK0AAAD/AAAA+gAAAP8AAADHAAAAAAAA'
                     b'AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAA'
                     b'AAAAAAHIAAAD/AAAA+QAAAP8AAAD/AAAA9wAAAO0AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAA'
                     b'DuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADtAAAA9wAAA'
                     b'P8AAAD/AAAA+QAAAP8AAABxAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAgAAADMAAAA/wAAAPoAAAD6AAAA/gAAAP8AAAD'
                     b'/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP'
                     b'8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAPoAAAD5AAAA/wAAAMwAAAAIAAAAAAAAAAEAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAd'
                     b'AAAA0AAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8'
                     b'AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA0A'
                     b'AAAB0AAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAACgAAAHIAAADNAAAA6wAAAO8AAADuAAAA7gAAAO4A'
                     b'AADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gAAAO4AAADuAAAA7gA'
                     b'AAO4AAADvAAAA6wAAAM0AAAByAAAACgAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAgAAAAAAA'
                     b'AABAAAADQAAABIAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAARAAAAEQAA'
                     b'ABEAAAARAAAAEQAAABEAAAARAAAAEQAAABEAAAASAAAADQAAAAEAAAAAAAAAAgAAAAIAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAQAAAAQAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                     b'AAAAAAEAAAAEAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/Rf/'
                     b'/ov8AAP6QAAAJfwAA/UAAAAK/AAD+gAAAAX8AAPkAAAAAnwAA+QAAAACfAAD5AAAAAJ8AAPoF//'
                     b'+gXwAA+gQABGBfAAD6BegIIF8AAPoF0pAgXwAA+gWkACBfAAD6BVAAYF8AAPoFIACgXwAA+gUgA'
                     b'SBfAAD6BUABIF8AAPoFQIEgXwAA+gVBQSBfAAD6BUCBIF8AAPoFQAEgXwAA+gUgAiBfAAD6BSAC'
                     b'IF8AAPoFUAUgXwAA+gQEECBfAAD6Bf//oF8AAPoEAAAgXwAA+gYAAGBfAAD6BgAAYF8AAPoGAAB'
                     b'gXwAA+gYAAGBfAAD6BAAAIF8AAPoF//+gXwAA+gX//6BfAAD6BAAAIF8AAPoGAABgXwAA+gYAAG'
                     b'BfAAD6BgAAYF8AAPoGAABgXwAA+gQAACBfAAD6BF/6IF8AAPoF//+gXwAA+QAAAACfAAD5AAAAA'
                     b'J8AAPkAAAAAnwAA/oAAAAF/AAD9QAAAAr8AAP6QAAAJfwAA/0X//6L/AAA=')

        icon_img1 = b64decode(icon_img1)
        icon_img1 = ImageTk.PhotoImage(data=icon_img1)
        view.tk.call('wm', 'iconphoto', view._w, icon_img1)

        # View window's menu
        topmenu = tk.Menu(view)
        filemenu = tk.Menu(topmenu, tearoff=False)
        filemenu.add_command(label="Open File",
                             command=lambda: View_windowshow(text, view), accelerator='Ctrl+F')
        filemenu.add_command(label="Exit", command=view.destroy, accelerator='Ctrl+E')
        topmenu.add_cascade(label="File", menu=filemenu)

        view.config(menu=topmenu)

        ybar = tk.Scrollbar(view)
        ybar.pack(side=tk.RIGHT, fill=tk.Y)
        xbar = tk.Scrollbar(view, orient=tk.HORIZONTAL)
        xbar.pack(side=tk.BOTTOM, fill=tk.X)

        text = tk.Text(view, xscrollcommand=xbar.set, yscrollcommand=ybar.set, height=500, width=1000, undo=True,
                       autoseparators=False, wrap='none')
        text.pack(side=tk.TOP, fill=tk.BOTH)

        ybar.config(command=text.yview)
        xbar.config(command=text.xview)

if __name__ == "__main__":

    # Main window
    root = tk.Tk()
    MAIN = MAINGUI(root)

