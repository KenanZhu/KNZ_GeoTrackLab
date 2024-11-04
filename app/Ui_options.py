#  @ File : UI_options.py
#
#  Copyright (c) 2024 KenanZhu. All Right Reserved.
#
#  @ Author       : KenanZhu
#  @ Time         : 2024/11/04
#  @ Brief        : Plot options window class.
#  #
#  @ IDE          : PyCharm 2024.2.1 (Community Edition)
#
#  ----------------------------------------------------------------------------------------

### Std
from PIL import ImageTk
from tkinter import ttk
from base64 import b64decode

import tkinter as tk


# noinspection PyProtectedMember
class OPTGUI:
    def __init__(
            self,
            hwndparent,
            cfg_get,
            func
    ):
        # init
        # -------------------------------------------------------------------------------
        self.func = func
        self.cfg_get = cfg_get
        self.hwndparent = hwndparent

        self.PlotFrame = None
        self.CalcuFrame = None

        self.systemv = None
        self.ctrobox = None
        self.cionbox = None
        self.opthwnd = None
        self.canglebox = None
        self.angleentry = None

        self.ulinewidth = None
        self.nlinewidth = None
        self.elinewidth = None

        self.initGUI()

    def initGUI(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        ### Set size
        self.opthwnd = tk.Toplevel(self.hwndparent)
        self.opthwnd.title("Options")
        self.opthwnd.resizable(0,0)
        self.func.Move_center(self.opthwnd,320,250)
        self.opthwnd.minsize(320,250)
        self.opthwnd.maxsize(320,250)
        ### Set icon
        icon_ico = (b'AAABAAEAICAAAAAAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAADjsAAA47AAAAAA'
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
        icon_ico = b64decode(icon_ico)
        icon_ico = ImageTk.PhotoImage(data=icon_ico)
        self.opthwnd.tk.call('wm', 'iconphoto', self.opthwnd._w, icon_ico)
        ### Main window
        self.initOPTION()
        self.initCONFIRM()

    def initOPTION(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        Optionscards = tk.ttk.Notebook(self.opthwnd)

        # Calcu options card
        # -------------------------------------------------------------------------------
        self.initCARDCALCU()
        Optionscards.add(self.CalcuFrame, text='Calc options')
        # Plot options card
        # -------------------------------------------------------------------------------

        self.initCARDDRAW()
        Optionscards.add(self.PlotFrame, text='Draw options')
        Optionscards.pack(fill=tk.BOTH, expand=True, padx='2px', pady='0px')

    def initCARDCALCU(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.CalcuFrame = tk.Frame(self.opthwnd)
        # Iono option frame
        # -------------------------------------------------------------------------------
        self.IONOOPT()
        # Trop option frame
        # -------------------------------------------------------------------------------
        self.TROPOPT()
        # Elev option frame
        # -------------------------------------------------------------------------------
        self.HANGOPT()
        # Syst option frame
        # -------------------------------------------------------------------------------
        self.SYSOPT()

    def IONOOPT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # ION correction frame#
        IonoFrame = ttk.Frame(self.CalcuFrame)
        IonoFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)
        ioncor = ttk.Label(IonoFrame, text='Ionosphere Correction')
        ioncor.pack(side=tk.LEFT, anchor='w', padx='1px')

        self.cionbox = ttk.Combobox(IonoFrame, width=15, height=4)
        self.cionbox['state'] = 'readonly'
        self.cionbox['value'] = ('OFF', 'Ion-Free LC', 'Broadcast')
        self.cionbox.current(self.cfg_get['Options_Calc']['iono_model'])
        self.cionbox.pack(side=tk.RIGHT, anchor='e')

    def TROPOPT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # TRO correction frame#
        TropFrame = ttk.Frame(self.CalcuFrame)
        TropFrame.pack( side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)
        ioncor = ttk.Label(TropFrame, text='Troposphere Correction')
        ioncor.pack(side=tk.LEFT, anchor='w', padx='1px')

        self.ctrobox = ttk.Combobox(TropFrame, width=15, height=4)
        self.ctrobox['state'] = 'readonly'
        self.ctrobox['value'] = ('OFF', 'Hopfield', 'Saastamoinen')
        self.ctrobox.current(self.cfg_get['Options_Calc']['trop_model'])
        self.ctrobox.pack(side=tk.RIGHT, anchor='e')

    def HANGOPT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # Angle of elevation frame
        SatElevFrame = ttk.Frame(self.CalcuFrame)
        SatElevFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)
        h_angle = ttk.Label(SatElevFrame, text='Satellite Elevation(°) / #')
        h_angle.pack(side=tk.LEFT, anchor='w', padx='1px')

        self.angleentry = ttk.Entry(SatElevFrame, width=8)
        self.angleentry.pack(side=tk.RIGHT, anchor='w')

        self.canglebox = ttk.Combobox(SatElevFrame, width=6, height=10)
        self.canglebox['state'] = 'readonly'
        self.canglebox['value'] = (
            '00', '05', '10', '15',
            '20', '25', '30', '35',
            '40', '45', '50', '55',)
        pos = int(self.cfg_get['Options_Calc']['elev_angle'])/5
        self.canglebox.current(int(pos))
        self.canglebox.pack(side=tk.RIGHT,anchor='e')

    def SYSOPT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # GNSS Options
        SystemFrame = ttk.LabelFrame(self.CalcuFrame, text='Satellite system', labelanchor='nw')
        SystemFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='2px', fill=tk.X)

        satsys = [("GPS", 1), ("GLO", 4), ("BeiDou", 2), ("Galileo", 3), ("SBAS", 5)]
        self.systemv = tk.IntVar()
        for sys, num in satsys:

            radio_button = ttk.Radiobutton(SystemFrame, text=sys, variable=self.systemv, value=num)
            radio_button.pack(side=tk.LEFT, padx='3px', anchor='w')

        self.systemv.set(self.cfg_get['Options_Calc']['sat_system'])

    def initCARDDRAW(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.PlotFrame = tk.Frame(self.opthwnd)

        self.initDRAWCOLOR()
        self.initDRAWLINE()

    def initDRAWLINE(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # Line's weight options#
        LineoptFrame = ttk.LabelFrame(self.PlotFrame, text='Draw configs', labelanchor='nw')
        LineoptFrame.pack(side=tk.RIGHT, expand=tk.YES, padx='1px', pady='1px', fill=tk.Y)

        EFrame = tk.Frame(LineoptFrame)
        EFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        elinewopt = tk.Label(
            EFrame,
            text='Eline:',
            width=5,
            height=1
        )
        elinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.elinewidth = ttk.Spinbox(
            EFrame,
            from_=0,
            to=10,
            increment=0.01,
            width=10
        )
        self.elinewidth.set(self.cfg_get['Options_Draw']['e_line'])
        self.elinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        NFrame = tk.Frame(LineoptFrame)
        NFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        nlinewopt = tk.Label(
            NFrame,
            text='Nline:',
            width=5,
            height=1
        )
        nlinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.nlinewidth = ttk.Spinbox(
            NFrame,
            from_=0,
            to=10,
            increment=0.01,
            width=10
        )
        self.nlinewidth.set(self.cfg_get['Options_Draw']['n_line'])
        self.nlinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        UFrame = tk.Frame(LineoptFrame)
        UFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ulinewopt = tk.Label(
            UFrame,
            text='Uline:',
            width=5,
            height=1
        )
        ulinewopt.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')
        self.ulinewidth = ttk.Spinbox(
            UFrame,
            from_=0,
            to=10,
            increment=0.01,
            width=10
        )
        self.ulinewidth.set(self.cfg_get['Options_Draw']['u_line'])
        self.ulinewidth.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        LineCon = tk.Frame(LineoptFrame)
        LineCon.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        linewre = ttk.Button(
            LineCon,
            text='Undo',
            width=10,
            command=lambda :self.func.Linewchoose(
                self.elinewidth,
                self.nlinewidth,
                self.ulinewidth,
                0
            )
        )
        linewre.pack(side=tk.LEFT, expand=tk.YES, padx='1px')

    def initDRAWCOLOR(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        # Satnum plot options#
        SatvisFrame = ttk.LabelFrame(self.PlotFrame, text='Satn configs', labelanchor='nw')
        SatvisFrame.pack(side=tk.BOTTOM, expand=tk.YES, padx='1px', pady='1px', fill=tk.BOTH)

        SatnFrame = tk.Frame(SatvisFrame)
        SatnFrame.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')
        satncollab = tk.Label(
            SatnFrame,
            width=5,
            height=1,
            bg=self.cfg_get['Options_Draw']['sat_amount_color'])
        satncollab.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        satncolopt = ttk.Button(
            SatnFrame,
            text='Satn Color',
            width=10,
            command=lambda :self.func.Colorchoose(self.opthwnd, 3, satncollab, 1)
        )
        satncolopt.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')

        SatviCon = tk.Frame(SatvisFrame)
        SatviCon.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        satviopt = ttk.Button(
            SatviCon,
            text='Undo',
            width=10,
            command=lambda :self.func.Colorchoose(self.opthwnd, 3, satncollab, 0)
        )
        satviopt .pack(side=tk.LEFT, expand=tk.YES, padx='1px')

        # Line's colors options#
        LinecolorFrame = ttk.LabelFrame(self.PlotFrame, text='ENU colors', labelanchor='nw')
        LinecolorFrame.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='1px', fill=tk.Y)

        EFrame = tk.Frame(LinecolorFrame)
        EFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ecollab = tk.Label(
            EFrame,
            width=5,
            height=1,
            bg=self.cfg_get['Options_Draw']['e_color'])
        ecollab.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        ecolopt = ttk.Button(
            EFrame,
            text='E Color',
            width=10,
            command=lambda :self.func.Colorchoose(self.opthwnd, 0, ecollab, 1)
        )
        ecolopt.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')

        NFrame = tk.Frame(LinecolorFrame)
        NFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ncollab = tk.Label(
            NFrame,
            width=5,
            height=1,
            bg=self.cfg_get['Options_Draw']['n_color']
        )
        ncollab.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        ncolopt = ttk.Button(
            NFrame,
            text='N Color',
            width=10,
            command=lambda :self.func.Colorchoose(self.opthwnd, 1, ncollab, 1)
        )
        ncolopt.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')


        UFrame = tk.Frame(LinecolorFrame)
        UFrame.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        ucollab = tk.Label(
            UFrame,
            width=5,
            height=1,
            bg=self.cfg_get['Options_Draw']['u_color']
        )
        ucollab.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')
        ucolopt = ttk.Button(
            UFrame,
            text='U Color',
            width=10,
            command=lambda :self.func.Colorchoose(self.opthwnd, 2, ucollab, 1)
        )
        ucolopt.pack(side=tk.RIGHT, expand=tk.YES, padx='5px', pady='0px')

        ColorCon = tk.Frame(LinecolorFrame)
        ColorCon.pack(side=tk.TOP, expand=tk.YES, padx='5px', pady='0px')
        colorcon = ttk.Button(
            ColorCon,
            text='Undo',
            width=10,
            command=lambda :[
                self.func.Colorchoose(self.opthwnd, 0, ecollab, 0),
                self.func.Colorchoose(self.opthwnd, 1, ncollab, 0),
                self.func.Colorchoose(self.opthwnd, 2, ucollab, 0),
            ]
        )
        colorcon.pack(side=tk.LEFT, expand=tk.YES, padx='5px', pady='0px')

    def initCONFIRM(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        ConfirmFrame = ttk.Frame(self.opthwnd)
        ConfirmFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.Y)
        TotalCancel = ttk.Button(
            ConfirmFrame,
            text='Cancel',
            width=10,
            command=lambda :[
                self.opthwnd.destroy()
            ]
        )
        TotalCancel.pack(side=tk.RIGHT, padx='1px', anchor='e')
        TotalCon = ttk.Button(
            ConfirmFrame,
            text='Confirm',
            width=10,
            command=lambda :[
                self.func.Colorchoose(self.opthwnd, 0, None, 2),
                self.func.Linewchoose(
                    self.elinewidth,
                    self.nlinewidth,
                    self.ulinewidth,
                    1
                ),
                self.func.Calcuconfirm(
                    self.cionbox,
                    self.ctrobox,
                    self.canglebox,
                    self.systemv
                ),
                self.opthwnd.destroy()
            ]
        )
        TotalCon.pack(side=tk.RIGHT, padx='1px', anchor='e')