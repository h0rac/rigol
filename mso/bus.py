from abc import ABC, abstractmethod
import os
import json
import sys

with open("{}/rigol/bus.json".format(os.path.dirname(os.getcwd())), 'r') as f:
    bustypes = json.load(f)

class BusFactory(object):

    def factory(type, instr, busNum):
        if type == "RS232":
            return RS232Bus(instr, busNum)

    factory = staticmethod(factory)

class Bus():
    def __init__(self, instr):
        self.instr = instr
        self.busNum = None
    
    def setBus(self, busNum, busType):
        if busNum > 0 and busNum <= 4:
            self.busNum = busNum
            self.instr.write(":BUS{0}:MODE {1}".format(str(busNum), bustypes['mode'][busType.lower()]))
        else:
            print("Device support only 4 buses")
            sys.exit()
    
    def toggle(self, status=False):
        if status:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay ON".format(self.busNum))
        elif not status:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay OFF".format(self.busNum))
        else:
            print("Expect 'ON' or 'OFF to toggle bus'")
            sys.exit()

    
    def setLabel(self):
        print("test set label")

class RS232Bus(Bus):
    def __init__(self, instr, busNum):
        self.instr = instr
        self.busNum = busNum
    
    def setBoud(self):
        print("Boud set", self.busNum)