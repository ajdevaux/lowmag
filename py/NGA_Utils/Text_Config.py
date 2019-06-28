import os
import io


class NGA_Text_Config:

    fn = r"..\config\config.txt"
    config = dict()

    def __init__(self, fn):
        self.config = dict()
        self.fn = fn
        self.loadConfig()
        
    def loadConfig(self):

        if (os.path.isfile(self.fn)):
            f = open(self.fn, 'r')
            for line in f:
                #print line,
                if (line.count(":") > 0):
                    tmp = line.split(":")
                    ttnum = 0
                    dic_value = ""
                    for entry in tmp:
                        clean_word = entry.strip()
                        ttnum = ttnum + 1
                        if (ttnum == 1):
                            dic_entry = clean_word
                        if (ttnum == 2):
                            dic_value = clean_word                
                    self.config[dic_entry] = dic_value
                    
            f.close()

    def recall_config(self):
        for key  in self.config:
            print key + ":" +  self.config[key]
