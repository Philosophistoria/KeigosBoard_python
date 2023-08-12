
from .com_esp32_switch_board import *
import numpy as np
import time
import threading


from . import Settings
from .rehamove_wrapper import DRehamove


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
        self.pulse_width = 200 # for each phase = 2 * 200 () + 100 (for switching) in total 
        self.frequency = 100
        self.period = 1000.0 / self.frequency
        self.channel = 1
        self.reset_all_channels_states()
        self.print_param()
        self.rehamove.change_mode(1)
    

    def print_param (self) -> None:
        print("=== print parameter ===")
        print(  f"intensity: {np.round(self.intensity,1)}\n"
              + f"p_width:   {self.pulse_width}\n"
              + f"frequency: {self.frequency}\n"
              + f"channel:   {self.channel}\n")
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
        

    # <instance>.rehamove.update() should be called at least every 2 sec while the status is stimulating
    def start(self):
        self.rehamove.set_pulse(self.intensity[self.channel - 1], self.pulse_width)
        self.rehamove.start("red", self.period) 
    

    def stop(self):
        self.rehamove.end()

    
    def update(self):
        self.rehamove.set_pulse(self.intensity[self.channel - 1], self.pulse_width)
        self.rehamove.update()

    
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
