from .multichannel_EMS import Stimulator
from .keyinput_module import keyinput, singlebuffer, queuebuffer
from .keyinput_module.pyobservable import observable, observer

import numpy as np


class ProcStatus:
    is_running = True
    is_stimulating = False


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
    import time
    status = ProcStatus()
    stimulator = Stimulator()
    stimulator.start_listening()

    itr = 0
    command_buf = queuebuffer.QueueBuffer()
    #command_buf.notifier.debug = True
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
