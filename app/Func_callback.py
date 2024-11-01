#
#
#
#
#
#
#
#
#
#-----------------------------------------------------------------#

### Std
import threading

import ctypes as ct
import tkinter as tk

from tkinter import filedialog
from tkinter import colorchooser

class CALLBACK:
    def __init__(self, cfg, cfg_get):
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

    @staticmethod
    def Move_center(hwnd, win_x, win_y):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Param :
        #
        #
        # Return:
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        position_x = int((hwnd.winfo_screenwidth() - win_x) / 2)
        position_y = int((hwnd.winfo_screenheight() - win_y) / 2)
        hwnd.geometry(f'{win_x}x{win_y}+{position_x}+{position_y}')

    def Calcuconfirm(self, cionbox, ctrobox, canglebox, systemv):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Param :
        #
        #
        # Return:
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------

        self.cfg_get.set('Options_Calc', 'Iono_model', self.ioncormode.get(cionbox.get()))
        self.cfg_get.set('Options_Calc', 'Trop_model', self.trocormode.get(ctrobox.get()))
        self.cfg_get.set('Options_Calc', 'Elev_angle', canglebox.get())
        self.cfg_get.set('Options_Calc', 'Sat_system', str(systemv.get()))
        self.cfg.save_config()

    def Colorchoose(self, hwndparent, i, colorlab, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Param : hwndparent :
        #         i          : 0==e & 1==n & 2==u & 3==satn
        #         colorlab   :
        #         mode       :
        # Return:
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
        # Method:
        # Brief :
        # Param : entry0 : spinbox handle
        #         entry1 : spinbox handle
        #         entry2 : spinbox handle
        #         mode   : 0==undo & 1==confirm
        # Return:
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

    def Dir_or_name_get(self, path, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Param : path :
        #         mode : 0==get file name & 1==get file dir
        # Return:
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
        # Method:
        # Brief :
        # Param :
        # Return:
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
        # Method:
        # Brief :
        # Param :
        # Return:
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
        # Method:
        # Brief :
        # Param :
        # Return:
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

    def AskOrNotCheck(self,
                      AskOrNotCheckVar,
                      AskDirectorySelectBox,
                      AskDirectorySelectButton):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Param :
        # Return:
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
        # Method:
        # Brief :
        # Param :
        #
        # Return:
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
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
        resname = syssign + '-' + self.Dir_or_name_get(obspath,0) + 'sp'
        respath = (directory + resname)

        ExecuteState.config(text='Processing...... file : %s' %resname)

        dll = ct.cdll.LoadLibrary('./brdm2pos.dll')
        dll.brdm2pos.restype = ct.c_double
        match dll.brdm2pos(
            navpath.encode(),
            obspath.encode(),
            respath.encode(),
            int(self.cfg_get['Options_Calc']['sat_system']),
            int(self.cfg_get['Options_Calc']['elev_angle'])
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