from .rehamove_integration_lib.builds.python.linux_amd64 import rehamove 
import sys
from . import utils
from .utils import bcolors


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
        utils._logger = logger
        utils.log("REHAMOVE DUMMY: port:" + port, color=bcolors.CYAN)

    def set_pulse(self, intensity:float, pulsewidth:int) -> None:
        utils.log("REHAMOVE DUMMY: intensity:   " + str(intensity), color=bcolors.CYAN)
        utils.log("REHAMOVE DUMMY: pulse width: " + str(pulsewidth),color=bcolors.CYAN)
        pass

    def change_mode(self, mode:int):
        utils.log("REHAMOVE DUMMY: " + repr(mode),color=bcolors.CYAN)
        pass

    def start(self, channel:str, wave_period:float) -> None:
        utils.log("REHAMOVE DUMMY: run ",   color=bcolors.CYAN)

    def end(self) -> None:
        utils.log("REHAMOVE DUMMY: stop ",  color=bcolors.CYAN)
    
    def update(self) -> None:
        utils.log("REHAMOVE DUMMY: update", color=bcolors.CYAN)
        pass
