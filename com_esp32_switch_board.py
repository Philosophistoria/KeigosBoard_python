# serial communication
import sys
from . import utils
from .utils import bcolors
import serial
import numpy as np
# ---
from enum import Enum, IntEnum 

class State (Enum):
    High = np.uint8(2)
    Gnd  = np.uint8(1)
    Open = np.uint8(0)

class REACTION_MODE(Enum):
    ON_EVERY_REQUEST         = np.uint8(0)
    ONLY_ON_REACTION_REQUEST = np.uint8(1)
    NO_REACTION              = np.uint8(2)

class REQUEST(Enum): 
    CHANGE_STATE          = np.uint8(0xff)
    CHECK_STATE           = np.uint8(0xfe)
    CHANGE_REACTION_MODE  = np.uint8(0xfd)


# for electrical stimulation
class SwitchBoard :

    def __init__(self, channel_num:int = 16, port:str = "DEBUG", baudrate:int = 921600, rcvbuf = sys.stderr, echo_mode:REACTION_MODE = REACTION_MODE.NO_REACTION) :
        # the number of electrodes
        self.numof_channels:int = channel_num 
        # serial port parameter
        self._baudrate:int = baudrate
        self._COM_port:str = port

        if (hasattr(rcvbuf, "write") and callable(rcvbuf.write)):
            self.rcvbuf = rcvbuf
        else:
            self.rcvbuf = sys.stderr

        try:
            self.echo_mode = REACTION_MODE(echo_mode)
        except ValueError:
            self.echo_mode = REACTION_MODE.NO_REACTION
        utils.log(f"SwitchBoard: reaction mode: {echo_mode}", color = bcolors.PURPLE)

        # switch array state: array of 1 byte integer
        self.switch_state = np.zeros(self.numof_channels, dtype="<u1")
        # open serial port
        if port == "DEBUG":
            # Option to set stdout for debugging
            self.serial_port = sys.stderr#.buffer
            utils.log("SwitchBoard: DEBUG MODE - it will echo the bytes on stdout", color = bcolors.PURPLE)
        else:
            try:
                self.serial_port = serial.Serial(port = self._COM_port, baudrate = self._baudrate, write_timeout=0)
                utils.log("SwitchBoard: Successed to open serial port" + self._COM_port, color = bcolors.PURPLE)
                if self.serial_port == None:
                    utils.log("SwitchBoard: Failed to open serial port" + self._COM_port, color = bcolors.PURPLE)
                if self.echo_mode != REACTION_MODE.NO_REACTION:
                    self.serial_port.write([REQUEST.CHANGE_REACTION_MODE.value, self.echo_mode.value])
            except Exception as e:
                utils.log(f"SwitchBoard: Failed to open serial port: {self._COM_port}", color = bcolors.YELLOW)
                utils.log(f"SwitchBoard: {sys._getframe().f_code.co_name}: {e}", color = bcolors.YELLOW)


    def set_all_open(self) :
        for i in range(0, self.numof_channels) :
            self.switch_state[i] = State.Open


    def set_channel_state(self, channel, state:State) :
        try:
            State(state)
        except ValueError:
            utils.log(f"SwitchBoard: An element in the list given doesn't match the State(IntEnum) type", color = bcolors.YELLOW)
            return -1
        except Exception as e:
            utils.log(f"SwitchBoard: {sys._getframe().f_code.co_name}: {e}", color = bcolors.YELLOW)
            return -1
        if channel < 1 or len(self.switch_state) < channel:
            utils.log("SwitchBoard: The index is exceeded with the number of the channels", color = bcolors.YELLOW)
            return -1
        self.switch_state[channel - 1] = state
        utils.log(f"SwitchBoard: current switch state: {self.switch_state}", color = bcolors.PURPLE)
        return 0


    def set_all_channels_states(self, state:np.ndarray[State]) :
        # check the length of the array given
        if len(state) != self.numof_channels:
            utils.log("SwitchBoard: The length of the list defining the switch state does not match the one declared", color = bcolors.YELLOW)
            return
        # check if the elements in the array can be regarded as State
        for elm in state:
            try:
                State(elm)
            except ValueError:
                utils.log("SwitchBoard: An element in the list given doesn't match the State(IntEnum) type", color = bcolors.YELLOW)
                return
            except Exception as e:
                utils.log(f"SwitchBoard: {sys._getframe().f_code.co_name}: {e}", color = bcolors.YELLOW)
                return
        # Not to change the type of array
        for i in range(self.numof_channels):
            self.switch_state[i] = state[i].value
        utils.log(f"SwitchBoard: switch state was reset.  current state: {self.switch_state}", color = bcolors.PURPLE)


    def roll_all_channels_states(self, numof_roll):
        self.switch_state = np.roll(self.switch_state, numof_roll) 
        utils.log(f"SwitchBoard: switch state was rolled. current state: {self.switch_state}", color = bcolors.PURPLE)


    def get_channel_state(self, channel) :
        return self.switch_state[channel - 1]


    def get_all_channels_states(self) :
        return self.switch_state


    def send_all_channels_states(self):
        try :
            #data = np.append(np.array([REQUEST.CHANGE_STATE], dtype="int8"), self.switch_state)
            data = np.append(REQUEST.CHANGE_STATE.value, self.switch_state)
            utils.log(f"{list(data), data.dtype}", color = bcolors.PURPLE)
            check = np.array([REQUEST.CHECK_STATE.value], dtype="uint8")
            if self._COM_port == "DEBUG":
                utils.log(f"SwitchBoard: DEBUG MODE - echo (size {len(data)})", color = bcolors.PURPLE)
                data = "SitchBoard: DEBUG MODE: " + repr(data) + "\n"
                check ="SitchBoard: DEBUG MODE: " + repr(check) + "\n"
            self.serial_port.write(data)
            self.serial_port.write(check)
            self.serial_port.flush()
        except Exception as e :
            utils.log(f"SwitchBoard: {sys._getframe().f_code.co_name}: {e}", color = bcolors.YELLOW)


    def read_serial(self):
        data = None
        try:
            if hasattr(self.serial_port, "in_waiting") and self.serial_port.in_waiting:
                self.rcvbuf.write (bcolors.BLUE + f"data received: {self.serial_port.in_waiting}\n" + bcolors.END)
                data = self.serial_port.read_all()
                self.rcvbuf.write (bcolors.BLUE + "=== (switch board) ===\n" + bcolors.END)
                self.rcvbuf.write (bcolors.BLUE + data.decode() + "\n" + bcolors.END)
                self.rcvbuf.write (bcolors.BLUE + "=== end of data ===\n" + bcolors.END)
        except Exception as e :
            utils.log(f"SwitchBoard: {e}", color = bcolors.PURPLE)

    def close(self) :
        self.serial_port.flush()
        self.serial_port.close()