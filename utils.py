
class bcolors:
    ASIS = ''
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

import sys
g_logger = sys.stderr
def log(text, logger = g_logger, color:str = bcolors.ASIS, eol = "\n"):
    logger.write(color + text + bcolors.END + eol)