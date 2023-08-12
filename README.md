# KeigosSwitchingBoard_python
Python script for Keigo's switching board with rehamove 3

I CONFIRMED THIS PYTHON PROGRAM WORKS ONLY UNDER LINUX_AMD64 ENVIRONMENT

# How to use

```
# if not cloned
> git clone --recursive https://github.com/Philosophistoria/KeigosSwitchingBoard_python.git

# or
> git clone https://github.com/Philosophistoria/KeigosSwitchingBoard_python.git
> git submodule init
> git submodule update

# then execute the code 
> python3 -m KeigosSwitchingBoard_python
```

Because __main__.py is prepared, and relative import is used in the __main__.py, so only this way (with `-m` option; executed as a module) works.
You can modify the relative import to absolute one in the __main__.py, you can execute it by:

```
> mv KeigosSwitchingBoard_python
> python3 __main__.py
# or
> python3 -m __main__
```

