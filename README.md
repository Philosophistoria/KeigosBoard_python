# KeigosSwitchingBoard_python
Python script for Keigo's switching board with rehamove 3

esp32 side code and hardwares: https://github.com/Philosophistoria/KeigosSwitchingBoard_esp32/blob/main

---
**I CONFIRMED THIS PYTHON PROGRAM WORKS ONLY WITH PYTHON3.10 and LINUX_AMD64 ENVIRONMENT**

1. the keyinput module might not work.
     - if so, please prepare other single key input module for your system and change keybind code in `__main__.py`
     - for example, https://pypi.org/project/getch/
       
1. rehastim module have to be modified to appropriate implementation
     - inside of `rehamove_wrapper.py`, please modify the first import line as below
       ```diff
       - from .rehamove_integration_lib.builds.python.linux_amd64 import rehamove
       + from .rehamove_integration_lib.builds.python.windows_amd64 import rehamove
       # or
       + from .rehamove_integration_lib.builds.python.macOS import rehamove
       ```
1. you could find some wiered strings appear when text printed.
    - it could be solved by turning on the Virtual Terminal Sequences(ANSI escape sequences), or change `utils.bcolors`'s elements to null string `''`
    - this may happen because some ANSI escape sequence codes are inserted to `print()` in `rehamove_wrapper.py` and `com_esp32_switch_board.py` to change the color of text print()ed to the console.


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
- open the `Setting.py` and make configurations such as COM Port.
     - if you don't have the devices, set the com ports to "DEBUG" so that the program behaves dummy.

- inside of `rehamove_wrapper.py`, please modify the first import line as below
  ```diff
  - from .rehamove_integration_lib.builds.python.linux_amd64 import rehamove
  + from .rehamove_integration_lib.builds.python.windows_amd64 import rehamove
  # or
  + from .rehamove_integration_lib.builds.python.macOS import rehamove
  ```

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

