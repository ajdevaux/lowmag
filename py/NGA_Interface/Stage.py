
# NGA CLASSES

from NGA_Config.Py import NGA_Config_Py

from NGA_Config.Stage import NGA_Config_Stage

from Stages.Virtual_Stage import Virtual_Stage
from Stages.MFC_2000 import MFC_2000
from Stages.MMC_100 import MMC_100
from Stages.SMC_Pollux import SMC_Pollux
from Stages.MMC_Pollux_Hybrid import MMC_Pollux_Hybrid
from Stages.MFC_Pollux_Hybrid import MFC_Pollux_Hybrid

class NGA_Interface_Stage:

    stage = None
    py_cfg = None
    port_cfg = None

    def __init__(self):
        # load defaults
        self.stage = None
        self.py_cfg = NGA_Config_Py()
        self.stage_cfg = NGA_Config_Stage()
        
        self.select_stage_and_load()
        
    
    def select_stage_and_load(self):
        stage_loaded = False
        
        stage_cnt = self.stage_cfg.defaults.config
        for key, value in stage_cnt.iteritems():
            stage_loaded = self.load_stage(key)
                
        if stage_loaded == False:
            print "STAGE: Error Loading Stage, Loading Virtual Stage"
            self.stage = Virtual_Stage()
    
    def load_stage(self,stage_to_load):
        stage_loaded = False
        if (self.stage_cfg.defaults.config[stage_to_load] != 'COM0'):
            if (stage_to_load == Virtual_Stage.STAGE_MFC2000):
                self.stage = MFC_2000()
                stage_loaded = self.stage.loaded
            elif (stage_to_load == Virtual_Stage.STAGE_MMC100):
                self.stage = MMC_100()
                stage_loaded = self.stage.loaded
            elif (stage_to_load == Virtual_Stage.STAGE_SMC_POLLUX):
                self.stage = SMC_Pollux()
                stage_loaded = self.stage.loaded
            elif (stage_to_load == Virtual_Stage.STAGE_MMC_POLLUX_HYBRID):
                self.stage = MMC_Pollux_Hybrid()
                stage_loaded = self.stage.loaded
            elif (stage_to_load == Virtual_Stage.STAGE_MFC_POLLUX_HYBRID):
                self.stage = MFC_Pollux_Hybrid()
                stage_loaded = self.stage.loaded
            elif (stage_to_load == Virtual_Stage.STAGE_VIRTUAL):
                self.stage = Virtual_Stage()
                stage_loaded = self.stage.loaded
        return stage_loaded

    #def unload_stage(self):
    #    if (self.stage_name == Virtual_Stage.STAGE_MMC100):
    #        self.stage.close()
    
    def stage_name(self):
        return self.stage.stage_name()
    
    def position(self):
        self.stage.get_position()
        return [self.stage.x_pos, self.stage.y_pos, self.stage.z_pos]
    
    def actual_position(self):
        self.stage.get_actual_position()
        return [self.stage.actual_x_pos, self.stage.actual_y_pos, self.stage.actual_z_pos]
    
    def move_x(self, x_pos):
        return self.stage.move_x(x_pos)
    def move_y(self, y_pos):
        return self.stage.move_y(y_pos)
    def move_z(self, z_pos):
        return self.stage.move_z(z_pos)

    def check_err(self):
        err = self.stage.check_err(1)
        if(err == 0):
            err = self.stage.check_err(2)
            if(err == 0):
                err = self.stage.check_err(3)
                if(err == 0):
                    return 0
                else:
                    return err
            else:
                return err
        else:
            return err
         
    def move_rel_x(self, x_pos):
        self.stage.move_rel_x(x_pos)
    def move_rel_y(self, y_pos):
        self.stage.move_rel_y(y_pos)
    def move_rel_z(self, z_pos):
        self.stage.move_rel_z(z_pos)  
    def zero(self):
        self.stage.zero()
              
    def home(self):
        self.stage.home()
    def abort(self):
        self.stage.abort()
    def status_x(self):
        return self.stage.update_status('x')
    def status_y(self):
        return self.stage.update_status('y')
    def status_z(self):
        return self.stage.update_status('z')
    
    def program12(self):
        self.stage.program12()    
    def program13(self):
        self.stage.program13()        
