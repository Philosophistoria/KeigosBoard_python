class Dummy:
    def __init__(self, port:str="DEBUG") -> None:
        print("port:" + port)

    def set_pulse(self, intensity:float, pulsewidth:int) -> None:
        #print("intensity:   " + str(intensity))
        #print("pulse width: " + str(pulsewidth))
        pass

    def change_mode(self, mode:int):
        #print (mode)
        pass

    def start(self, channel:str, wave_period:float) -> None:
        print("run")

    def end(self) -> None:
        print("stop")
    
    def update(self) -> None:
        #print("update")
        pass
