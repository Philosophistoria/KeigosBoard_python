from .rehamovelib.builds.python.linux_amd64.rehamove import *          # Import our library
import time

r = Rehamove("/dev/ttyS6")            # Open USB port (on Windows)
for i in range(0, 100):
    r.pulse("red", 6, 200)     # Send pulse every second
    time.sleep(.02)
