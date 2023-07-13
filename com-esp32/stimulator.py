# serial communication
from tkinter.tix import MAX
import serial
import struct
import numpy as np
import time
# ---

import util

from typing import List, Tuple
from enum import IntEnum

PC_ESP32_MEASURE_REQUEST = 0xFE
PC_ESP32_STIM_PATTERN = 0xFF

ESP32_PC_MEASURE_RESULT: int = 0xFF
STATE_HIGH: np.uint8 = 2 # connect to Vpp
STATE_GND: np.uint8 = 1 # connect to GND
STATE_OPEN: np.uint8 =0 # high impedance mode
MAX_VOLUME: int = 4095
MIN_VOLUME: int = 0

class State (IntEnum) :
    High = 2
    Gnd = 1
    Open = 0

# for electrical stimulation
class Stimulator :

    ElectrodeNum = 16
    Baudrate: int = 921600
    Comport: str = "COM3" # change
    # 配列的にアクセスするために、各電極の座標を計算して二次元配列にしたもの7
    # 上のposition配列では奇数や偶数になっているが、それを 0 ~ [各軸の電極数] に変換した値
    # ConvertedElectrodePos = np.zeros((const.ELECTRODE_NUM, 2), dtype="<i8")
    # ElectrodeIntensities = np.zeros(const.ELECTRODE_NUM, dtype=np.float32)

    def __init__(self, port, baudrate) :
        Stimulator.Baudrate = baudrate
        Stimulator.Comport = port
        # self.electrode_num = 16
        self.switch_state = np.zeros(Stimulator.ElectrodeNum, dtype="<i1")
        self.serial_port = serial.Serial(port=Stimulator.Comport,baudrate=Stimulator.Baudrate, write_timeout=0)


    def set_all_open(self) :
        for i in range(0, Stimulator.ElectrodeNum) :
            self.switch_state[i] = int(State.Open)

    def set_switch_state(self, channel, state) :
        index = channel - 1
        if index > len(self.switch_state) :
            print("the index is exceeded with the number of the channels")
            return
        
        self.switch_state[index] = int(state)
        # print(f"current switch state: {self.switch_state}")

    def get_switch_state(self, channel) :
        index = channel - 1
        return self.switch_state[index]

    def get_all_switch_states(self) :
        return self.switch_state

    def convert_current_to_command(current) :
        # convert current [mA] to command (0 - 4095)
        current = util.clamp(current, 0, 24) # max: 24mA
        command = (current + 0.01) / 0.00566
        return int(command)

    def stimulate_2ch(self, ch1, ch2, volume, width) :
        print(f"current switch state: {self.switch_state}")
        print(f"volume: {volume}, width: {width}")
        i1 = ch1 - 1
        i2 = ch2 - 1

        temp_switch_state = np.zeros(Stimulator.ElectrodeNum, dtype="<i1")
        temp_switch_state[i1] = self.switch_state[i1]
        temp_switch_state[i2] = self.switch_state[i2]

        volume = util.clamp(volume, MIN_VOLUME, MAX_VOLUME) # constrain in case a value over 4095 is passed

        l_vol = volume & 0x3f
        h_vol = volume >> 6

        # just stimulate 2 channels while keeping other switching states
        send_data = bytearray([PC_ESP32_STIM_PATTERN, l_vol, h_vol, int(width/10.0)] + list(temp_switch_state))
        # print(send_data)
        try :
            self.serial_port.write(send_data)
        except Exception as e :
            print(e)

    def _set_switch_state_to_anode(self, ch) :
        for i in range(0, Stimulator.ElectrodeNum) :
            if (i == ch-1) :
                self.switch_state[i] = int(State.High)
            else :
                self.switch_state[i] = int(State.Open)
        self.switch_state[7] = State.Gnd # [caution] temp test

    def _set_switch_state_to_cathode(self, ch) :
        for i in range(0, Stimulator.ElectrodeNum) :
            if (i == ch-1) :
                self.switch_state[i] = int(State.Gnd)
            else :
                self.switch_state[i] = int(State.Open)
        self.switch_state[7] = State.High # [caution] temp test

    def stimulate_1ch(self, ch, state, volume, width) :
        if (state == State.High) :
            self._set_switch_state_to_anode(ch)
        elif (state == State.Gnd) :
            self._set_switch_state_to_cathode(ch)
        
        self.stimulate(volume, width)

    def stimulate(self, volume, width) :
        print(f"current switch state: {self.switch_state}")
        print(f"volume: {volume}, width: {width}")

        volume = util.clamp(volume, MIN_VOLUME, MAX_VOLUME)

        l_vol = volume & 0x3f
        h_vol = volume >> 6

        send_data = bytearray([PC_ESP32_STIM_PATTERN, l_vol, h_vol, int(width/10.0)] + list(self.switch_state))
        # print(send_data)
        try :
            self.serial_port.write(send_data)
        except Exception as e :
            print(e)


    def close(self) :
        self.serial_port.flush()
        self.serial_port.close()