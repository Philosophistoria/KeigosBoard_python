from lib2to3.pytree import convert
from operator import is_
from turtle import pu
import numpy as np
from switch_board import *
import time
import util

from pynput.keyboard import Listener, Key

is_running = True
is_stimulating = False
port = "COM5"
baudrate = 921600
stim = SwitchBoard(port, baudrate)

intensity = 5
pulse_width = 500
channel = 1

def keypress_callback(key) :
    global is_running, stim, intensity, pulse_width, channel
    global is_stimulating

    if (hasattr(key, "char")) :
        c = key.char

        if (c == 'q') :
            print("quit")
            is_running = False
        elif (c == 'n') :
            channel = channel % 8 + 1 # 1-8
            print(f"channel: {channel}")
        elif (c == 's') :
            is_stimulating = not is_stimulating

    if (key == Key.up) :
        print(f"current intensity: {intensity}")
        intensity = util.clamp(intensity + 0.5, 0, 24)
    elif (key == Key.down) :
        print(f"current intensity: {intensity}")
        intensity = util.clamp(intensity - 0.5, 0, 24)

    elif (key == Key.left) :
        print(f"current pulse_width: {pulse_width}")
        pulse_width = util.clamp(pulse_width - 10, 0, 1000)
    elif (key == Key.right) :
        print(f"current pulse_width: {pulse_width}")
        pulse_width = util.clamp(pulse_width + 10, 0, 1000)

def convert_current_to_command(current) :
    current = util.clamp(current, 0, 24)
    command = (current + 0.01) / 0.00566
    return int(command)

def custom_sleep(ms) :
    st = time.perf_counter_ns()
    et = st + ms * 1000
    ct = st
    while ct < et :
        ct = time.perf_counter_ns()

def reverse_polarity(ch) :
    global stim
    s = stim.get_switch_state(ch)
    if (s == State.Gnd) :
        stim.set_switch_state(State.High)
    elif (s == State.High) :
        stim.set_switch_state(State.Gnd)

def swap_polarity(ch1, ch2) :
    global stim
    s1 = stim.get_switch_state(ch1)
    s2 = stim.get_switch_state(ch2)

    stim.set_switch_state(ch1, s2)
    stim.set_switch_state(ch2, s1)

def change_other_channels_to_open(ch1, ch2) :
    for i in range(1, stim.ElectrodeNum+1) :
        if (i == ch1 or i == ch2) :
            continue
        stim.set_switch_state(i, State.Open)

def line_stimulation(pulse_count, command, pulse_width) :
    global stim
    electrode_set = [(1, 2), (3, 4), (5, 6)]
    intensities = [22, 13, 14]
    commands = [convert_current_to_command(intensity) for intensity in intensities]
    
    for j, (ch1, ch2) in enumerate(electrode_set) :
        change_other_channels_to_open(ch1, ch2)
        stim.set_switch_state(ch1, State.High)
        stim.set_switch_state(ch2, State.Gnd)
        for i in range(pulse_count) :
            # stim.stimulate(command, pulse_width)
            # print(j, ch1, ch2)
            stim.stimulate(commands[j], pulse_width)
            # reverse_polarity(ch1, ch2)
            # custom_sleep(10)
            time.sleep(0.01)
        

t = 0
def wave_stimulation(command, pulse_width) :
    global t, stim
    t = time.time_ns()  / 1000000000.0 # -> sec
    electrode_set = [(1, 2), (3, 4), (5, 6)]
    intensities = [22, 13, 14]

    freq = 0.5
    index = int(np.ceil(3 * (0.5 * np.sin(2 * np.pi * freq * t) + 0.5)))
    
    ch1, ch2 = electrode_set[index - 1]
    swap_polarity(ch1, ch2)
    # change_other_channels_to_open(ch1, ch2)
    
    stim.stimulate_2ch(ch1, ch2, command, pulse_width)



def main() :

    global is_running, stim, intensity, pulse_width
    global is_stimulating

    listener = Listener(on_press=keypress_callback)
    listener.start()

    pulse_count = 50
    # pulse_width = 300
    # intensity = 10 # 0 ~ 20 mA

   
    # initializing switch state before stimulation
    for i in range(1, 6 + 1, 2) :
        print(f"current: {i}")
        stim.set_switch_state(i, State.High)
        stim.set_switch_state(i+1, State.Gnd)

    try :
        while is_running :
            

            if (is_stimulating) :
                # user_input = input(f"set intensity (current intensity={intensity}): ")
                # if (user_input != '') :
                #     intensity = int(user_input)

                command = convert_current_to_command(intensity)
                # print(f"command value is: {command}")

                stim.stimulate(command, pulse_width)

                
                # line_stimulation(pulse_count, command, pulse_width)
                # wave_stimulation(command, pulse_width)

            time.sleep(0.01)
    except KeyboardInterrupt as e :
        print("key board interrupted")
        stim.close()

    # if stim.serial_port.is_open :
    #     stim.close()


if __name__ == "__main__" :
    main()