from .rehamove_integration_lib.builds.python.linux_amd64.rehamove import * 
from .rehamove_integration_lib.builds.python.linux_amd64.rehamovelib import * 
from .com_esp32.switch_board import *
import numpy as np
import time
import threading


from . import Settings
from . import rehamove_dummy

class ProcStatus:
    is_running = True
    is_stimulating = False


class Stimulator:

    def __init__(self) -> None:
        self.switchbd = SwitchBoard(
            channel_num = Settings.SwitchBoard.Numof_channels, 
            port = Settings.SwitchBoard.COM_Port, 
            #port = "DEBUG",
            baudrate = Settings.SwitchBoard.Baudrate,
            echo_mode = REACTION_MODE.ON_EVERY_REQUEST) 
        self.rehamove = rehamove_dummy.Dummy("DEBUG")
        #self.rehamove = Rehamove(Settings.Rehamove.COM_Port, logger=sys.stderr)
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
    ... GND [GAP GAP] STIM [GAP GAP] GND ... if 2 gaps
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
        self.rehamove.set_pulse(self.intensity[0], self.pulse_width)
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


from .keyinput_module import keyinput, singlebuffer, queuebuffer
from .keyinput_module.pyobservable import observable, observer



def keypress_callback(buf:queuebuffer.QueueBuffer, status:ProcStatus, stimulator:Stimulator) :

    key = ord(buf.read())
    #print(key)

    # If tty setting is C-break mode or richer, the line below is no needed
    if (key == 3):
        # Ctrl+C (^C) is pressed
        raise KeyboardInterrupt
    # --------------------------------------------
    # keybind
    # --------------------------------------------
    elif (key == ord('q')) :
        status.is_running = False
        print("quit\n")
    elif (key == ord('a')) :
        status.is_stimulating = not status.is_stimulating
        if(status.is_stimulating):
            print("started")
            stimulator.start()
        else:
            print("stopped")
            stimulator.stop()
    elif (key == ord('s')) :
        status.is_stimulating = True
        stimulator.start()
    elif (key == ord('p')) :
        status.is_stimulating = False
        stimulator.stop()
    elif (key == 27):
        buf.wait_new_data()
        # Check if the 2nd char is ok as arrow key
        key = ord(buf.read())
        if not key == 91:
            print('not an arrow key: ' + str(key))
            buf.flush()
        buf.wait_new_data()
        # Check what arrow key is pressed
        key = ord(buf.read())
        # UP
        if (key == 65) :
            stimulator.stop()
            stimulator.intensity[stimulator.channel - 1] = np.clip(stimulator.intensity[stimulator.channel - 1] + 0.5, 0, 24)
            if(status.is_stimulating):
                stimulator.start()
        # DOWN
        elif (key == 66) :
            stimulator.stop()
            stimulator.intensity[stimulator.channel - 1] = np.clip(stimulator.intensity[stimulator.channel - 1] - 0.5, 0, 24)
            if(status.is_stimulating):
                stimulator.start()
        # RIGHT
        elif (key == 67) :
            stimulator.stop()
            stimulator.set_channel(((stimulator.channel -1) + 1) % stimulator.switchbd.numof_channels + 1)
            if(status.is_stimulating):
                stimulator.start()
        # LEFT
        elif (key == 68) :
            stimulator.stop()
            stimulator.set_channel(((stimulator.channel -1) - 1) % stimulator.switchbd.numof_channels + 1)
            if(status.is_stimulating):
                stimulator.start()

    stimulator.print_param()


if __name__ == "__main__" :
    status = ProcStatus()
    stimulator = Stimulator()
    stimulator.start_listening()

    itr = 0
    ev=threading.Event()
    command_buf = observable.ObservableNotifier(queuebuffer.QueueBuffer())
    #command_buf.notifier.debug = True
    command_buf.attatch(observer.receive_notification_by(ev.set,'write','post'))
    keylistener = keyinput.KeyListener(command_buf, '')
    keylistener.daemon = True
    keylistener.start()

    print("wait for secs...")
    time.sleep(1)
    print("done")
    prompt = keyinput.PromptView('neko > ')
    prompt.showPrompt(False)
    isStarted = False

    try :
        while status.is_running:
            time.sleep(0.01)
            if status.is_stimulating:
                itr += 1
                if(itr == 100):
                    stimulator.update()
                    itr = 0
            if command_buf.readable():
                keypress_callback(command_buf, status, stimulator)
                prompt.showPrompt(False)
        print("the process will end\n")
    except KeyboardInterrupt as e :
        print("key board interrupted\n")
        stimulator.switchbd.close()

    # if stimulator.switchbd.serial_port.is_open :
    #     stimulator.switchbd.close()

    stimulator.end_listening()
    keylistener.terminate()
    keylistener.join()