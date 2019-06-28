
# NGA CLASSES
from NGA_Utils.Text_Config import NGA_Text_Config
from NGA_Utils.Text_Config_Save import NGA_Text_Config_Save

class NGA_Config_Py:

    defaults = dict()
    fn = r"..\config\config.py.txt"
    
    def __init__(self):
        self.defaults = NGA_Text_Config(self.fn)
        #print "-----"
        #self.defaults.recall_config()
        #print "-----"

    def save(self):
        tcs = NGA_Text_Config_Save(self.fn, self.defaults.config)
