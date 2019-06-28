
class NGA_Text_Config_Save:

    fn = r"..\config\config.txt"

    def __init__(self, fn, config):
        self.fn = fn
        self.saveConfig(config)
        
    def saveConfig(self, config):

        f = open(self.fn, 'w')
        for key in config:
            #print key + ":" + config[key] + "\n\r"
            f.write(key + ":" + config[key] + "\n\r")
        f.close()

