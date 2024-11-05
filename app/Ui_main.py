#  @ File : UI_main.py
#
#  Copyright (c) 2024 KenanZhu. All Right Reserved.
#
#  @ Author       : KenanZhu
#  @ Time         : 2024/11/04
#  @ Brief        : Main window class.
#  #
#  @ IDE          : PyCharm 2024.2.1 (Community Edition)
#
#  ----------------------------------------------------------------------------------------

### Self
import Ui_view as vie
import Ui_about as abo
import Ui_options as opt
import Ui_processor as pro
import Config_file as config
import Func_callback as func

### Std
import threading

from tkinter import ttk
from PIL import ImageTk
from base64 import b64decode
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import tkinter as tk
import tkinter.font as tkfont
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

def instanceOPT(hwndparent, cfg_get_, func_):
    opt.OPTGUI(hwndparent, cfg_get_, func_)

def instancePRO(hwndparent, cfg_get_, func_):
    pro.EXECUDUI(hwndparent, cfg_get_, func_)

def instanceVIE(hwndparent, func_):
    vie.VIEWGUI(hwndparent, func_)

def instanceABO(hwndparemt, cfg_get_, func_):
    abo.ABODUI(hwndparemt, cfg_get_, func_)

def _instanceOPT(hwndparemt, cfg_get_, func_):
    T = threading.Thread(target=lambda :instanceOPT(hwndparemt, cfg_get_, func_))
    T.start()

def _instancePRO(hwndparemt, cfg_get_, func_):
    T = threading.Thread(target=lambda :instancePRO(hwndparemt, cfg_get_, func_))
    T.start()

def _instanceVIE(hwndparemt, func_):
    T = threading.Thread(target=lambda :instanceVIE(hwndparemt, func_))
    T.start()

def _instanceABO(hwndparemt, cfg_get_, func_):
    T = threading.Thread(target=lambda :instanceABO(hwndparemt, cfg_get_, func_))
    T.start()


# noinspection PyUnusedLocal,PyProtectedMember
class MAINGUI:
    def  __init__(self, hwnd_, func_):
        # init
        # -------------------------------------------------------------------------------
        self.func = func_
        self.hwnd = hwnd_

        self.ux = None
        self.nx = None
        self.ex = None

        self.satn = None
        self.satvisb = None
        self.sattrack = None

        self.canvas1 = None
        self.canvas0 = None
        self.canvas2 = None

        self.Drawcards = None
        self.Figurefrm_Sky = None
        self.Figurefrm_Vis = None
        self.Figurefrm_ENU = None

        self.lastx = None
        self.lasty = None
        self.press = None

        self.plotstate = None

        self.initGUI()

    def initGUI(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        ### Set size
        self.hwnd.title(
            "KNZ_GeoTrackLab %s"
            %cfg_get['INFO']['Version']
        )
        self.func.Move_center(hwnd,1200,700)
        self.hwnd.minsize(1200, 700)
        ### Set icon
        icon_ico = (b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
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
        icon_ico = b64decode(icon_ico)
        icon_ico = ImageTk.PhotoImage(data=icon_ico)
        self.hwnd.tk.call('wm', 'iconphoto', self.hwnd._w, icon_ico)
        ### Set front
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=9)
        ### Top tool
        self.initTOPMENU()
        ### Plot area
        self.initPLOT()
        ### State bar
        self.initSTATE_BAR()
        ### Quit event & mainloop start
        self.hwnd.protocol("WM_DELETE_WINDOW", self.hwnd.quit)
        self.hwnd.mainloop()

    def initTOPMENU(self):
        # -------------------------------------------------------------------------------
        # Class :
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        topmenu = tk.Menu(self.hwnd)
        ### File
        filemenu = tk.Menu(topmenu, tearoff=False)
        ### File > Open...
        openmenu = tk.Menu(filemenu, tearoff=False)
        ### File > Open... > Open Pos Solution
        openmenu.add_command(
            label="Open Pos Solution",
            accelerator='Ctrl+S',
            command=lambda :self.func._OpenkslnFile(
                self.ex,self.nx,self.ux,self.satn,self.satvisb,
                self.canvas0,self.canvas1,self.plotstate)
        )
        ### File > Open... > Open Sat Solution
        openmenu.add_command(
            label="Open Sat Solution",
            accelerator='Ctrl+S',
            command=lambda :self.func._Plot2polar(
                self.sattrack,self.plotstate,self.canvas2)
        )
        ### File > Open... > Open RINEX
        openmenu.add_command(
            label="Open RINEX",
            command=lambda :instancePRO(hwnd, cfg_get, self.func),
            accelerator='Ctrl+P'
        )
        filemenu.add_cascade(label="Open...", menu=openmenu)
        ### File > Clesr
        filemenu.add_command(
            label="Clear",
            command=self.Clear_canvas
        )
        ### File > View
        filemenu.add_command(
            label="View",
            command=lambda :instanceVIE(self.hwnd, self.func)
        )
        ### File > Exit
        filemenu.add_command(
            label="Exit",
            command=self.hwnd.quit,
            accelerator='Ctrl+E'
        )
        topmenu.add_cascade(label="File", menu=filemenu)

        ### Options
        optmenu = tk.Menu(topmenu, tearoff=False)
        ### Options > Options...
        optmenu.add_command(
            label="Options...",
            command=lambda :instanceOPT(self.hwnd,cfg_get,self.func)
        )
        topmenu.add_cascade(
            label="Options",
            menu=optmenu
        )

        ### Help
        helpmenu = tk.Menu(topmenu, tearoff=False)
        ### Help > About
        helpmenu.add_command(
            label="About",
            command=lambda :instanceABO(self.hwnd, cfg_get, self.func)
        )
        topmenu.add_cascade(label="Help", menu=helpmenu)

        self.hwnd.config(menu=topmenu)

    def initPLOT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initPLOT
        # Brief : Initializes the drawing area of the main ui
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.Drawcards = ttk.Notebook(self.hwnd)
        # E-N-U Plot area
        # -------------------------------------------------------------------------------
        self.PLOT_ENU()
        self.Drawcards.add(self.Figurefrm_ENU, text='ENU-Draw')
        # Valid Satellite Amout area
        # -------------------------------------------------------------------------------
        self.PLOT_VIS()
        self.Drawcards.add(self.Figurefrm_Vis, text='Sat Number')
        # Sky Track Plot area
        # -------------------------------------------------------------------------------
        self.PLOT_SKY()
        self.Drawcards.add(self.Figurefrm_Sky, text='Sat Track')
        self.Drawcards.pack(fill=tk.BOTH, expand=True, padx='2px', pady='0px')

    def PLOT_ENU(self):
        # -------------------------------------------------------------------------------
        # >
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.Figurefrm_ENU = tk.Frame(self.hwnd)
        self.Figurefrm_ENU.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        plt.rc('font', family='Segoe UI')
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        fig, (self.ex, self.nx, self.ux) = plt.subplots(
            3,
            1,
            figsize=(10, 0),
            sharex=True
        )
        for spine in ['right', 'left']:
            self.ex.spines[spine].set_visible(False)
        self.ex.set_facecolor('#f5f5f5')
        for spine in ['right', 'left']:
            self.nx.spines[spine].set_visible(False)
        self.nx.set_facecolor('#f5f5f5')

        for spine in ['right', 'left']:
            self.ux.spines[spine].set_visible(False)
        self.ux.set_facecolor('#f5f5f5')
        fig.subplots_adjust(
            left=0,
            bottom=0.040,
            right=1,
            top=1,
            hspace=0.0
        )
        self.canvas0 = FigureCanvasTkAgg(fig, self.Figurefrm_ENU)
        self.canvas0.draw()
        self.canvas0.get_tk_widget().pack( side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        toolbar0 = NavigationToolbar2Tk(self.canvas0, self.Figurefrm_ENU, pack_toolbar=False)
        toolbar0.update()
        toolbar0.pack(side=tk.LEFT)
        ### Call back event
        self.canvas0.mpl_connect("button_press_event",self.On_press)
        self.canvas0.mpl_connect("button_release_event",self.On_release)
        self.canvas0.mpl_connect("motion_notify_event",self.On_move)
        self.canvas0.mpl_connect('scroll_event',self.On_scaleing)

    def PLOT_VIS(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.Figurefrm_Vis = tk.Frame(self.hwnd)
        self.Figurefrm_Vis.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        plt.rc('font', family='Segoe UI')
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        fig, (self.satn, self.satvisb) = plt.subplots(
            2,
            1,
            figsize=(10, 0),
            sharex=True
        )
        fig.subplots_adjust(
            left=0,
            bottom=0.045,
            right=1,
            top=0.95,
            hspace=0.0
        )
        for spine in ['right', 'left']:
            self.satn.spines[spine].set_visible(False)
        self.satn.set_facecolor('#f5f5f5')
        for spine in ['right', 'left']:
            self.satvisb.spines[spine].set_visible(False)
        self.satvisb.set_facecolor('#f5f5f5')

        self.canvas1 = FigureCanvasTkAgg(fig, self.Figurefrm_Vis)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        toolbar1 = NavigationToolbar2Tk(self.canvas1, self.Figurefrm_Vis, pack_toolbar=False)
        toolbar1.update()
        toolbar1.pack(side=tk.LEFT)

    def PLOT_SKY(self):
        # -------------------------------------------------------------------------------
        # >
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.Figurefrm_Sky = tk.Frame(self.hwnd)
        self.Figurefrm_Sky.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        plt.rc('font', family='Segoe UI')
        fig = plt.figure()
        self.sattrack = fig.add_subplot(
            projection=ccrs.Mercator()
        )
        self.sattrack.coastlines(resolution='110m')
        self.sattrack.gridlines()
        fig.subplots_adjust(
            left=0,
            bottom=0.03,
            right=1,
            top=0.95
        )
        for spine in ['right', 'left']:
            self.sattrack.spines[spine].set_visible(False)
        self.sattrack.set_facecolor('#f5f5f5')

        self.canvas2 = FigureCanvasTkAgg(fig, self.Figurefrm_Sky)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        toolbar2 = NavigationToolbar2Tk(self.canvas2, self.Figurefrm_Sky, pack_toolbar=False)
        toolbar2.update()
        toolbar2.pack(side=tk.TOP, anchor='w')

    def initSTATE_BAR(self):
        stateframe = tk.Frame(self.hwnd)
        stateframe.pack(side=tk.BOTTOM, fill=tk.X)
        self.plotstate = ttk.Label(stateframe, text="None")
        self.plotstate.pack(side=tk.LEFT, anchor='w')

    def On_press(self, event):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        if event.inaxes:
            if event.button == 1:
                self.press = True
                self.lastx = event.xdata
                self.lasty = event.ydata

    def On_move(self, event):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        axtemp = event.inaxes
        if axtemp:
            if self.press:
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty
                x_min, x_max = axtemp.get_xlim()
                y_min, y_max = axtemp.get_ylim()
                x_min = x_min - x
                x_max = x_max - x
                y_min = y_min - y
                y_max = y_max - y
                axtemp.set_xlim(x_min, x_max)
                axtemp.set_ylim(y_min, y_max)
                self.canvas0.draw()

    def On_release(self, event):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        if self.press:
            self.press = False

    def On_scaleing(self, event):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        axtemp = event.inaxes
        y_min, y_max = axtemp.get_ylim()
        scaley = (y_max - y_min) / 10
        if event.button == 'up':
            axtemp.set(ylim=(y_min + scaley, y_max - scaley))
        elif event.button == 'down':
            axtemp.set(ylim=(y_min - scaley, y_max + scaley))
        self.canvas0.draw_idle()

    def Clear_canvas(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: Clear_canvas
        # Brief : clear the canvas
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
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
        self.hwnd.update()

if __name__ == "__main__":

    ### LOad Config
    cfg = config.Configinit('config.ini')
    cfg.load_config()
    cfg_get = cfg.get_config()

    ### Call Back Process
    func = func.CALLBACK(cfg, cfg_get)

    ### Main Window
    hwnd = tk.Tk()
    mainui = MAINGUI(hwnd, func)


