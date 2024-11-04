#  @ File : UI_processor.py
#
#  Copyright (c) 2024 KenanZhu. All Right Reserved.
#
#  @ Author       : KenanZhu
#  @ Time         : 2024/11/04
#  @ Brief        : RINEX file processor window class.
#  #
#  @ IDE          : PyCharm 2024.2.1 (Community Edition)
#
#  ----------------------------------------------------------------------------------------

### Std
from tkinter import ttk
from PIL import ImageTk
from base64 import b64decode

import tkinter as tk


# noinspection PyProtectedMember
class EXECUDUI:
    def __init__(self, hwndparent, cfg_get, func):
        # init
        # -------------------------------------------------------------------------------
        self.func = func
        self.cfg_get = cfg_get
        self.hwndparent = hwndparent

        self.exehwnd = None
        self.ObsSelectBoxVar = tk.StringVar()
        self.NavSelectBoxVar = tk.StringVar()
        self.AskOrNotCheckButtonVar = tk.IntVar()
        self.DirectorySelectBoxVar = tk.StringVar()

        self.initGUI()

    def initGUI(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.exehwnd = tk.Toplevel(self.hwndparent)
        self.exehwnd.title("RINEX Processor")
        self.exehwnd.resizable(0,0)
        self.func.Move_center(self.exehwnd,550,180)
        self.exehwnd.minsize(550,180)
        self.exehwnd.maxsize(550,180)

        ### Set icon
        icon_ico = (b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAADjsAAA47AAAAAAAAAAAAAAAAAAAAAAAAAA'
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
                     b'//9L6AAAF/////8=')
        icon_ico = b64decode(icon_ico)
        icon_ico = ImageTk.PhotoImage(data=icon_ico)
        self.exehwnd.tk.call('wm', 'iconphoto', self.exehwnd._w, icon_ico)

        self.initIO()

    def initIO(self):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        MainFrame = tk.Frame(self.exehwnd)
        MainFrame.pack()
        InputFrame = ttk.Frame(MainFrame)
        InputFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='1px', fill=tk.X)

        # Input Frame
        # -------------------------------------------------------------------------------
        ###  Observation file
        ObsInFrame = ttk.LabelFrame(InputFrame, text='RINEX Obs File')
        ObsInFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.X)
        ObsFileSelectBox = ttk.Combobox(
            ObsInFrame,
            width=70,
            height=4,
            values=self.func.obsvar,
            textvariable=self.ObsSelectBoxVar
        )
        ObsFileSelectBox.current(len(ObsFileSelectBox['value'])-1)
        ObsFileSelectBox.pack(side=tk.LEFT, anchor='w', padx='0px', pady='0px')
        ObsFileSelectButton = ttk.Button(
            ObsInFrame,
            text='...',
            width=3,
            command=lambda :self.func.GetObsFilePath(self.exehwnd, ObsFileSelectBox)
        )
        ObsFileSelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='0px')
        ### Navigation file
        NavInFrame = ttk.LabelFrame(InputFrame, text='RINEX Nav File')
        NavInFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.X)
        NavFileSelectBox = ttk.Combobox(
            NavInFrame,
            width=70,
            height=4,
            values=self.func.navvar,
            textvariable=self.NavSelectBoxVar
        )
        NavFileSelectBox.current(len(NavFileSelectBox['value'])-1)
        NavFileSelectBox.pack(side=tk.LEFT, anchor='w', padx='0px', pady='0px')
        NavFileSelectButton = ttk.Button(
            NavInFrame,
            text='...',
            width=3,
            command=lambda :self.func.GetNavFilePath(self.exehwnd, NavFileSelectBox)
        )
        NavFileSelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='0px')

        # Output Frame
        # -------------------------------------------------------------------------------
        OutputFrame = ttk.Frame(MainFrame)
        OutputFrame.pack(side=tk.BOTTOM, expand=tk.YES, padx='1px', pady='0px', fill=tk.X)

        FileOutFrame = ttk.LabelFrame(OutputFrame, text='Output Directory')
        FileOutFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.X)
        ## CheckButton Initialize
        AskOrNotCheckButton = ttk.Checkbutton(
            FileOutFrame,
            text='Directory',
            variable=self.AskOrNotCheckButtonVar,
            onvalue=1,
            offvalue=0,
            command=lambda :self.func.AskOrNotCheck(
                self.AskOrNotCheckButtonVar,
                AskDirectorySelectBox,
                AskDirectorySelectButton
            )
        )
        AskOrNotCheckButton.pack(side=tk.LEFT, anchor='w', padx='0px', pady='0px')
        AskDirectorySelectBox = ttk.Combobox(
            FileOutFrame,
            width=60,
            height=4,
            values=self.func.outvar,
            state=tk.DISABLED,
            textvariable=self.DirectorySelectBoxVar
        )
        AskDirectorySelectBox.current(len(AskDirectorySelectBox['value'])-1)
        AskDirectorySelectBox.pack(side=tk.LEFT, anchor='w', padx='0px', pady='0px')
        AskDirectorySelectButton = ttk.Button(
            FileOutFrame,
            text='...',
            width=3,
            state=tk.DISABLED,
            command=lambda :self.func.AskDirectory(self.exehwnd, AskDirectorySelectBox)
        )
        AskDirectorySelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='0px')

        # Execute frame
        # -------------------------------------------------------------------------------
        ExeFrame = ttk.Frame(OutputFrame)
        ExeFrame.pack(side=tk.TOP, expand=tk.YES, padx='1px', pady='0px', fill=tk.X)

        ExitButton = ttk.Button(
            ExeFrame,
            text='Exit',
            width=10,
            command=self.exehwnd.destroy
        )
        ExitButton.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        ExecuteButton = ttk.Button(
            ExeFrame,
            text='Execute',
            width=10,
            command=lambda :self.func._ExecuteFile(
                ExecuteState,
                self.ObsSelectBoxVar,
                self.NavSelectBoxVar,
                self.AskOrNotCheckButtonVar,
                self.DirectorySelectBoxVar
            )
        )
        ExecuteButton.pack(side=tk.LEFT, expand=tk.YES, padx='1px', pady='0px')

        # State bar
        # -------------------------------------------------------------------------------
        StateFrame = ttk.Frame(OutputFrame)
        StateFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')
        ExecuteState = ttk.Label(StateFrame, text="None")
        ExecuteState.pack(side=tk.LEFT, anchor='nw')