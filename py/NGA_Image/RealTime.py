
import subprocess

class NGA_RealTime:

    realtime_executable = r"..\bin\FlyCap2RealTime.exe"
    
    def __init__(self):
        self.load()

    def load(self):
        self.realtime_output = subprocess.Popen(self.realtime_executable)
        
    def close(self):
        self.realtime_output.terminate()
