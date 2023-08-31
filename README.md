# KeigosSwitchingBoard_python
Python script for Keigo's switching board with rehamove 3

esp32 side code and hardwares: https://github.com/Philosophistoria/KeigosSwitchingBoard_esp32/blob/main

---
**I CONFIRMED THIS PYTHON PROGRAM WORKS ONLY WITH PYTHON3.10 and LINUX_AMD64 ENVIRONMENT**

if you'r using windows or mac

1. maybe the keyinput module doesn't work.
     - -> please prepare other single key input module for your system and change keybind code in `__main__.py`
1. rehastim module have to be modified to appropriate implementation
     - inside of `rehamove_wrapper.py`, please modify the first import line as below
       ```diff
       - from .rehamove_integration_lib.builds.python.linux_amd64 import rehamove
       + from .rehamove_integration_lib.builds.python.windows_amd64 import rehamove
       # or
       + from .rehamove_integration_lib.builds.python.macOS import rehamove
       ```
     - you might have to change an absolute import to a relative import in the `rehamove.py`
       ```diff
       - import rehamovelib
       + from . import rehamovelib
       ```
     - somehow, the `rehamove.py` prints all messages to `stdout`, and it is really bothering.
          - so I chagnged the `rehamove.py` for Linux as it logs the messages to `stderr`.
          - if you also bothering about the many meeages from `rehamove.py` I would recommend changing the one for your system so that the messages printed out to `stderr` 
1. you could find some wiered strings appear when text printed.
    - may turn on the Virtual Terminal Sequences(ANSI escape sequences), or change `utils.bcolors`'s elements to null string `''`
    - this is because some ANSI escape sequences code is inserted to `print()` in `rehamove_wrapper.py` and `com_esp32_switch_board.py` to change the color of text print()ed to the console.


---

# How to use

## Clone the repository
when cloning repository, don't forget download the submodules by adding `--recursive` option or `git submodule init` / `update`.
```bash
git clone --recursive https://github.com/Philosophistoria/KeigosSwitchingBoard_python.git
```

or
```bash
git clone https://github.com/Philosophistoria/KeigosSwitchingBoard_python.git
git submodule init
git submodule update
```

## Configuration
open the `Setting.py` and make configurations such as COM Port.
if you don't have the devices, set the com ports to "DEBUG" so that the program behaves dummy.

## Run
with any message printed to `stdout` and `stderr`
```bash
python3 -m KeigosSwitchingBoard_python
```

w/o the messages to `stderr`, discard them, for example of `bash`, by the following:
```bash
python3 -m KeigosSwitchingBoard_python > /dev/null
```

Because `__main__.py` is prepared, and relative import is used in the `__main__.py`, so only the above way (with `-m` option; executed as a module) works.
You can modify the relative import to absolute one in the `__main__.py`, you can execute it by:

```bash
mv KeigosSwitchingBoard_python
python3 __main__.py
```
or
```bash
mv KeigosSwitchingBoard_python
python3 -m __main__
```

