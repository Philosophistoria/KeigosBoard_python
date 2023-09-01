
class bcolors:
    ASIS    :str    = ''
    PURPLE  :str    = '\033[95m'
    CYAN    :str    = '\033[96m'
    DARKCYAN:str    = '\033[36m'
    BLUE    :str    = '\033[94m'
    GREEN   :str    = '\033[92m'
    YELLOW  :str    = '\033[93m'
    RED     :str    = '\033[91m'
    BOLD    :str    = '\033[1m'
    UNDERLINE:str   = '\033[4m'
    END     :str    = '\033[0m'

import sys
g_logger = sys.stderr
def log(text:str, logger = g_logger, color:str = bcolors.ASIS, eol = "\n"):
    logger.write(str(color) + str(text) + str(bcolors.END) + eol)