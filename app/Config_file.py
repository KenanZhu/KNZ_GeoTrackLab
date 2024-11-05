#  @ File : Config_file.py
#
#  Copyright (c) 2024 KenanZhu. All Right Reserved.
#
#  @ Author       : KenanZhu
#  @ Time         : 2024/11/04
#  @ Brief        : Initialize the configuration file.
#  #
#  @ IDE          : PyCharm 2024.2.1 (Community Edition)
#
#  ----------------------------------------------------------------------------------------

from configparser import ConfigParser

class Configinit:
    def __init__(self, config_filepath):
        # init
        # -------------------------------------------------------------------------------
        self.config = ConfigParser()
        self.config_filepath = config_filepath### Config file path

    def load_config(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: load_config
        # Brief : Load config file, if not exist, regenerate the config.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        try:
            with open(self.config_filepath, 'r'):
                pass
        except FileNotFoundError:
            self.create_config()

    def get_config(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: get_config
        # Brief : Capture config instance handle.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.config.read(self.config_filepath)
        return self.config

    def create_config(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: create_config
        # Brief : Generate the initial config file.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        ### Config for software info
        self.config.add_section('INFO')
        self.config.set('INFO', 'Version','1.5.5.0')
        self.config.add_section('Options_Calc')
        ### Config for calculate param
        self.config.set('Options_Calc', 'Iono_model', '0')
        self.config.set('Options_Calc', 'Trop_model', '0')
        self.config.set('Options_Calc', 'Elev_angle', '0')
        self.config.set('Options_Calc', 'Sat_system', '0')
        ### Config for plot param
        self.config.add_section('Options_Draw')
        self.config.set('Options_Draw', 'E_Color', '#0080FF')
        self.config.set('Options_Draw', 'N_Color', '#0080FF')
        self.config.set('Options_Draw', 'U_Color', '#0080FF')
        self.config.set('Options_Draw', 'E_Line', '0.80')
        self.config.set('Options_Draw', 'N_Line', '0.80')
        self.config.set('Options_Draw', 'U_Line', '0.80')
        self.config.set('Options_Draw', 'Sat_Amount_Color', '#0080FF')
        self.config.set('Options_Draw', 'Enable of track', '0')
        self.config.set('Options_Draw', 'Track of prn', '01')
        self.config.set('Options_Draw', 'Track sample rate','10')

        ### Config for input path
        self.config.add_section('Input_Obs_Path')
        self.config.set('Input_Obs_Path', '0', '')
        self.config.add_section('Input_Nav_Path')
        self.config.set('Input_Nav_Path', '0', '')
        ### Config for output path
        self.config.add_section('Output_Path')
        self.config.set('Output_Path','0','')

        with open(self.config_filepath, 'w') as configfile:
            self.config.write(configfile)
        return

    def save_config(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: save_config
        # Brief : Save changes of config file.
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        with open(self.config_filepath, 'w') as configfile:
            self.config.write(configfile)











