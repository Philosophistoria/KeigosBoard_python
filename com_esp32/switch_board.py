# serial communication
import sys
import serial
import numpy as np
# ---
from enum import IntEnum 

class State (IntEnum) :
    High = 2
    Gnd = 1
    Open = 0

# for electrical stimulation
class SwitchBoard :

    def __init__(self, channel_num:int = 16 , port:str = "DEBUG", baudrate:int = 921600) :
        # the number of electrodes
        self.numof_channels:int = channel_num 
        # serial port parameter
        self._baudrate:int = baudrate
        self._COM_port:str = port

        # data header
        self.header = 0xff
        # switch array state: array of 1 byte integer
        self.switch_state = np.zeros(self.numof_channels, dtype="<i1")
        # open serial port
        if port == "DEBUG":
            # Option to set stdout (accept bite string) for debugging
            self.serial_port = sys.stdout.buffer
        else:
            try:
                self.serial_port = serial.Serial(port = self._COM_port, baudrate = self._baudrate, write_timeout=0)
            except:
                print ("Failed to open serial")


    def set_all_open(self) :
        for i in range(0, self.numof_channels) :
            self.switch_state[i] = State.Open


    def set_channel_state(self, channel, state) :
        if channel < 1 or len(self.switch_state) < channel:
            print("The index is exceeded with the number of the channels")
            return
        self.switch_state[channel - 1] = state
        print(f"current switch state: {self.switch_state}")


    def set_all_channels_states(self, state:np.ndarray[State]) :
        # check the length of the array given
        if len(state) != len(self.switch_state):
            print("The length of the list defining the switch state does not match the one declared")
            return
        # check if the elements in the array can be regarded as State
        for elm in state:
            try:
                State(elm)
            except ValueError:
                print ("An element in the list given doesn't match the State(IntEnum) type")
                return
        print(f"current switch state: {self.switch_state}")
        # Not to change the type of array
        for i in range(self.numof_channels):
            self.switch_state[i] = state[i]


    def roll_all_channels_states(self, numof_roll):
        self.switch_state = np.roll(self.switch_state, numof_roll) 


    def get_channel_state(self, channel) :
        return self.switch_state[channel - 1]


    def get_all_channels_states(self) :
        return self.switch_state


    def send_all_channels_states(self):
        try :
            data = np.append([self.header], self.switch_state)
            self.serial_port.write(data)
        except Exception as e :
            print(e)


    def close(self) :
        self.serial_port.flush()
        self.serial_port.close()