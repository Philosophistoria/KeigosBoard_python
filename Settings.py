from .com_esp32_switch_board import REACTION_MODE
class SwitchBoard:
    Numof_channels:int = 12
    COM_Port:str = "/dev/ttyS9"
    #COM_Port:str = "DEBUG"
    Baudrate:int = 1500000 #921600
    #   With this mode, the switch board not only echo the header, 
    #   it returns some reactions on every request. 
    #   This is good for debug or something
    #echo_mode = REACTION_MODE.ON_EVERY_REQUEST 
    #   With this mode, nothing is returns from switch board.
    #Reaction_Mode:REACTION_MODE = REACTION_MODE.NO_REACTION
    Reaction_Mode:REACTION_MODE = REACTION_MODE.NO_REACTION
import sys
class Rehamove:
    #COM_Port:str = "/dev/ttyS10"
    COM_Port:str = "DEBUG"
    Logger = sys.stderr
