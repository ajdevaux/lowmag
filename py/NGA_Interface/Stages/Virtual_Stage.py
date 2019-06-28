
# NGA CLASSES

from time import sleep

from NGA_Utils.Stage_Status import NGA_Stage_Status

class Virtual_Stage:

    STAGE_VIRTUAL = 'virtual'
    STAGE_POLLUX = 'pollux'
    STAGE_MMC100 = 'mmc100'
    STAGE_MFC2000 = 'mfc2000'
    STAGE_MMC_POLLUX_HYBRID = 'mmc_pollux_hybrid'
    STAGE_MFC_POLLUX_HYBRID = 'mfc_pollux_hybrid'
    name = "virtual"
    loaded = False
    interface = ""
    x_pos = 0.0
    y_pos = 0.0
    z_pos = 0.0
    actual_x_pos = 0.0
    actual_y_pos = 0.0
    actual_z_pos = 0.0
    x_speed = 2
    y_speed = 2
    z_speed = 2
    status = dict()
    
    STAGE_SPEED_HI = 2.0
    STAGE_SPEED_MED = 1.0
    STAGE_SPEED_SLOW = 0.5

    def __init__(self):
        self.interface = self.STAGE_VIRTUAL
        self._init()
        self.load()
        

    def _init(self):
        self.loaded = False
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
        self.actual_x_pos = 0.0
        self.actual_y_pos = 0.0
        self.actual_z_pos = 0.0
        self.x_speed = self.STAGE_SPEED_MED
        self.y_speed = self.STAGE_SPEED_MED
        self.z_speed = self.STAGE_SPEED_MED
        self.status = dict()
        print "Stage: Config:", self.interface
    
    '''
    load
    name
    move_rel_x
    move_rel_y
    move_rel_z
    move_x
    move_y
    move_z
    move_serial_x_y_z
    move_parrallel_x_y_z
    get_position (optional)
    get_actual_position
    abort
    home
    zero
    program12
    program13
    status
    hi_speed
    slow_speed
    med_speed
    '''
    
  
    def load(self):
        self.loaded = True
        print "Stage: Loaded: Virtual Stage"

    def stage_name(self):
        return self.name

    def move_rel_x(self, x_pos):
        sleep(abs(x_pos/self.x_speed))
        self.x_pos = self.x_pos + x_pos
        
    def move_rel_y(self, y_pos):
        sleep(abs(y_pos/self.y_speed))
        self.y_pos = self.y_pos + y_pos
    
    def move_rel_z(self, z_pos):
        sleep(abs(z_pos/self.z_speed))
        self.z_pos = self.z_pos + z_pos
        
    def move_x(self, x_pos):
        sleep(abs(x_pos-self.x_pos)/self.x_speed)
        self.x_pos = x_pos
        
    def move_y(self, y_pos):
        sleep(abs(y_pos-self.y_pos)/self.y_speed)
        self.y_pos = y_pos
    
    def move_z(self, z_pos):
        sleep(abs(z_pos-self.z_pos)/self.z_speed)
        self.z_pos = z_pos
    
    def move_serial_x_y_z(self, x_pos, y_pos, z_pos):
        self.move_x(x_pos)
        self.move_y(y_pos)
        self.move_z(z_pos)
    
    def move_parrallel_x_y_z(self, x_pos, y_pos, z_pos):       
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        
    def get_position(self):
        # this is the requested positions
        self.x_pos = self.x_pos
        self.y_pos = self.y_pos
        self.z_pos = self.z_pos
        
    def get_actual_position(self):
        # this is the actual positions from the stage
        # virtual has already got this info
        sleep(0.05)
        self.actual_x_pos = self.x_pos
        self.actual_y_pos = self.y_pos
        self.actual_z_pos = self.z_pos
    
    def abort(self):
        print "Stage: Abort!"
        #for virtual, nothing to stop really
    
    def home(self):
        self.zero()
        
    def zero(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
        
    # we'll use programs to define particle functions
    def program12(self):
        print "Stage: Program: This program will enable lock-mode the System"
    def program13(self):
        print "Stage: Program: This program will unlock the System"
     
    def update_status(self, xyz_str):
        stage_status = NGA_Stage_Status()
        self.status = stage_status.config
        return self.status
    
    def hi_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = self.STAGE_SPEED_HI
        elif (xyz_str == 'y'):
            self.y_speed = self.STAGE_SPEED_HI
        elif (xyz_str == 'z'):
            self.z_speed = self.STAGE_SPEED_HI
    def med_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = self.STAGE_SPEED_MED
        elif (xyz_str == 'y'):
            self.y_speed = self.STAGE_SPEED_MED
        elif (xyz_str == 'z'):
            self.z_speed = self.STAGE_SPEED_MED
    def slow_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = self.STAGE_SPEED_SLOW
        elif (xyz_str == 'y'):
            self.y_speed = self.STAGE_SPEED_SLOW
        elif (xyz_str == 'z'):
            self.z_speed = self.STAGE_SPEED_SLOW
        
    def print_location(self):
        print "Stage: Pos(x,y,z): {0:.6f},{1:.6f},{2:.6f}".format(self.x_pos, self.y_pos, self.z_pos)
