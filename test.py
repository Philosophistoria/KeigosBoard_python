class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            #tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            print("called", [ch], ord(ch))
        finally:
            #termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            pass
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

while True:
    getch = _Getch()
    x = getch()

    if (int(x) == 1):
        print ('\n')
        print ('correct')
        print (x)
    else:
        print ("\n")
        print ('wrong')
        print (x)

'''
from .rehamovelib.builds.python.linux_amd64.rehamove import *          # Import our library
r = Rehamove("/dev/ttyS6")            # Open USB port (on Windows)
r.set_pulse(6, 200)
r.run("red", 10, 500)
'''
'''
import time
for i in range(0, 100):
    r.pulse("red", 6, 200)     # Send pulse every second
    time.sleep(.02)
'''
