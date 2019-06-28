
# NGA CLASSES
from NGA_Utils.Text_Config import NGA_Text_Config

class NGA_Config_Stage:

    defaults = dict()
    
    def __init__(self):
        self.defaults = NGA_Text_Config(r"..\config\config.stage.defaults.txt")
        #print "-----"
        #self.defaults.recall_config()
        #print "-----"

