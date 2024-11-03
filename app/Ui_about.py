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
import tkinter as tk

class ABODUI:
    def __init__(self, hwndparent, cfg_get, func):
        # init
        # -------------------------------------------------------------------------------
        self.func = func
        self.cfg_get = cfg_get
        self.hwndparent = hwndparent

        self.initGUI()

    def initGUI(self):
        abo = tk.Toplevel(self.hwndparent)
        abo.title("About")
        abo.attributes('-toolwindow', 2)
        self.func.Move_center(abo, 200, 100)
        abo.minsize(200, 100)
        abo.maxsize(200, 100)

        About = tk.Label(abo,
                         text="\nKNZ_GeoTrackLab %s"
                              "\n"
                              "\nCopyright (c) 2024 by KenanZhu"
                              "\nAll Right Reserved."
                              % self.cfg_get['INFO']['Version']
                         )
        About.pack(side=tk.TOP, expand=tk.YES)