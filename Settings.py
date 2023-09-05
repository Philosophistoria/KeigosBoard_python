from .com_esp32_switch_board import REACTION_MODE
class SwitchBoard:
    Numof_channels:int = 12
    #COM_Port:str = "/dev/ttyS9"
    COM_Port:str = "DEBUG"
    '''
        if com port is set as "DEBUG", no serial port will be open
        but the class behave as it was open.
    '''
    Baudrate:int = 1500000 #921600
    #Reaction_Mode:REACTION_MODE = REACTION_MODE.ON_EVERY_REQUEST 
    '''
        With this mode, the switch board not only echo the header, 
        it returns some reactions on every request. 
        This is good for debug or something
    '''
    Reaction_Mode:REACTION_MODE = REACTION_MODE.NO_REACTION
    '''
        With this mode, nothing is returns from switch board.
    '''
import sys
class Rehamove:
    #COM_Port:str = "/dev/ttyS10"
    COM_Port:str = "DEBUG"
    '''
        if com port is set as "DEBUG", no serial port will be open
        but the class behave as it was open.
        In this case Dummy class object will be returned.
    '''
    Logger = sys.stderr

class StimulatingPattern:
    Gap:int = 0
    Pulse_Width:int = 200 # for each phase = 2 * 200 () + 100 (for switching) in total 
    Frequency:int = 100