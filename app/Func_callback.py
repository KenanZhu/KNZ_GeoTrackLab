#  @ File : Func_callback.py
#
#  Copyright (c) 2024 KenanZhu. All Right Reserved.
#
#  @ Author       : KenanZhu
#  @ Time         : 2024/11/04
#  @ Brief        : Interactive control callback function class.
#  #
#  @ IDE          : PyCharm 2024.2.1 (Community Edition)
#
#  ----------------------------------------------------------------------------------------

### Std
import math
import threading

import numpy as np
import ctypes as ct
import tkinter as tk
import cartopy.crs as ccrs

from tkinter import filedialog
from tkinter import colorchooser

class CALLBACK:
    def __init__(self, cfg, cfg_get):
        # init
        # -------------------------------------------------------------------------------
        self.cfg = cfg
        self.cfg_get = cfg_get

        self.system = {1:'G',2:'C',3:'E',4:'R',5:'S'}
        self.ioncormode = {'OFF':'0', 'Ion-Free LC':'1',    'Broadcast':'2'}
        self.trocormode = {'OFF':'0',    'Hopfield':'1', 'Saastamoinen':'2'}

        self.colorvalue = [
            self.cfg_get['Options_Draw']['e_color'],
            self.cfg_get['Options_Draw']['n_color'],
            self.cfg_get['Options_Draw']['u_color'],
            self.cfg_get['Options_Draw']['sat_amount_color']
        ]
        self.linewidth = [
            self.cfg_get['Options_Draw']['e_line'],
            self.cfg_get['Options_Draw']['n_line'],
            self.cfg_get['Options_Draw']['u_line']
        ]

        self.obsvar = ('',)
        self.navvar = ('',)
        self.outvar = ('',)

        self.outdir = dict(self.cfg_get.items('Output_Path'))
        self.obspath = dict(self.cfg_get.items('Input_Obs_Path'))
        self.navpath = dict(self.cfg_get.items('Input_Nav_Path'))

        for i in self.obspath:
            if self.obspath.get(i):
                self.obsvar += (self.obspath.get(i),)

        for i in self.navpath:
            if self.navpath.get(i):
                self.navvar += (self.navpath.get(i),)

        for i in self.outdir:
            if self.outdir.get(i):
                self.outvar += (self.outdir.get(i),)
        ### Const value
        global blank
        blank = ' '

    @staticmethod
    def Move_center(hwnd, win_x, win_y):
        # -------------------------------------------------------------------------------
        # >
        # Method: Move_Ccenter
        # Brief : Move the window to the center of screen.
        # Param : hwnd : instance handle of window
        #         win_x: the x size of window
        #         win_y: the y size of window
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        position_x = int((hwnd.winfo_screenwidth() - win_x) / 2)
        position_y = int((hwnd.winfo_screenheight() - win_y) / 2)
        hwnd.geometry(f'{win_x}x{win_y}+{position_x}+{position_y}')

    def Calcuconfirm(self, cionbox, ctrobox, canglebox, systemv,
                     trackprn, trackint):
        # -------------------------------------------------------------------------------
        # >
        # Method: Calcuconfirm
        # Brief : Callback function of confirm button of options window
        # Param : cionbox  : iono combobox handle
        #         ctrobox  : trop combobox handle
        #         canglabox: elev angle of sat combobox handle
        #         systemv  : sat system button handle
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------

        self.cfg_get.set('Options_Calc', 'Iono_model', self.ioncormode.get(cionbox.get()))
        self.cfg_get.set('Options_Calc', 'Trop_model', self.trocormode.get(ctrobox.get()))
        self.cfg_get.set('Options_Calc', 'Elev_angle', canglebox.get())
        self.cfg_get.set('Options_Calc', 'Sat_system', str(systemv.get()))
        self.cfg_get.set('Options_Draw', 'Track of prn', trackprn.get())
        self.cfg_get.set('Options_Draw', 'Track sample rate', trackint.get())

        self.cfg.save_config()

    def Colorchoose(self, hwndparent, i, colorlab, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method: Colorchoose
        # Brief : Color choose card of options callback function.
        # Param : hwndparent : instance handle of options window
        #         i          : 0==e    & 1==n      & 2==u & 3==satn
        #         colorlab   : color label handle
        #         mode       : 0==undo & 1==select & 2==save change
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        match mode:
            case 0:
                if not i==3:
                    self.colorvalue = [
                        self.cfg_get['Options_Draw']['e_color'],
                        self.cfg_get['Options_Draw']['n_color'],
                        self.cfg_get['Options_Draw']['u_color'],
                        self.colorvalue[3]
                    ]
                    colorlab.config(bg=self.colorvalue[i])
                else:
                    self.colorvalue = [
                        self.colorvalue[0],
                        self.colorvalue[1],
                        self.colorvalue[2],
                        self.cfg_get['Options_Draw']['sat_amount_color']
                    ]
                    colorlab.config(bg=self.colorvalue[i])
            case 1:
                colorvalue = tk.colorchooser.askcolor(parent=hwndparent)
                if colorvalue[1]:
                    self.colorvalue[i] = str(colorvalue[1])
                    colorlab.config(bg=self.colorvalue[i])
            case 2:
                self.cfg_get.set('Options_Draw', 'E_Color', str(self.colorvalue[0]))
                self.cfg_get.set('Options_Draw', 'N_Color', str(self.colorvalue[1]))
                self.cfg_get.set('Options_Draw', 'U_Color', str(self.colorvalue[2]))
                self.cfg_get.set('Options_Draw', 'Sat_Amount_Color', str(self.colorvalue[3]))
                self.cfg.save_config()

    def Linewchoose(self, entry0, entry1, entry2, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method: Linewchoose
        # Brief : Line width selection of plot.
        # Param : entry0 : spinbox handle
        #         entry1 : spinbox handle
        #         entry2 : spinbox handle
        #         mode   : 0==undo & 1==confirm
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        match mode:
            case 0:
                entry0.set(self.cfg_get['Options_Draw']['e_line'])
                entry1.set(self.cfg_get['Options_Draw']['n_line'])
                entry2.set(self.cfg_get['Options_Draw']['u_line'])
            case 1:
                self.cfg_get.set('Options_Draw', 'E_Line', str(entry0.get()))
                self.cfg_get.set('Options_Draw', 'N_Line', str(entry1.get()))
                self.cfg_get.set('Options_Draw', 'U_Line', str(entry2.get()))
                self.cfg.save_config()

    @staticmethod
    def Dir_or_name_get(path, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method: Dir_or_name_get
        # Brief : Get the filedir or filename form path
        # Param : path : file path
        #         mode : 0==get file name & 1==get file dir
        # Return: mode==0 return filename,mode==1 return file dir
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global nameend, filename, filedir
        match mode:
            case 0:
                path_len = len(path)
                while path_len > 0:
                    sig = path[path_len - 1:path_len]
                    if sig == '.':
                        nameend = path_len
                    if sig == '\\' or sig == '/':
                        filename = path[path_len:nameend]
                        return filename
                    path_len -= 1


            case 1:
                path_len = len(path)
                while path_len > 0:
                    sig = path[path_len - 1:path_len]
                    if sig == '\\' or sig == '/':
                        filedir = path[:path_len]
                        return filedir
                    path_len -= 1

    def GetObsFilePath(self, hwndparent, ObsFileSelectBox):
        # -------------------------------------------------------------------------------
        # >
        # Method: GetObsFilePath
        # Brief : Get obs file path of RINEX.
        # Param : hwndparent       : instance handle of RINEX processor window
        #         ObsFileSelectBox : string value of path combobox
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        path = filedialog.askopenfilename(
            parent=hwndparent,
            title='RINEX OBS File',
            filetypes=[('RINEX OBS File(*.o*.*.*obs.*.*d)', '*.*o;*.*obs;*.*d'),
                       ('All Files', '*.*')]
        )
        if path and path not in ObsFileSelectBox['value']:
            ObsFileSelectBox['value'] += (path,)
            ObsFileSelectBox.current(len(ObsFileSelectBox['value']) - 1)
            self.obsvar += (path,)
            self.cfg_get.set('Input_Obs_Path', '%s'
                             % str(len(ObsFileSelectBox['value']) - 1),
                             path)
            self.cfg.save_config()

    def GetNavFilePath(self, hwndparent, NavFileSelectBox):
        # -------------------------------------------------------------------------------
        # >
        # Method: GetNavFilePath
        # Brief : Get nav file path of RINEX.
        # Param : hwndparent       : instance handle of RINEX processor window
        #         NavFileSelectBox : string value of path combobox
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        path = filedialog.askopenfilename(
            parent=hwndparent,
            title='RINEX NAV File',
            filetypes=[('RINEX NAV File(*.*nav.*.hnav.*.gnav.*.qnav.*.*n.*.*g.*.*h.*.*q.*.*p)',
                                       '*.*nav;*.hnav;*.gnav;*.qnav;*.*n;*.*g;*.*h;*.*q;*.*p'),
                       ('All Files', '*.*')]
        )
        if path and path not in NavFileSelectBox['value']:
            NavFileSelectBox['value'] += (path,)
            NavFileSelectBox.current(len(NavFileSelectBox['value']) - 1)
            self.navvar += (path,)
            self.cfg_get.set('Input_Nav_Path', '%s'
                             % str(len(NavFileSelectBox['value']) - 1),
                             path)
            self.cfg.save_config()

    def AskDirectory(self, hwndparent, AskDirectorySelectBox):
        # -------------------------------------------------------------------------------
        # >
        # Method: AskDirectory
        # Brief : Get the output file diectory.
        # Param : hwndparent            : instance handle of RINEX processor window
        #         AskDirectorySelectBox : instance handle of dir combox
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        path = filedialog.askdirectory(parent=hwndparent)
        if path and path not in AskDirectorySelectBox['value']:
            AskDirectorySelectBox['value'] += (path + '/*.sp',)
            AskDirectorySelectBox.current(len(AskDirectorySelectBox['value']) - 1)
            self.outvar += (path + '/*.sp',)
            self.cfg_get.set('Output_Path', '%s'
                             % str(len(AskDirectorySelectBox['value']) - 1),
                             path + '/*.sp')
            self.cfg.save_config()

    @staticmethod
    def AskOrNotCheck(AskOrNotCheckVar,
                      AskDirectorySelectBox,
                      AskDirectorySelectButton):
        # -------------------------------------------------------------------------------
        # >
        # Method: AskOrNotCheck
        # Brief : Check the file diectory.
        # Param : AskOrNotCheckVar         : button int value
        #         AskDirectorySelectBox    : instance handle of dir combobox
        #         AskDirectorySelectButton : instance handle dir select button
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        if AskOrNotCheckVar.get() == 0:
            AskDirectorySelectBox.config(state=tk.DISABLED)
            AskDirectorySelectButton.config(state=tk.DISABLED)
        else:
            AskDirectorySelectBox.config(state=tk.NORMAL)
            AskDirectorySelectButton.config(state=tk.NORMAL)

    def ExecuteFile(self,
                    ExecuteState,
                    ObsSelectBoxVar,
                    NavSelectBoxVar,
                    AskOrNotCheckVar,
                    DirectorySelectBoxVar):
        # -------------------------------------------------------------------------------
        # >
        # Method: ExecuteFile
        # Brief : Execute RINEX file into .ksln.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        exten = "ksln"
        statemsg = ""
        state3 = ["","",""]
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

        obspath = ObsSelectBoxVar.get()
        navpath = NavSelectBoxVar.get()
        directory = obspath
        if AskOrNotCheckVar.get():
            directory = DirectorySelectBoxVar.get()


        directory = self.Dir_or_name_get(directory, 1)
        syssign = self.system.get(int(self.cfg_get['Options_Calc']['sat_system']))
        if int(self.cfg_get['Options_Draw']['Enable of track'])==1:
            exten="ssln"
        resname = syssign + '-' + self.Dir_or_name_get(obspath,0) + exten
        respath = (directory + resname)

        ExecuteState.config(text='Processing...... file : %s' %resname)

        dll = ct.cdll.LoadLibrary('./brdm2pos.dll')
        dll.brdm2pos.restype = ct.c_double
        match dll.brdm2pos(
            navpath.encode(),
            obspath.encode(),
            respath.encode(),
            int(self.cfg_get['Options_Calc']['Sat_system']),
            int(self.cfg_get['Options_Calc']['Elev_angle']),
            int(self.cfg_get['Options_Calc']['Iono_Model']),
            int(self.cfg_get['Options_Calc']['Trop_Model']),
            int(self.cfg_get['Options_Draw']['Enable of track'])
            ):
            case  0.0:
                ExecuteState.config(text='Generated successfully ! file : %s' %resname)
            case -1.0:
                ExecuteState.config(text='Error ! cant open nav file')
            case -2.0:
                ExecuteState.config(text='Error ! cant open obs file')
            case -3.0:
                ExecuteState.config(text='Error ! unsupported nav file')
            case -4.0:
                ExecuteState.config(text='Error ! no nav data')
            case -5.0:
                ExecuteState.config(text='Error ! unsupported obs file')
            case -6.0:
                ExecuteState.config(text='Error ! no obs data')
        ct.windll.kernel32.FreeLibrary('./brdm2pos.dll')

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

    def OpenkslnFile(self,
                     explot,nxplot,uxplot,satnplot,visbplot,
                     canvas0,canvas1,plotstate):
        # -------------------------------------------------------------------------------
        # >
        # Method: OpenkslnFile
        # Brief : Plot by open ksln as pos solution.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        path = filedialog.askopenfilename(title='Open as Pos Solution',
                                          filetypes=[('Solution File(*.ksln)', '*.ksln'),
                                                     ('All Files', '*.*')])
        if not path: return
        with open(path,'r')as f:
            while 1:
                line = f.readline()
                if line.find('APPROX POSITION XYZ')>=0:
                    apx = float(line[22:35])
                    apy = float(line[35:48])
                    apz = float(line[48:61])
                elif line.find('APPROX POSITION BLH')>=0:
                    apb = float(line[22:35])
                    apl = float(line[35:48])
                    aph = float(line[48:61])
                    S = np.array([
                        [-math.sin(apl)              , math.cos(apl)              , 0],
                        [-math.sin(apb)*math.cos(apl),-math.sin(apb)*math.sin(apl),math.cos(apb)],
                        [ math.cos(apb)*math.cos(apl), math.cos(apb)*math.sin(apl),math.sin(apb)]
                    ])
                elif line.find('INTERVAL')>=0:
                    ive = float(line[22:27])
                elif line.find('<END OF HEADER')>=0:
                    plotstate.config(text="Reading...")
                    break

            satnum = 0
            ENU = np.empty((3,0))
            EPO = np.empty((1,0))
            NUM = np.empty((1,0))
            while 1:
                line = f.readline()
                if line[0:1]=='>':
                    satnum = 0
                    EPO = np.hstack((EPO,[[float(line[1:6])]]))
                    plotstate.config(text='Reading...%5d/%5d Mode: Single solving'
                                          %(int(line[1:6]), int(86400/ive)))

                elif line[0:1]==self.system.get(int(
                        self.cfg_get['Options_Calc']['sat_system']
                )) and line.find('END')==-1 and line.find('Rec')==-1:
                    satnum += 1

                elif line.find('Rec:')>=0:
                    if line.find('insufficient')>=0:
                        ds = np.array([
                            [0],
                            [0],
                            [0]
                        ])
                    else:
                        ds = np.array([
                            [float(line[ 4:13])],
                            [float(line[14:23])],
                            [float(line[24:33])]
                        ])
                    ENU = np.hstack((ENU,S@ds))
                    NUM = np.hstack((NUM,[[satnum]]))
                elif line.find('END')>=0:
                    # plot on the e
                    # -------------------------------------------------------------------
                    explot.clear()
                    nxplot.clear()
                    uxplot.clear()
                    # plot on n
                    # -------------------------------------------------------------------
                    explot.plot(
                        EPO[0, :],
                        ENU[0, :],
                        marker='.',
                        linestyle=':',
                        ms=self.cfg_get['Options_Draw']['e_line'],
                        color=self.cfg_get['Options_Draw']['e_color'],
                        linewidth=self.cfg_get['Options_Draw']['e_line'],
                    )
                    explot.set_title(' E-W(m)', x=0.02, y=0, fontsize=8)
                    explot.grid(True, linestyle='--', alpha=0.7)
                    # plot on u
                    # -------------------------------------------------------------------
                    nxplot.plot(
                        EPO[0, :],
                        ENU[1, :],
                        marker='.',
                        linestyle=':',
                        ms=self.cfg_get['Options_Draw']['n_line'],
                        color=self.cfg_get['Options_Draw']['n_color'],
                        linewidth=self.cfg_get['Options_Draw']['n_line'],
                    )
                    nxplot.set_title(' N-S(m)', x=0.02, y=0, fontsize=8)
                    nxplot.grid(True, linestyle='--', alpha=0.7)
                    # plot on u
                    # -------------------------------------------------------------------
                    uxplot.plot(
                        EPO[0, :],
                        ENU[2, :],
                        marker='.',
                        linestyle=':',
                        ms=self.cfg_get['Options_Draw']['u_line'],
                        color=self.cfg_get['Options_Draw']['u_color'],
                        linewidth=self.cfg_get['Options_Draw']['u_line'],
                    )
                    uxplot.set_title(' U-D(m)', x=0.02, y=0, fontsize=8)
                    uxplot.grid(True, linestyle='--', alpha=0.7)
                    canvas0.draw()

                    satnplot.clear()
                    satnplot.plot(
                        EPO[0, :],
                        NUM[0, :],
                        ms=5,
                        marker='|',
                        linewidth=0,
                        linestyle=None,
                        color=self.cfg_get['Options_Draw']['sat_amount_color'],
                    )
                    satnplot.set_title('Valid Satellite Numbers', loc='left', fontsize=8)
                    satnplot.set_xlabel('Epochs')
                    satnplot.grid(True, linestyle='--', alpha=0.7)

                    canvas1.draw()

                    f.close()

                    plotstate.config(text="Plot   form: %s" % path)
                    break

    def _OpenkslnFile(self,
                      explot, nxplot, uxplot, satnplot, visbplot,
                      canvas0, canvas1, plotstate):
        T = threading.Thread(
            target=lambda :self.OpenkslnFile(
            explot,nxplot,uxplot,satnplot,visbplot,
            canvas0,canvas1,plotstate)
                             )
        T.start()

    def Plot2polar(self, sattrack, plotstate, canvas2):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        if self.cfg_get['Options_Draw']['Enable of track']=='0':
            plotstate.config(text="Track plot is not avaliable now, Please enable it.")
            return
        satprn = int(self.cfg_get['Options_Draw']['Track of prn'])
        anirat = int(self.cfg_get['Options_Draw']['Track sample rate'])
        system = self.system.get(int(self.cfg_get['Options_Calc']['sat_system']))

        path = filedialog.askopenfilename(title='Open as Sat Solution',
                                          filetypes=[('Solution File(*.ssln)', '*.ssln'),
                                                     ('All Files', '*.*')])
        if not path: return
        sattrack.clear()

        sattrack.coastlines(resolution='110m')
        sattrack.gridlines()

        with open(path,'r') as f:
            while 1:
                line = f.readline()

                if line.find('APPROX POSITION BLH')>=0:
                    apb = math.degrees( float(line[22:35]) )
                    apl = math.degrees( float(line[35:48]) )
                    plotstate.config(text="Plotting...")

                    sattrack.scatter(
                        apl,
                        apb,
                        color='r',
                        s=35,
                        transform=ccrs.PlateCarree()
                    )
                    sattrack.text(
                        apl,
                        apb,
                        blank*4+marker,
                        color='k',
                        fontsize=10,
                        fontweight='bold',
                        transform=ccrs.PlateCarree()
                    )
                    canvas2.draw()

                elif line.find('GENERATE SOURCE')>=0:
                    marker = line[22:26]

                elif line.find('INTERVAL')>=0:
                    ive = float(line[22:27])

                elif line.find('<END OF HEADER')>=0:
                    break

            epoch = 0
            while 1:
                line =f.readline()
                if line[0:1]==blank:
                    pass

                elif line[0:1]==system and line.find('END')==-1 and line.find('Rec')==-1:
                    epoch = int(line[41:46])
                    plotstate.config(text="Reading...%5d/%5d Mode: Sat track plot"
                                          % (int(line[41:46]), int(86400 / ive)))

                    if int(line[1:3])==satprn and epoch%anirat==0:
                        b = math.degrees( float(line[ 4:13]) )
                        l = math.degrees( float(line[14:23]) )
                        sattrack.scatter(
                            l,
                            b,
                            color='b',
                            s=2,
                            transform=ccrs.PlateCarree()
                        )
                        canvas2.draw()
                        text = sattrack.text(
                        l,
                        b,
                        4*blank+system+'%02d'%satprn,
                        color='k',
                        fontsize=10,
                        fontweight='bold',
                        transform=ccrs.PlateCarree()
                        )
                        point = sattrack.scatter(
                            l,
                            b,
                            color='b',
                            s=10,
                            transform=ccrs.PlateCarree()
                        )
                        canvas2.draw()
                        text.remove()
                        point.remove()
                    else:
                        pass

                elif line.find('END')>=0:
                    plotstate.config(text="Done ! Track plot form: sys=%s sat=%2d interval=%2d"
                                          %(system, satprn, anirat))

    def _Plot2polar(self, sattrack, plotstate, canvas2):
        T = threading.Thread(
            target=lambda :self.Plot2polar(sattrack, plotstate, canvas2)
        )
        T.start()

















