
from .com_esp32_switch_board import *
import numpy as np
import time
import threading


from . import Settings
from .rehamove_wrapper import DRehamove
from enum import Enum, IntEnum 
from . import utils

class Stimulator:

    def __init__(self) -> None:
        self.switchbd = SwitchBoard(
            channel_num = Settings.SwitchBoard.Numof_channels, 
            port        = Settings.SwitchBoard.COM_Port, 
            baudrate    = Settings.SwitchBoard.Baudrate,
            echo_mode   = Settings.SwitchBoard.Reaction_Mode
            ) 
        self.rehamove = DRehamove(
            port    = Settings.Rehamove.COM_Port, 
            logger  = Settings.Rehamove.Logger
            )
        self.intensity = np.zeros(self.switchbd.numof_channels, dtype="<f8")
        self.pulse_width = Settings.StimulatingPattern.Pulse_Width
        self.frequency = Settings.StimulatingPattern.Frequency
        self.period = 1.0 / self.frequency
        self.channel = 1
        # ---alt mode ----
        self.channel_list = [self.channel]
        self.num_pulse_to_alt_ch = 1 
        self.altmode = False
        # ----------------
        self.reset_all_channels_states(gap=Settings.StimulatingPattern.Gap)
        self.print_param()
        self.rehamove.change_mode(1)
    

    def print_param (self) -> None:
        print("=== print parameter ===")
        print(  f"intensity: {np.round(self.intensity,1)}\n"
              + f"p_width:   {self.pulse_width}\n"
              + f"frequency: {self.frequency}\n"
              + f"channel:   {self.channel}\n"
              + f"channel list:   {self.channel_list}\n")
        sys.stdout.flush()

    
    '''
    set Channel 1 as stim electrode and others as grd with 2 gaps bw stim and gnd
    ... GND [GAP GAP] STIM [GAP GAP] GND ... if  gap = 2
    ... GND [   section not GND    ] GND ...
    '''
    def reset_all_channels_states(self, gap:int = 2):
        states = [State.Gnd] * self.switchbd.numof_channels
        '''
        The gap is the spacial interval between STIM and GND
        This implementation the gap is prepared symmetrically
        *2 because the gap is prepared symmetrically
        +1 for stimulation electrode
        '''
        section_notGND = gap * 2 + 1
        for i in range(section_notGND):
            ch = (i - int(section_notGND / 2)) % self.switchbd.numof_channels + 1
            if (ch == 1):
                # Set Stim channel
                states[ch - 1] = State.High
            else:
                # Set Gap Channel
                states[ch - 1] = State.Open
        self.switchbd.set_all_channels_states(states)
        self.set_channel(1)


    def set_channel(self, ch):
        self.switchbd.roll_all_channels_states(ch - self.channel)
        self.channel = ch
        self.switchbd.send_all_channels_states()
        time.sleep(0.01)


    def set_channel_list(self, ch_list:list):
        for i in range(len(ch_list)):
            ch_list[i] = (ch_list[i] - 1) % Settings.SwitchBoard.Numof_channels + 1
        self.channel = ch_list[0]
        self.channel_list = ch_list


    def set_num_pulse_to_alt_ch(self, num):
        self.num_pulse_to_alt_ch = num
        

    # <instance>.rehamove.update() should be called at least every 2 sec while the status is stimulating
    def start(self, altmode = None):
        if altmode != None and type(altmode) is bool:
            self.altmode = altmode
        if not self.altmode:
            self.rehamove.change_mode(1)
            self.rehamove.set_pulse(self.intensity[self.channel - 1], self.pulse_width)
            self.rehamove.start("red", self.period) 
        else:
            self.rehamove.change_mode(0)
            self.altmode_stimulation_alive = True
            self.altmode_stimulation_thread = threading.Thread(target=self._altmode_stimulation)
            self.altmode_stimulation_thread.start()
    

    def stop(self):
        if not self.altmode:
            self.rehamove.end()
        else:
            self.altmode_stimulation_alive = False
            self.altmode_stimulation_thread.join()

    
    def update(self):
        if not self.altmode:
            self.rehamove.change_mode(1)
            self.rehamove.set_pulse(self.intensity[self.channel - 1], self.pulse_width)
            self.rehamove.update()
        else:
            utils.log("updated: altmode")


    def _altmode_stimulation(self):
        t = 0
        while self.altmode_stimulation_alive:
            self.set_channel(self.channel_list[0])
            for i in range(self.num_pulse_to_alt_ch):
                self.rehamove.pulse(self.channel, self.intensity[self.channel - 1], self.pulse_width)
                t_tmp = time.perf_counter()
                if t != 0 and t_tmp - t < self.period:
                    time.sleep(self.period - (t_tmp - t))
                else:
                    time.sleep(self.period)
                t = t_tmp
            self.channel_list = np.roll(self.channel_list, 1)

    
    def _listener_switchboard(self):
        while self.listener_alive:
            self.switchbd.read_serial()


    def start_listening(self):
        self.listener_alive = True
        self.listener = threading.Thread(target = self._listener_switchboard)
        self.listener.start()


    def end_listening(self):
        self.listener_alive = False
        self.listener.join()
