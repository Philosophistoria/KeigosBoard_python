from .rehamove_integration_lib.builds.python.linux_amd64 import rehamove 
import sys


class DRehamove():
    __instance = []
    __num_inst = 0
    def __new__(cls, port:str, logger = sys.stderr):
        cls.__num_inst += 1
        if str.upper(port) == "DEBUG":
            cls.__instance += [super().__new__(cls)]
        else:
            cls.__instance += [rehamove.Rehamove(port_name=port, logger=logger)]
        return cls.__instance[cls.__num_inst - 1]
            

    def __init__(self, port:str="DEBUG", logger = sys.stderr) -> None:
        self.logger = logger
        self.log("REHAMOVE DUMMY: port:" + port )

    def set_pulse(self, intensity:float, pulsewidth:int) -> None:
        self.log("REHAMOVE DUMMY: intensity:   " + str(intensity))
        self.log("REHAMOVE DUMMY: pulse width: " + str(pulsewidth))
        pass

    def change_mode(self, mode:int):
        self.log("REHAMOVE DUMMY: " + repr(mode))
        pass

    def start(self, channel:str, wave_period:float) -> None:
        self.log("REHAMOVE DUMMY: run ")

    def end(self) -> None:
        self.log("REHAMOVE DUMMY: stop ")
    
    def update(self) -> None:
        self.log("REHAMOVE DUMMY: update")
        pass
    def log(self, text:str) -> None:
        self.logger.write(bcolors.OKCYAN + text + bcolors.ENDC + "\n")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
