import os
import io


class NGA_Stage_Status:

    config = dict()

    def __init__(self):
        self.config = dict()
        self.loadConfig()
        
    def loadConfig(self):
        # MFC 2000
        self.config['axis_moving'] = False
        self.config['axis_enabled'] = False
        self.config['motor_enabled'] = False
        self.config['joystick_enabled'] = False
        self.config['motor_ramping_up'] = False
        self.config['motor_ramping_down'] = False
        self.config['upper_limit_swtich_closed'] = False
        self.config['lower_limit_swtich_closed'] = False
        
        # SMC_POLLUX
        self.config['closed_loop_in_window'] = False
        
        # MMC_100
        self.config['error'] = False
        self.config['program_running'] = False
        self.config['deceleration'] = False
        self.config['constant_velocity'] = False
        self.config['acceleration'] = False